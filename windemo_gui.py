#-*- coding:utf-8 -*-
import sys
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *
from bs4 import BeautifulSoup
from multiprocessing import Pool, Process, Queue, Manager
import multiprocessing as mp
import urllib.request
import numpy as np
# from tqdm import trange, notebook
import pandas as pd
# import requests
import time # record run time



class Application(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        self.start = QLineEdit(self)
        self.start.setText('')

        self.end = QLineEdit(self)
        self.end.setText('')

        btn = QPushButton(self)
        btn.setText("Download")
        btn.clicked.connect(self.scrappy)
    
        grid = QGridLayout()
        grid.addWidget(QLabel('s:'),0,0)
        grid.addWidget(QLabel('e:'),1,0)
        grid.addWidget(self.start,0,1)
        grid.addWidget(self.end,1,1)
        grid.addWidget(btn,2,0,2,1)
        
        self.setLayout(grid)
        self.setWindowTitle("data_scrapper_demo")
        self.setWindowIcon(QIcon("icon.png"))
        self.show()
    

    def scrappy(self):
        page_url = input
        # soup = BeautifulSoup(html_doc, 'html.parser')
        start = time.time()


        page_url = 'https://www.lawmaking.go.kr/opnPtcp/nsmLmSts/out?pageIndex=' # main page scrap
        # details = 'https://www.lawmaking.go.kr/opnPtcp/nsmLmSts/out/{lawnum}/detailRP' # details scrap
        data=[]

        s = int(self.start.text())
        e = int(self.end.text())+1

        for no in range(s, e):
            url = page_url + str(no)
            f = urllib.request.urlopen(url)
            source = f.read()
            
            # start the soup for page scrap
            soup = BeautifulSoup(source, "html.parser")
            tables=soup.select('table', encoding = 'cp949') # fixed html tag

            table_html = str(tables)
            table_df_list = pd.read_html(table_html, encoding = 'cp949') # LIST type
            table_df_list[0]['의안번호(대안번호)'] = table_df_list[0]['의안번호(대안번호)'].astype(str)
            add_list = table_df_list[0]
            data.append(add_list)

        # Data framing
        X= np.array(data).reshape(-1, 6)
        X= np.insert(X,6,values='', axis=1)

        for i in range(len(X)):
            # get lawnum
            lawnum = X[i][5]
            if ' ' in lawnum:
                lawnum = lawnum[:lawnum.find(' ')]
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
    
        print("경과시간 : ", time.time() - start)

if __name__ == '__main__':
    manager = Manager()
    pool = Pool(processes=4)
    app = QApplication(sys.argv)
    window = Application()
    window.show()
    sys.exit(app.exec_())
