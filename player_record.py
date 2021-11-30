# KBO 기록실에서 연도별 선수 성적 크롤링
import numpy as np
import pandas as pd
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from html_table_parser import parser_functions as parser
from selenium.webdriver.support.select import Select

# Query 변수
sort_list = {"HitterBasic" : "BasicOld", "PitcherBasic" : "BasicOld"}
team_list = {"두산" : "OB", "롯데" : "LT", "삼성" : "SS", "키움" : "WO", "한화" : "HH",
             "KIA" : "HT", "KT" : "KT", "LG" : "LG", "NC" : "NC", "SSG" : "SK"}

# 2018 ~ 2021 선수 성적
kbo_list = list(np.arange(2019, 2022))
year_record = []

for record in kbo_list:
    record = pd.DataFrame()
    year_record.append(record)
    
for i in range(0, len(sort_list)):
    # 드라이버 객체
    driver = webdriver.Chrome(executable_path='D:/conda/chromedriver.exe')
    
    # KBO 기록실 URL
    part_URL = "https://www.koreabaseball.com/Record/Player/"
        
    # 각 기록별 URL
    part_URL += list(sort_list.keys())[i] + "/" + list(sort_list.values())[i] + ".aspx"
    
    driver.get(url=str(part_URL))
    
    select_tag = Select(driver.find_element_by_id("cphContents_cphContents_cphContents_ddlSeries_ddlSeries"))
    select_tag.select_by_value(str(0))
        
    time.sleep(2)
    
    for j in range(0, 3):   
        select_tag = Select(driver.find_element_by_id("cphContents_cphContents_cphContents_ddlSeason_ddlSeason"))
        select_tag.select_by_value(str(kbo_list[j]))
        
        time.sleep(2)
        
        for k in range(0, 10):
            select_tag = Select(driver.find_element_by_id("cphContents_cphContents_cphContents_ddlTeam_ddlTeam"))
            select_tag.select_by_value(list(team_list.values())[k])

            time.sleep(2)
            
            button = driver.find_elements_by_xpath('//*[@id="cphContents_cphContents_cphContents_udpContent"]/div[2]/div[2]/a[1]')[0]
            button.click()
            
            time.sleep(2)

            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            record_table = soup.find_all('table')
            data = parser.make2d(record_table[0])
            df = pd.DataFrame(data[1:], columns=data[0])
            df = df.drop(['순위'], axis=1)
            year_record[j] = pd.concat([year_record[j], df], ignore_index=True)

            button = driver.find_elements_by_xpath('//*[@id="cphContents_cphContents_cphContents_udpContent"]/div[2]/div[2]/a[2]')[0]
            button.click()

            time.sleep(2)

            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            record_table = soup.find_all('table')
            data = parser.make2d(record_table[0])
            df = pd.DataFrame(data[1:], columns=data[0])
            df = df.drop(['순위', '팀명'], axis=1)
            year_record[j] = pd.merge(year_record[j], df, on='선수명')

            year_record[j].to_csv('./' + str(list(team_list.keys())[k]) + '_' + str(list(sort_list.keys())[i])
                                  + '_' + str(kbo_list[j]) + '.csv', index=False)
            
            # DataFrame 초기화
            year_record[j] = pd.DataFrame()
            
    driver.close()
