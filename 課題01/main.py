
import csv

path = "character_list.csv"


def opne_csv():
    with open(path) as f:
        source = list(csv.reader(f))[0]
        return source
    
def write_csv(source):
    with open(path, mode='w') as f:
        writer = csv.writer(f)
        writer.writerow(source)


### 検索ツール
def search():
    
    source = opne_csv()
    word =input("鬼滅の登場人物の名前を入力してください >>> ")

    if word in source:
        print(f"{word}が見つかりました")
    else:
        print(f"{word}が見つかりませんでしたのでsourceへ追加します")
        source.append(word)
        
        print(f"{word}をcharacter_list.csvへ追加します") 
        write_csv(source)
        
if __name__ == "__main__":
    search()