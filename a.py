import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# 2001 ~ 2021 팀 성적 csv 불러오기
file = []
year_record = pd.DataFrame()

for i in range(2001, 2022):
    file.append(pd.read_csv('./' + str(i) + '_new.csv'))
    
# 하나로 합침
for f in file:
    year_record = pd.concat([year_record, f], ignore_index=True)

# 승률과의 상관관계 확인 전 각 컬럼의 속성 확인
'''pd.set_option('display.max_rows', None)
print(year_record.dtypes)
print(len(year_record.columns))''' # columns -> 71개

# object인 팀명, IP 컬럼 제거
#year_record = year_record.drop(['팀명', 'IP'], axis=1)
feature = ['팀명']

for index, col in enumerate(year_record.columns):
    if col == '팀명' or col == 'IP':
        continue
    elif index <= 66 and (0.4 <= year_record[col].corr(year_record['WPCT']) <= 0.7 or -0.7 <= year_record[col].corr(year_record['WPCT']) <= -0.4):
        feature.append(col)
        print(col, year_record[col].corr(year_record['WPCT']))
        plt.scatter(x=year_record[col], y=year_record['WPCT'], label=col)
        plt.xlabel(col)
        plt.ylabel('WPCT')
        plt.show()

feature.append('WPCT')
feature.append('순위')
print(feature)
