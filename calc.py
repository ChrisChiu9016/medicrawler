import os

def calc_total():
    files = os.listdir('.\keywords_cus\\')
    dict = {}
    for i in range(1, len(files)):
        try:
            path = '.\keywords_cus\\' + str(i) + ".txt"
            
            with open(path, "r", encoding="utf-8") as f:
                content = f.readlines()
                for line in content:
                    keyword = line.split(',')[0]
                    value  = line.split(',')[1].replace('\n', '')
                    print(keyword, value)
                    if keyword in dict:
                        dict[keyword] = float(dict[keyword]) + float(value)
                    else:
                        dict.update({keyword : value})
                print(path, " done!")
        except:
            continue
    with open('total_cus.txt', 'w', encoding='utf-8') as nf:
        dict = sorted(dict.items(), key=lambda x: float(x[1]), reverse=True)
        for key in dict:
            if float(key[1]) > 1.0:
                nf.write(key[0].replace("'",'')+' '+str(key[1])+'\n')
    print("done!")

if __name__ == "__main__":
    calc_total()