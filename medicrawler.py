import requests as rq
from bs4 import BeautifulSoup as soup
import io
import sys
import time

file_name       = "chinatimes.txt"
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36'}

'''
https://pansci.asia/archives/tag/醫學/page/1
https://www.chinatimes.com/Search/健康?page=2&chdtv
https://udn.com/api/more?page=1&id=search:醫療&channelId=2&type=searchword&last_page=2667
'''

def crawl_url():
    url = "https://www.chinatimes.com/Search/醫療?page="
    # fetch link in page
    with open(file_name, "a", encoding="utf-8") as f:
        i = 1
        while(1):
            current_url = url + str(i) + "&chdtv"
            res = rq.get(current_url, headers=headers)
            html = soup(res.content, "html.parser")

            titles = html.find_all("h3", class_="title")
            print(len(titles))
            if len(titles) > 0:
                for title in titles:
                    f.write(title.a.get("href") + "\n")
            else:
                break

            i += 1
    f.close()
    print(f"crawl complete! with {i-1} lines write to {file_name}")

def crawl_content():
    with open("chinatimes.txt", "r", encoding="utf-8") as f:
        i = 1
        for line in f:
            target_url = line

            try:
                res = rq.get(target_url, headers=headers)
                html = soup(res.content, "html.parser")
                contents = html.find("div", class_="article-body").find_all("p")
            except:
                continue
            
            target_file_name = "chinatimes/" + str(i) + ".txt"
            with open(target_file_name, "w", encoding="utf-8") as output:
                for content in contents:
                    output.write(content.getText().replace('"', ''))
            output.close()

            print(f"create file {i}.txt successfully.")
            i += 1
    
    f.close()

def crawl_qna():
    url = 'https://sp1.hso.mohw.gov.tw/doctor/All/history.php?UrlClass=%AEa%C2%E5%AC%EC&SortBy=q_no&PageNo='
    i = 1
    j = 1
    while(1):
        current_url = url + str(i)
        try:
            res = rq.get(current_url, headers=headers)
            html = soup(res.text.encode('iso-8859-1').decode('big5'), "html.parser")
            title = html.find("div", class_="main").find_all("a")

            if len(title) == 0:
                break
            for index in range(1, len(title) - min(2, i)):
                output_file = open(f'q&a/{j}.txt', 'w', encoding='big5')
                link = 'https://sp1.hso.mohw.gov.tw/doctor/All/' + title[index-1].get('href')

                res = rq.get(link, headers=headers)
                body = soup(res.content, "html.parser")
                contents = body.find_all('div', class_='msg')

                p = []
                for content in contents:
                    p.append(content.div.getText().strip().replace(' ', '').replace('\r', '').replace('\n', '').replace(u'\u3000', '').replace(u'\xa0', ''))

                try:
                    output_file.write(' '.join(p))
                    print(p)
                except:
                    continue
                # print(p)
                time.sleep(1)
                output_file.close()
                j += 1
        except:
            pass
        i = i + 1

    print("all done!")

if __name__ == "__main__":
    crawl_qna()