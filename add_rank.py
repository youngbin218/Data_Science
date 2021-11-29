# 팀 성적에는 없던 순위 가져오기
import numpy as np
import pandas as pd
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from html_table_parser import parser_functions as parser
from selenium.webdriver.support.select import Select

# 2001 ~ 2021 팀 성적 csv 불러오기
file = []
year_record = []

for i in range(2001, 2022):
    file.append('./' + str(i) + '.csv')
    
for f in file:
    year_record.append(pd.read_csv(f))

# 드라이버 객체
driver = webdriver.Chrome(executable_path='D:/conda/chromedriver.exe')
    
# KBO 기록실 URL
URL = "https://www.koreabaseball.com/TeamRank/TeamRank.aspx"

driver.get(url=str(URL))

for i in range(2001, 2022):
    select_tag = Select(driver.find_element_by_id("cphContents_cphContents_cphContents_ddlYear"))
    select_tag.select_by_value(str(i))
    
    time.sleep(2)
    
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    record_table = soup.find('table') #div#cphContents_cphContents_cphContents_udpRecord table')
    data = parser.make2d(record_table)
    df = pd.DataFrame(data[1:], columns=data[0])
    df = df.drop(['승률', '경기', '승', '패', '무', '게임차' ,'최근10경기', '연속', '홈', '방문'], axis=1)
    year_record[i-2001] = pd.merge(year_record[i-2001], df, on='팀명')
    year_record[i-2001].to_csv('./' + str(i) + '_new.csv', index=False)

driver.close()
