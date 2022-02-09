import jieba
import jieba.analyse
import os
import math

def tfidf():
    # jieba.load_userdict('.\dict\\user_dict.txt')
    post = os.listdir('.\chinatimes')
    for i in range(1, len(post)):
        try:
            path = '.\chinatimes\\' + str(i) + ".txt"
            new_file = ".\keywords_cus\\" + str(i) + ".txt"
            
            with open(path, "r", encoding="utf-8") as f:
                content = f.readline()
                
                keywords = jieba.analyse.extract_tags(content, topK=20, withWeight=True, allowPOS=('n')) # 只抓名詞
                with open(new_file, "w", encoding="utf-8") as nf:
                    for item in keywords:
                        nf.write(item[0]+","+str(item[1])+"\n")
                nf.close()
            f.close()
            print(f"parse file {i}.txt successfully.")
        except:
            continue
    print("done!")

def idf():
    outstr = []
    # load user dictionary
    # jieba.load_userdict('.\dict\\dictionTest.txt')

    # load stopwords
    stop_words = []
    with open('dict/stopword.txt', 'r', encoding='utf-8') as f:
        stop_words = [stop_word.strip() for stop_word in f.readlines()]
    # 列出檔案路徑
    post = os.listdir('.\chinatimes')
    for i in range(1, 20000):
        try:
            path = '.\chinatimes\\' + str(i) + ".txt"
            new_file = ".\keywords_cus\\" + str(i) + ".txt"

            with open(path, "r", encoding="utf-8") as f:
                # 讀入文章
                content = f.readline()
                # 進行斷詞
                content_seg = jieba.cut(content.strip())
                # 去除停止詞
                for word in content_seg:
                    if word not in stop_words and word != ' ':
                        outstr.append(word)
            f.close()
            print(f"parse file {i}.txt successfully.")
        except:
            continue

    # 計算出現次數
    all_dict = {}
    for word in outstr:
        num = all_dict.get(word, 0)
        all_dict[word] = num + 1
    # 計算 idf
    idf_dict = {}
    iwf_dict = {}
    for key in all_dict:
        w = key
        p = '%.10f' % (math.log10(len(post)/all_dict[key]+1))
        q = '%.10f' % (math.log10(len(outstr)/all_dict[key]))
        if w > u'\u4e00' and w <= '\u9fa5':
            idf_dict[w] = p
            iwf_dict[w] = q
    with open('idf_dict.txt', 'w', encoding='utf-8') as f:
        sorted_dict = sorted(
            idf_dict.items(), key=lambda x: x[1])
        for k in sorted_dict:
            if k != '\n':
                f.write(k[0] + ' ' + k[1] + '\n')
    with open('iwf_dict.txt', 'w', encoding='utf-8') as f:
        sorted_dict = sorted(
            iwf_dict.items(), key=lambda x: x[1], reverse=True)
        for k in sorted_dict:
            if k != '\n':
                f.write(k[0] + ' ' + k[1] + '\n')

if __name__ == "__main__":
    idf()