from bs4 import BeautifulSoup
import requests
import Algorithmia
from matplotlib import pyplot as plt 
import numpy as np 


#---main function here#
def pl_draw():
    #----here------
    #a='Taylor swift'
    a=input("Enter the artist name: ")
    i=input("Enter the artist's song: ")

    def test(a,sng):
        try:
            url='https://www.azlyrics.com/lyrics/'
            aa=a.replace(' ', '')
            bb=sng.replace(' ', '')

            url=url+aa+'/'+bb+'.html'

            web_page=requests.get(url)
            soup=BeautifulSoup(web_page.content, 'html.parser')


            lyrics = soup.find_all("div", attrs={"class":None, "id":None})

            def supify(lyrics):
                    for i in lyrics:
                        i.replace('\n','')
                        return i
                        break
            if lyrics:
                lyrics=[x.get_text() for x in lyrics]
                #print(lyrics)


            else:
                print("No results found")
            s=supify(lyrics)

            s1=s.replace('\n','. ')
            ninput=s1.replace('\r','')
            def algo(ninput):
                client = Algorithmia.client('simMpB7sihn++27HzwRr0dO95f41')
                algo = client.algo('nlp/SocialSentimentAnalysis/0.1.4')
                algo.set_options(timeout=300) # optional
                return algo.pipe(ninput).result[0]

            def auto_tag(ninput):
                client = Algorithmia.client('simMpB7sihn++27HzwRr0dO95f41')
                algo = client.algo('nlp/AutoTag/1.0.1')
                algo.set_options(timeout=300) # optional
                return algo.pipe(ninput).result

            auto=auto_tag(ninput)

            asa= algo(lyrics)
            lst=[]
            #lst.append(asa['compound'])
            lst.append(asa['negative'])
            lst.append(asa['neutral'])
            lst.append(asa['positive'])

            nlist=['negative','neutral','positive']
            explode = (0, 0, 0.1)  # only "explode" the 2nd slice (i.e. 'Hogs')

            
            

            #print(s)
            fig = plt.figure(figsize =(10, 7)) 
            plt.pie(lst, labels = nlist, explode=explode, autopct='%1.1f%%', shadow=True, startangle=90) 
            plt.title(sng.upper())
            plt.show()
            #for i in auto:
            #    final_list.append(i)
        except:
            print("Song not available")
    #print(auto)
    #for i in songus[0:2]:
    #    test(a.lower(),i.lower())
    def draw_fun(a,i):
        test(a.lower(), i.lower())

    draw_fun(a,i)

if __name__ == "__main__":
    pl_draw()  


