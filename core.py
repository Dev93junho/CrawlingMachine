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
import json
import pandas as pd
import numpy as np
import math

# searched & scrapped all tag components in the url
def url_search(input):
    # initialize
    url = input
    data_tmp = []
    
    f = urllib.request.urlopen(url)
    source = f.read()

    #list_rowcol = get_num_rowcol(url)

    #start the soup
    soup = BeautifulSoup(source, "html.parser")
    table = soup.find_all(['tb', 'table'])
    ### table = soup.select('table') # table tag scrap
    string = soup.find_all(['p'])
    ### string = soup.select('p') # p tag scrap

    data_tmp = table, string

    return data_tmp

'''
start the filtering to material blocks
'''

# filtered table tag and make drag&drop block
def table_scrappy(data):
    ### tables is url_search(url)[0] ###
    table_html = data[0]

    ### return list of table tag
    result = json.dumps([str(x.text) for x in table_html if x!=""], ensure_ascii=False)
    
    return result

# filtered tag about string and make drag&drop block
def str_scrappy(data):
    ### tables is url_search(url)[1] ###
    str_html = data[1]

    ### return list of p tag
    result = json.dumps([str(x.text) for x in str_html if x!=""], ensure_ascii=False)

    return result

#get num of row&column
def table_scrappy_mk2(input):
    url = input
    df = pd.read_html(url)
    
    result = []

    for i in df:
        row = len(i)

        # result.append({'row':row,'col':col,'text':[[i[x][n] for x in i] for n in range(row)]})
        result.append([{x:'' if pd.isna(i[x][n]) else str(i[x][n]) for x in i} for n in range(row)])
    
    result = json.dumps(result, ensure_ascii=False)
    return result

#print(table_scrappy_mk2("https://www.lawmaking.go.kr/opnPtcp/nsmLmSts/out?pageIndex=1"))