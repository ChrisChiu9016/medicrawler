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
    f1 = open("dict/total.txt", "r", encoding="utf-8")
    f2 = open("dict/commonNews.txt", "r", encoding="utf-8")

    txt1 = f1.read()
    txt2 = f2.read()

    f1.close()
    f2.close()

    line1 = txt1.split("\n")
    line2 = txt2.split("\n")

    outfile1 = open("dict/f_diff.txt", 'w', encoding="utf-8")
    outfile2 = open("dict/f_same.txt", 'w', encoding="utf-8")
    #過濾掉1.txt跟2.txt相同的詞
    for i in line1:
        if i.split(',')[0] not in line2:
            outfile1.write(i)
            outfile1.write("\n")
        else:
            outfile2.write(i)
            outfile2.write('\n')
    outfile1.close()
    outfile2.close()

if __name__ == "__main__":
    # crawl_url()
    decrease()

