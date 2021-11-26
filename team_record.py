# KBO 기록실에서 연도별 팀 성적 크롤링
import numpy as np
import pandas as pd
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from html_table_parser import parser_functions as parser
from selenium.webdriver.support.select import Select

# Query 변수
sort_list = {"Hitter" : "BasicOld", "Pitcher" : "BasicOld", "Defense" : "Basic", "Runner" : "Basic"}

# 2001 ~ 2021 팀 성적
kbo_list = list(np.arange(2001, 2022))
year_record = []

for record in kbo_list:
    record = pd.DataFrame()
    year_record.append(record)
    
for i in range(0, len(sort_list)):
    # 드라이버 객체
    driver = webdriver.Chrome(executable_path='D:/conda/chromedriver.exe')
    
    # KBO 기록실 URL
    part_URL = "https://www.koreabaseball.com/Record/Team/"
        
    # 각 기록별 URL
    part_URL += list(sort_list.keys())[i] + "/" + list(sort_list.values())[i] + ".aspx"
    
    driver.get(url=str(part_URL))
    
    if i == 0:
        select_tag = Select(driver.find_element_by_id("cphContents_cphContents_cphContents_ddlSeries_ddlSeries"))
        select_tag.select_by_value(str(0))
    elif i == 1:
        select_tag = Select(driver.find_element_by_id("cphContents_cphContents_cphContents_ddlSeries_ddlSeries"))
        select_tag.select_by_value(str(7))
        time.sleep(2)
        select_tag = Select(driver.find_element_by_id("cphContents_cphContents_cphContents_ddlSeries_ddlSeries"))
        select_tag.select_by_value(str(0))
        
    time.sleep(2)
    
    for j in range(0, 21):
        if i == 0 or i == 1:
            button = driver.find_elements_by_xpath('//*[@id="cphContents_cphContents_cphContents_udpContent"]/div[2]/div/div/a[1]')[0]
            button.click()
            
        time.sleep(2)
            
        select_tag = Select(driver.find_element_by_id("cphContents_cphContents_cphContents_ddlSeason_ddlSeason"))
        select_tag.select_by_value(str(j+2001))
        
        time.sleep(2)
        
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        record_table = soup.find_all('table')
        data = parser.make2d(record_table[0])
        df = pd.DataFrame(data[1:], columns=data[0])
        
        if i == 0:
            year_record[j] = pd.concat([year_record[j], df], ignore_index=True)
        else:
            year_record[j] = pd.merge(year_record[j], df, on='팀명')
            
        if i == 0 or i == 1:
            button = driver.find_elements_by_xpath('//*[@id="cphContents_cphContents_cphContents_udpContent"]/div[2]/div/div/a[2]')[0]
            button.click()
            
            time.sleep(2)
        
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            record_table = soup.find_all('table')
            data = parser.make2d(record_table[0])
            df = pd.DataFrame(data[1:], columns=data[0])
            year_record[j] = pd.merge(year_record[j], df, on='팀명')
            
    driver.close()

pd.set_option('display.max_columns', None)
print(year_record[0].columns)
    
for i in range(len(year_record)):
    year_record[i] = year_record[i].drop(['순위_x', 'G_x', '순위_y', 'AVG_y', 'ERA_y' ,'G_y'], axis=1)
    year_record[i].to_csv('./' + str(kbo_list[i]) + '.csv', index=False)
