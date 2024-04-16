import time
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import pyperclip


class NaverCafe:


    def __init__(self, name, clubid):
        self.name = name
        self.clubid = clubid
        self.driver = Chrome()
        self.driver.get(f"https://cafe.naver.com/{name}")
        
        
    def enter_id_pw(self, userid, userpw):
        self.driver.get('https://nid.naver.com/nidlogin.login')
        
        div_id = self.driver.find_element(By.ID, 'id')
        div_id.click()
        pyperclip.copy(userid)
        div_id.send_keys(Keys.CONTROL, 'v')

        div_pw = self.driver.find_element(By.ID, 'pw')
        div_pw.click()
        pyperclip.copy(userpw)
        div_pw.send_keys(Keys.CONTROL, 'v')

        self.driver.find_element(By.ID, 'log.login').click()
        
        
    def articleboard(self, menuid):
        boardtype = 'L'
        userDisplay = 50
        pageurl = f"https://cafe.naver.com/{self.name}?iframe_url=/ArticleList.nhn%3Fsearch.clubid={self.clubid}%26search.boardtype={boardtype}%26search.menuid={menuid}%26search.marketBoardTab=D%26search.specialmenutype=%26userDisplay={str(userDisplay)}"
        self.driver.get(pageurl)
        self.driver.switch_to.frame("cafe_main")
        html = self.driver.page_source
        soup = BeautifulSoup(html,'html.parser')
        prev_next = self.driver.find_elements(By.XPATH, "//div[@class='prev-next']/a")
        df = pd.DataFrame()
        pages = []
        for page in prev_next:
            pages.append(int(page.text))
        df = pd.DataFrame(columns=['rowheadings', '제목', '작성자', '작성일', '조회', '좋아요'])

        for page in pages:
            #print("page:", page)
            pageurl = f"https://cafe.naver.com/{self.name}?iframe_url=/ArticleList.nhn%3Fsearch.clubid={self.clubid}%26search.menuid={menuid}%26userDisplay={str(userDisplay)}%26search.boardtype={boardtype}%26search.specialmenutype=%26search.totalCount=62%26search.cafeId=30853297%26search.page={str(page)}"
            
            self.driver.get(pageurl)
            time.sleep(3)
            self.driver.switch_to.frame("cafe_main")
            html = self.driver.page_source
            soup = BeautifulSoup(html,'html.parser')
            inner_number = self.driver.find_elements(By.CLASS_NAME, 'inner_number')
            num_inner_number = len(inner_number)
            #print(num_inner_number)
            article = self.driver.find_elements(By.CLASS_NAME, 'article')
            num_articles = len(article)
            offset = num_articles - num_inner_number
            pnick = self.driver.find_elements(By.CLASS_NAME, 'p-nick')
            tddate = self.driver.find_elements(By.CLASS_NAME, 'td_date')
            td_view = self.driver.find_elements(By.CLASS_NAME, 'td_view')
            td_likes = self.driver.find_elements(By.CLASS_NAME, 'td_likes')
            
            for i in range(num_inner_number):
                df.loc[len(df)] = [
                    inner_number[i].text, 
                    article[i + offset].text,
                    pnick[i + offset].text,
                    tddate[i + offset].text,
                    td_view[i + offset].text,
                    td_likes[i + offset].text
                ]
        return df
        
    
    def comments(self, articleid):
        article_url = f'https://cafe.naver.com/{self.name}/{str(articleid)}'
        self.driver.get(article_url)
        time.sleep(3)
        self.driver.switch_to.frame("cafe_main")
        bs = BeautifulSoup(self.driver.page_source,'html.parser')
        comment_nickname = self.driver.find_elements(By.CLASS_NAME, 'comment_nickname')
        text_comment = self.driver.find_elements(By.CLASS_NAME, 'text_comment')
        comment_info_date = self.driver.find_elements(By.CLASS_NAME, 'comment_info_date')
        df = pd.DataFrame(columns=['닉네임', '댓글', '작성일시'])
        for i in range(len(comment_nickname)):
            df.loc[i] = [comment_nickname[i].text, text_comment[i].text, comment_info_date[i].text]
        
        return df
