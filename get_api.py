import simplejson,requests
import sys
import csv

url = "https://dapi.kakao.com/v2/local/search/category.json"
headers = {"Authorization":"KakaoAK "} #이곳에 키 입력
category_name='' #이곳에 카테고리 코드입력

file=open('.csv','w',encoding='utf-8',newline='') #이곳에 파일명 입력
document_list=['id','place_name','category_name','category_group_code','category_group_name','phone','address_name','road_address_name','x','y','place_url','distance']
wr=csv.DictWriter(file,fieldnames=document_list)
wr.writeheader()

xinc=(126.99165617728882-126.96449264899856)/25
yinc=(37.58186344028994-37.55974571895999)/25
#충정로역에서 창덕궁까지의 사각형범위를 잘게 나누어 조사함(카카오에서 한번에 45개까지의 장소만 제공하므로)

for i in range(30):
    lx=126.96449264899856
    ly=37.55974571895999+yinc*i
    rx=lx+xinc
    ry=ly+yinc
    for j in range(30):
        page=1
        params={'category_group_code':category_name,'rect':f'{lx},{ly},{rx},{ry}','page':page}
        places=requests.get(url,params=params,headers=headers).json()['documents']
        total=requests.get(url,params=params,headers=headers).json()['meta']['total_count']
        if total==0:
            lx=rx
            rx=lx+xinc
            continue
        while(1):
                for k in range(15):
                    try:
                        wr.writerows([places[k]])
                    except IndexError:
                        break
                if (requests.get(url,params=params,headers=headers).json()['meta']['is_end'] or page==3):
                        break
                else:
                    page+=1
                    params={'category_group_code':category_name,'rect':f'{lx},{ly},{rx},{ry}','page':page}
                    places=requests.get(url,params=params,headers=headers).json()['documents']

        lx=rx
        rx=lx+xinc

file.close()