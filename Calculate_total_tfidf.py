import os

from pyparsing import Keyword

def calc_total():
    files = os.listdir('keywords/')
    dict = {}
    cnt = {}
    for file in files:
        try:
            with open('keywords/'+file, "r", encoding="utf-8") as f:
                content = f.readlines()
                for line in content:
                    keyword = line.split(',')[0]
                    value  = line.split(',')[1].replace('\n', '')
                    if keyword not in cnt:
                        cnt.update({keyword: 1})
                    else:
                        cnt[keyword] = int(cnt[keyword]) + 1
                    if keyword in dict:
                        dict[keyword] = float(dict[keyword]) + float(value)
                    else:
                        dict.update({keyword : value})
                print(file, " done!")
        except:
            continue
    with open('dict/jieba-TFIDF/count_news.txt', 'w', encoding='utf-8') as nf:
        dict = sorted(dict.items(), key=lambda x: float(x[1]), reverse=True)
        for key in dict:
            if float(key[1]) > 1.0:
                nf.write(key[0].replace("'", '') + ' ' + str(float(key[1])/cnt.get(key[0])) + ' ' + str(cnt.get(key[0]))+'\n')
    print("all done!")

if __name__ == "__main__":
    calc_total()