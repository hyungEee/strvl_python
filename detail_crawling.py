#기본 api에서 제공하지 않는 휠체어가능여부, 동물출입가능여부, 키워드, 별점정보를 가져오는 코드이다.

import selenium
from selenium import webdriver
import time
import pandas as pd
from bs4 import BeautifulSoup

driver=webdriver.Chrome("C:\chromedriver_win32\chromedriver.exe")

file=pd.read_csv('.csv') #이곳에 입력파일
url=file['place_url']
wheelchair=[]
animal=[]
keyword=[]
rate_count=[]
rate=[]

for i in range (file.shape[0]):
    driver.get(url[i])
    time.sleep(2)
    try:
        driver.find_element_by_css_selector("#mArticle > div.cont_essential > div.details_placeinfo > div.placeinfo_default.placeinfo_facility > ul > li:nth-child(4) > span.ico_comm.ico_handicapped")
        wheelchair.append("y")
    except:
        try:
            driver.find_element_by_css_selector("#mArticle > div.cont_essential > div.details_placeinfo > div.placeinfo_default.placeinfo_facility > ul > li:nth-child(4) > span.ico_comm.ico_nohandicapped")
            wheelchair.append("n")
        except:
            wheelchair.append("unknown")
    try:
        driver.find_element_by_css_selector("#mArticle > div.cont_essential > div.details_placeinfo > div.placeinfo_default.placeinfo_facility > ul > li:nth-child(2) > span.ico_comm.ico_animal")
        animal.append("y")
    except:
        try:
            driver.find_element_by_css_selector("#mArticle > div.cont_essential > div.details_placeinfo > div.placeinfo_default.placeinfo_facility > ul > li:nth-child(2) > span.ico_comm.ico_noanimal")
            animal.append("n")
        except:
            animal.append("unknown")
            
    html=driver.page_source
    soup=BeautifulSoup(html,'html.parser')
    
    try:
        element=soup.select('#mArticle > div.cont_essential > div.details_placeinfo > div:nth-child(5) > div > div > span > a')
        text=""
        for e in element:
            text=text+e.text+" "
        keyword.append(text)
    except:
        keyword.append("")

    try:
        element=soup.select_one('#mArticle > div.cont_evaluation > strong > span').text
        rate_count.append(element)
    except:
        rate_count.append("0")
        rate.append("0")
        continue
    try:
        element=soup.select_one('#mArticle > div.cont_evaluation > div.ahead_info > div > em').text
        rate.append(element)
    except:
        rate.append("0")

df=pd.DataFrame({'wheelchair':wheelchair,'animal':animal,'keyword':keyword,'rate_count':rate_count,'rate':rate})
df_concat=pd.concat([file,df],axis=1)
df_concat.to_csv('.csv',index=False) #이곳에 출력파일