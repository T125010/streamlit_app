import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title('産業と従業員')
df=pd.read_csv('data.csv',encoding='utf-8', skiprows=10)
df.rename(columns={df.columns[7]:'産業名'},inplace=True)

# デバッグ用：最初の20行の「産業名」を画面に出して確認する
st.write("CSVの中身（産業名列）:", df['産業名'].head(20))

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

    st.divider()
    st.header('表示設定')
    display_option=st.selectbox('表示内容',['基本データ','男女比グラフ'])

filtered_df=df[df.iloc[:,7].str.contains(selected_job,na=False,)]

if not filtered_df.empty:
    target_row=filtered_df.iloc[0]
    st.write(f'{selected_job} のデータ一覧')
    st.dataframe(filtered_df)

    st.write('就業者の男女比較')
    labels=['男性','女性']
    
    try:
        male_count=pd.to_numeric(target_row.iloc[8], errors='coerce')
        female_count=pd.to_numeric(target_row.iloc[9], errors='coerce')
        
        counts=[male_count,female_count]

        fig,ax=plt.subplots(figsize=(8,5))
        ax.bar(labels, counts, color=['skyblue','pink'])
        ax.set_ylabel('人数')
        ax.set_title(f'{selected_job} の就業者数内訳')

        st.pyplot(fig)
    except:
        st.error('データの数値変換に失敗しました。')
else:
    st.warning('データが見つかりませんでした。')