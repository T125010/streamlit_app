import streamlit as st
import pandas as pd
import plotly.express as px

st.title('産業と従業員')
df=pd.read_csv('data.csv',encoding='utf-8', skiprows=10)
df.rename(columns={df.columns[7]:'産業名'},inplace=True)

main_jobs=[
    "コンビニエンスストア",
    "菓子・パン小売業",
    "機械器具小売業",
    "繊維・衣服等卸売業",
    "飲食料品卸売業",
    "百貨店・総合スーパー",
    "医薬品・化粧品小売業",
    "通信販売・訪問販売小売業"
]

with st.sidebar:
    st.header('フィルタ設定')
    selected_job=st.selectbox('分析したい業種を選択してください',main_jobs)
