import streamlit as st
import pandas as pd

st.title('産業と従業員')
df=pd.read_csv('data.csv',encoding='utf-8', skiprows=10)

df_clean=df.iloc[:,[8,9,10]].copy() 
df_clean.columns=['産業コード名','男性','女性']


main_jobs={
    'コンビニエンスストア':'5891',
    '菓子・パン小売業':'586',
    '機械器具小売業':'59',
    '繊維・衣服等卸売業':'51',
    '飲食料品卸売業':'52',
    '百貨店・総合スーパー':'561',
    '医薬品・化粧品小売業':'603',
    '通信販売・訪問販売小売業':'611'
}

with st.sidebar:
    st.header('フィルタ設定')
    selected_job=st.selectbox('分析したい業種を選択してください',list(main_jobs.keys()))
    selected_code=main_jobs[selected_job]

    st.divider()
    display_option=st.radio('表示設定',['表を表示','グラフを表示'])

filtered_df = df_clean[df_clean['産業コード名'].astype(str).str.contains('^' + selected_code, na=False)]

if not filtered_df.empty:
    target_row=filtered_df.iloc[0]
    if display_option == '表を表示':
        st.write(f"{selected_job} の抽出データ")
        st.table(filtered_df.assign(index=None).set_index('index'))
        
    else:
        st.write(f"{selected_job} の就業者数（男女比）")

        def clean_speed(x):
            s = str(x).replace(',', '').replace(' ', '').replace('　', '')
            return pd.to_numeric(s, errors='coerce')
        
        m = pd.to_numeric(str(target_row['男性']).replace(',', ''), errors='coerce')
        f = pd.to_numeric(str(target_row['女性']).replace(',', ''), errors='coerce')
        
        if pd.notnull(m) and pd.notnull(f) and (m + f) > 0:
            fig, ax = plt.subplots(figsize=(6, 4))
            ax.bar(['男性', '女性'], [m, f], color=['#87CEEB', '#FFB6C1'])
            ax.set_ylim(0,max(m,f)*1.2)
            st.pyplot(fig)
            

            st.error("数値が取得できません。CSVの列番号（現在 8列目と9列目）が正しいか確認してください。")