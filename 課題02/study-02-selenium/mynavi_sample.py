import os
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
import datetime
import re
import math


import pandas as pd

LOG_FILE_PATH = "logs/log_{datetime}.log"
log_file_path = LOG_FILE_PATH.format(datetime=datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S'))
EXP_CSV_PATH = "results/exp_list_{search_keyword}_{datetime}.csv"
success = 0
fail = 0


# Selenium4対応済


def set_driver(hidden_chrome: bool=False):
    '''
    Chromeを自動操作するためのChromeDriverを起動してobjectを取得する
    '''
    USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36"
    options = ChromeOptions()

    # ヘッドレスモード（画面非表示モード）をの設定
    if hidden_chrome:
        options.add_argument('--headless')

    # 起動オプションの設定
    options.add_argument(f'--user-agent={USER_AGENT}') # ブラウザの種類を特定するための文字列
    options.add_argument('log-level=3') # 不要なログを非表示にする
    options.add_argument('--ignore-certificate-errors') # 不要なログを非表示にする
    options.add_argument('--ignore-ssl-errors') # 不要なログを非表示にする
    options.add_experimental_option('excludeSwitches', ['enable-logging']) # 不要なログを非表示にする
    options.add_argument('--incognito') # シークレットモードの設定を付与
    
    # ChromeのWebDriverオブジェクトを作成する。
    service=Service(ChromeDriverManager().install())
    return Chrome(service=service, options=options)

def makedir_for_filepath(filepath: str):
    '''
    ファイルを格納するフォルダを作成する
    '''
    # exist_ok=Trueとすると、フォルダが存在してもエラーにならない
    os.makedirs(os.path.dirname(filepath), exist_ok=True)


def log(txt):
    '''
    ログファイルおよびコンソール出力
    (学習用に１から作成しているが、通常はloggingライブラリを推奨)
    '''
    now = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    logStr = '[%s: %s] %s' % ('log',now , txt)
    # ログ出力
    makedir_for_filepath(log_file_path)
    with open(log_file_path, 'a', encoding='utf-8_sig') as f:
        f.write(logStr + '\n')
    print(logStr)


def get_data(driver, page_count):
    
    result = []
    target_blocks = driver.find_elements(by=By.CLASS_NAME, value="cassetteRecruit__content")

    for i, block in enumerate(target_blocks):
        try :
            company = block.find_element(by=By.CLASS_NAME, value="cassetteRecruit__name").text
            catch_copy = block.find_element(by=By.CLASS_NAME, value="cassetteRecruit__copy").text
            print(company)
            print(catch_copy)
        
            data = {
                'ページ': page_count,
                "会社名": company, 
                "キャッチコピー": catch_copy,
            }
            log(f"[成功]{i+1} 件目 (page: {page_count}) : {company}")
            global success
            success += 1


            
            result.append(data)
        except Exception as e:
            log(f"[失敗]{i+1}  件目 (page: {page_count})")
            log(e)
            global fail
            fail += 1

    
    return result
        
        
def main():
    
    log(f"処理開始")
    search_keyword = input('検索ワードを入力してください:')
    log("検索キーワード:{}".format(search_keyword))

    # driverを起動
    driver = set_driver()
    
    # Webサイトを開く
    driver.get("https://tenshoku.mynavi.jp/")
    time.sleep(5)
    
    '''
    ポップアップを閉じる
    ※余計なポップアップが操作の邪魔になる場合がある
      モーダルのようなポップアップ画面は、通常のclick操作では処理できない場合があるため
      excute_scriptで直接Javascriptを実行することで対処する
    '''
    driver.execute_script('document.querySelector(".karte-close").click()')
    time.sleep(5)
    # ポップアップを閉じる
    driver.execute_script('document.querySelector(".karte-close").click()')

    # 検索窓に入力
    driver.find_element(by=By.CLASS_NAME, value="topSearch__text").send_keys(search_keyword)
    # 検索ボタンクリック
    driver.find_element(by=By.CLASS_NAME, value="topSearch__button").click()

    time.sleep(5)
    
    # 件数と最大ページ数を取得
    # ●件〜●件（全●●件中）のテキストを取得
    count_data_text = driver.find_element(by=By.CLASS_NAME, value="pager__text").text

    # 最大件数取得
    target_text = r'全(.+?)件'
    r = re.findall(target_text, count_data_text) 
    max_data = int(r[0].replace(',',''))
    
    # 最大ページ数を計算
    max_page = math.ceil(max_data/50)
    print(f'全{max_data}件,{max_page}ページあります')
    
    
    data = []

    page_count = 1
    while page_count <= max_page:
        
        print(f'{page_count}ページ目です！')
        
        time.sleep(3)
        result = get_data(driver, page_count)
        data.extend(result)
        
        
        left_arrow = driver.find_elements(by=By.CLASS_NAME, value="iconFont--arrowLeft")
        
        if left_arrow:
            left_arrow[0].click()
            page_count += 1
        else:
            log("最終ページです。終了します。")
            break
    
        
    print('処理終了')    
        
    # DataFrame作成
    now = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    df = pd.DataFrame(data)    
    makedir_for_filepath(EXP_CSV_PATH)
    df.to_csv(EXP_CSV_PATH.format(search_keyword=search_keyword, datetime=now), header=False, index=False, encoding='utf_8_sig')
    log(f"csv書き込み処理完了 成功件数: {success} 件 / 失敗件数: {fail} 件")


# 直接起動された場合はmain()を起動(モジュールとして呼び出された場合は起動しないようにするため)
if __name__ == "__main__":
    main()
