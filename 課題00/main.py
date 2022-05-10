def test():
    return '関数化の課題' 

def test2(name,hikisuu):
    if hikisuu in name:
        print(f'6 引数を使う関数の使い方:{hikisuu}は含まれます')
    else:
        print(f'6 引数を使う関数の使い方:{hikisuu}は含まれません')


def main():
    
    # １ 変数の使い方
    name1 = 'ねずこ'
    name2 = 'ぜんいつ'

    print('1 変数の使い方',name1)
    print('1 変数の使い方',name2)
    
    
    # ２ if文の使い方
    name2 = 'むざん'

    if name2 == 'むざん':
        print('2 if文の使い方:仲間ではありません')
        
        
    # ３ 配列の使い方
    name = ["たんじろう","ぎゆう","ねずこ","むざん"]
    
    name.append("ぜんいつ")
    print('3 配列の使い方',name)
    
    
    # ４ for文の使い方
    for data in name:
        print('4 for文の使い方',data)
    
    
    # ５ 関数の使い方
    print('5 関数の使い方', test())


    # ６ 引数を使う関数の使い方
    test2(name, 'れんごく')
    test2(name, 'ぎゆう')

if __name__ == '__main__':
    main()
    
