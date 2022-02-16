from http.client import ImproperConnectionState
from pydoc import doc
import jieba
import jieba.analyse
import os
import math
import re
from numpy import vectorize
from sklearn.feature_extraction.text import TfidfVectorizer

def tfidf():
    # load user_dict
    jieba.load_userdict('./dict/dict_big.txt')
    # load stopwords
    stop_words = []
    with open('dict/stopword.txt', 'r', encoding='utf-8') as f:
        stop_words = [stop_word.strip() for stop_word in f.readlines()]
    f.close()
    # list document
    document = os.listdir('chinatimes/')
    print(len(document))
    for doc in document:
        try:
            with open('chinatimes/'+doc, "r", encoding="utf-8") as f:
                content = f.readline()
                
                keywords = jieba.analyse.extract_tags(content, topK=20, withWeight=True, allowPOS=('v','n')) # 只抓名詞
                with open("keywords/"+doc, "w", encoding="utf-8") as nf:
                    for item in keywords:
                        if item[0] not in stop_words:
                            nf.write(item[0]+","+str(item[1])+"\n")
                nf.close()
            f.close()
            print(f"parse file {doc}.txt successfully.")
        except:
            continue
    print("done!")

def tfiwf():
    # load user_dict
    jieba.load_userdict('./dict/dict_big.txt')
    # load stopwords
    stop_words = []
    with open('dict/stopword.txt', 'r', encoding='utf-8') as f:
        stop_words = [stop_word.strip() for stop_word in f.readlines()]
    f.close()
    outstr = []
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

def qna_idf():
    # load user_dict
    jieba.load_userdict('./dict/dict_big.txt')
    # load stopwords
    stop_words = []
    with open('dict/stopword.txt', 'r', encoding='utf-8') as f:
        stop_words = [stop_word.strip() for stop_word in f.readlines()]
    f.close()
    # list document
    sentences = []
    files = os.listdir('q&a/')

    result = re.compile(r'(http|https)://[a-zA-Z0-9.?/&=:]*', re.S)

    for file in files:
        f = open('q&a/'+file, 'r', encoding='Big5')
        content = f.readline()
        # 去除網址
        sentence = result.sub('', content)
        sentences.append(sentence)
        print(f'load {file}.')
        f.close()
    # 由於原工具是為英文設計，所以必須在句子中加上空格
    document = [' '.join(jieba.cut(sent)) for sent in sentences]
    # 相關參數設定
    max_df = 1.0
    min_df = 3
    max_features = None
    ngram_range = (1, 2)
    # 匹配非數字開頭的詞，允許兩個字詞形成詞組，上限5000個詞
    vectorizer = TfidfVectorizer(
        token_pattern=r'(?u)\b[A-Za-z\u4e00-\u9fa5]{2,}\b',
        ngram_range=ngram_range,
        stop_words=stop_words,
        max_features=max_features,
        max_df=max_df,
        min_df=min_df,
    ).fit(document)

    result = vectorizer.transform(document)
    word = vectorizer.get_feature_names_out()
    with open(f'dict\TfidfVectorizer\qna_voc_{max_df}_{min_df}_{max_features}_{str(ngram_range)}.txt', 'w', encoding='utf-8') as f:
        for key, value in sorted(vectorizer.vocabulary_.items(), key=lambda x: x[1]):
            keyword = key.strip()
            if keyword not in stop_words:
                f.write(keyword + ' ' + str(value) + '\n')
    f.close()

    print('all done!')

if __name__ == "__main__":
    qna_idf()