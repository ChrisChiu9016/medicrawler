import requests as rq
from bs4 import BeautifulSoup as soup


file_name       = "chinatimes.txt"
headers         = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'}

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
    while(1):
        current_url = url + str(i)
        
    pass

if __name__ == "__main__":
    # crawl_url()
    crawl_content()