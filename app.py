import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title('産業と従業員')
df=pd.read_csv('data.csv',encoding='utf-8', skiprows=10)
df_clean=df.iloc[:,[7,8,9]].copy() 
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
    if display_option == '表を確認':
        st.write(f"### {selected_job} の抽出データ")
        st.write("必要な列（コード・男・女）だけを表示しています")
        st.table(filtered_df) 
        
    else:
        st.write(f"### {selected_job} の就業者数（男女比）")
        
        m = pd.to_numeric(str(target_row['男性']).replace(',', ''), errors='coerce')
        f = pd.to_numeric(str(target_row['女性']).replace(',', ''), errors='coerce')
        
        if pd.notnull(m) and pd.notnull(f):
            fig, ax = plt.subplots(figsize=(6, 4))
            ax.bar(['男性', '女性'], [m, f], color=['skyblue', 'pink'])
            ax.set_title(f"{selected_job} の男女比")
            st.pyplot(fig)
            
            ratio = (f / (m + f)) * 100
            st.info(f"この業種の女性比率は **{ratio:.1f}%** です。")
        else:
            st.error("数値データが見つかりませんでした。")
else:
    st.warning(f'「{selected_job}(コード:{selected_code})」のデータが見つかりませんでした。')