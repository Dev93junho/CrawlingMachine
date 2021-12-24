'''
1. this is scrappy API for HTML document
2. Configurated for table, img, str scrap
3. url input and scrapping all html structure
4. distribute data to other module
5. table_scp is display table tag
6. string_scp is display p tag
** Created by JHShin in Oct.2021 **
** Updated by BSKang since Nov.2021 **
'''

# from flask_restful import Api,Resource,reqparse

from bs4 import BeautifulSoup
import urllib.request
import pandas as pd
import numpy as np

def scrappy():
    page_url = input
    # soup = BeautifulSoup(html_doc, 'html.parser')


    page_url = 'https://www.lawmaking.go.kr/opnPtcp/nsmLmSts/out?pageIndex=' # main page scrap
    # details = 'https://www.lawmaking.go.kr/opnPtcp/nsmLmSts/out/{lawnum}/detailRP' # details scrap
    data=[]

    for no in range(1, 2):
        url = page_url + str(no)
        f = urllib.request.urlopen(url)
        source = f.read()
        
        # start the soup for page scrap
        soup = BeautifulSoup(source, "html.parser")
        tables=soup.select('table', encoding = 'cp949') # fixed html tag

        table_html = str(tables)
        table_df_list = pd.read_html(table_html, encoding = 'cp949') # LIST type

        add_list = table_df_list[0]
        data.append(add_list)

    # Data framing
    X= np.array(data).reshape(-1, 6)
    X= np.insert(X,6,values='', axis=1)

    for i in range(len(X)):
        # get lawnum
        lawnum = X[i][5]
        details = f'https://www.lawmaking.go.kr/opnPtcp/nsmLmSts/out/{lawnum}/detailRP' # details scrap
        # url open
        details_f = urllib.request.urlopen(details)
        details_source = details_f.read()
        details_soup = BeautifulSoup(details_source, "html.parser")
        pre = details_soup.select('pre', encoding = 'cp949')[0].text

        X[i][6]=pre 
        
    df = pd.DataFrame(X)

    # change the order
    df.columns = ['의안명','발의의원', '상임위', '국회현황', '의결결과','의안번호','주요내용']
    final = df[['의안번호', '국회현황','발의의원','의안명','의결결과','상임위','주요내용']] # need to add details columns
    final.to_excel("result.xlsx", encoding = 'cp949')

scrappy()