from re import T
import requests as rq
import jieba
from jieba import analyse
from bs4 import BeautifulSoup as soup

file_name = "chinatimes.txt"
header = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'}

'''
https://pansci.asia/archives/tag/醫學/page/1
https://www.chinatimes.com/Search/健康?page=2&chdtv
https://udn.com/api/more?page=1&id=search:醫療&channelId=2&type=searchword&last_page=2667
'''


def news():
    # 中時即時新聞
    url = 'https://www.chinatimes.com/search/生活?page='
    article_holder = []
    stopwords = []
    with open('dict/stopword.txt', 'r', encoding='utf-8') as f:
        stopwords = [stopword.strip() for stopword in f.readlines()]
    f.close()
    # 抓取20000篇普通新聞
    for i in range(1, 1000):
        current_url = url + str(i) + "&chdtv"
        res = rq.get(current_url, headers=header)
        html = soup(res.content, "html.parser")
        titles = html.find_all("h3", class_="title")
        if len(titles) > 0:
            for title in titles:
                try:
                    current_url = title.a.get("href")
                    print(current_url)
                    res = rq.get(current_url, headers=header)
                    html = soup(res.content, "html.parser")
                    contents = html.find("div", class_="article-body").find_all("p")
                    tmp = ''
                    for content in contents:
                        tmp += content.getText().replace('"', '').strip()
                        
                    article_holder.append(tmp)
                except:
                    continue
        else:
            break
    # 儲存文章內容
    with open ("news.txt", 'w', encoding='utf-8') as f:
        for item in article_holder:
            f.write(item+'\n')
    f.close()

    all_dict = []
    for article in article_holder:
        content_seg = jieba.cut(article.strip())
        for word in content_seg:
            if word not in stopwords:
                if word != '\n' and word != '\t' and word != ' ':
                    all_dict.append(word)

    with open('dict/commonNews.txt', 'w', encoding='utf-8') as f:
        for item in all_dict:
            f.write(item+'\n')
    f.close()

    # temp_dict = {}
    # cnt_dict = {}
    # all_dict = {}
    # 計算TF-IDF
    # total_len = len(article_holder)
    # for article in article_holder:
    #     keywords = analyse.extract_tags(article, topK=20, withWeight=True, allowPOS=('n','nr','ns','v','vn'))
    #     for item in keywords:
    #         keyword = item[0]
    #         weight = item[1]
    #         temp_dict[keyword] = temp_dict.get(keyword, 0.0) + weight
    #         cnt_dict[keyword] = cnt_dict.get(keyword, 0) + 1
    # 計算平均
    # for item in temp_dict:
    #     keyword = item[0]
    #     weight = item[1]
    #     all_dict[keyword] = '%.10f' % (temp_dict.get(keyword) / cnt_dict.get(keyword))

    print("complete!.")

def decrease():
    file1 = 'dict/TfidfVectorizer/qna_voc_1_3_None_(1, 1).txt'
    file2 = "dict/jieba-TFIDF/count_qna.txt"
    with open(file1, "r", encoding="utf-8") as f1, open(file2, "r", encoding="utf-8") as f2:
        temp1 = f1.readlines()
        temp2 = f2.readlines()
        set1 = []
        set2 = []
        for x in temp1:
            set1.append(x.split(' ')[0])
        for x in temp2:
            set2.append(x.split(' ')[0])
        f1.close()
        f2.close()

    f = open('dict/TfidfVectorizer/not_in_model.txt', 'w', encoding='utf-8')
    for word in set2:
        if word not in set1:
            f.write(word+'\n')
    f.close()
    
    # f = open('dict/TfidfVectorizer/100-200.txt', 'w', encoding='utf-8')
    # for word in set2:
    #     if word not in set1:
    #         f.write(word+'\n')
    # f.close()

if __name__ == "__main__":
    # crawl_url()
    decrease()

