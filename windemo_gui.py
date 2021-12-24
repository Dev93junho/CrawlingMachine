#-*- coding:utf-8 -*-
import sys
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *
from bs4 import BeautifulSoup
import urllib.request
import numpy as np
# from tqdm import trange, notebook
import pandas as pd
# import requests


class Application(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(400,250,300,400)
        self.setWindowTitle("data_scrapper_demo")
        self.setWindowIcon(QIcon("icon.png"))
        

        btn = QPushButton("Download", self)
        btn.move(97, 350)
        btn.clicked.connect(self.scrappy)
    
    def scrappy(self):
        page_url = input
        # soup = BeautifulSoup(html_doc, 'html.parser')


        page_url = 'https://www.lawmaking.go.kr/opnPtcp/nsmLmSts/out?pageIndex=' # main page scrap
        # details = 'https://www.lawmaking.go.kr/opnPtcp/nsmLmSts/out/{lawnum}/detailRP' # details scrap
        data=[]

        for no in range(1, 76):
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
<<<<<<< HEAD

        # Data framing
        X= np.array(data).reshape(-1, 6)
        for i in X:
            # get lawnum
            # details = 'https://www.lawmaking.go.kr/opnPtcp/nsmLmSts/out/{lawnum}/detailRP' # details scrap
            # url open
            # i.append(<pre>)
        
        df = pd.DataFrame(X)
=======

        # Data framing
        X= np.array(data).reshape(-1, 6)
        for i in X:
            # get lawnum
            # details = 'https://www.lawmaking.go.kr/opnPtcp/nsmLmSts/out/{lawnum}/detailRP' # details scrap
            # url open
            # i.append(<pre>)
        
        df = pd.DataFrame(X)

>>>>>>> 41dbc94280acd3a3de618b2660be49915b571cd6

        # change the order
        df.columns = ['의안명','발의의원', '상임위', '국회현황', '의결결과','의안번호']
        final = df[['의안번호', '국회현황','발의의원','의안명','의결결과','상임위']] # need to add details columns
        final.to_excel("result.xlsx", encoding = 'cp949')




app = QApplication(sys.argv)
window = Application()
window.show()
app.exec_()
