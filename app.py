import streamlit as st
import pandas as pd
import plotly.express as px

st.title('産業と従業員')
df=pd.read_csv('data.csv')