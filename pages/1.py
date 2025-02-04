import requests
import pandas as pd
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import matplotlib as mpl
#from dotenv import load_dotenv
import seaborn as sns
import streamlit as st
#import os
#load_dotenv()
#key=os.getenv('key')
url="http://api.sexoffender.go.kr/openapi/SOCitysStats/"
params={'serviceKey':st.secrets['key']}
#api호출
response=requests.get(url, params=params)
if response.status_code==200:
    root=ET.fromstring(response.content)
    data=[]
    for city in root.findall('.//City'):
        data.append(
            {
                'city_name':city.find('city-name').text,
                'city_count':city.find('city-count').text
            }
        )
    df=pd.DataFrame(data)
    df['city_count']=df['city_count'].astype(int)
    df=df.sort_values('city_count',ascending=False)
    
    #시각화
    mpl.rcParams['font.family']='Malgun Gothic'
    mpl.rcParams['font.size']=12
    mpl.rcParams['axes.unicode_minus']=False

    fig=plt.figure(figsize=(12,6))
    sns.barplot(x='city_name',y='city_count',data=df)
    plt.xticks(rotation=45)
    plt.title('지역별 성범죄 통계')
    #plt.show()
    st.pyplot(fig)
   