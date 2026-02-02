import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import japanize_matplotlib

st.title('産業と従業員分析アプリ')
df=pd.read_csv('data.csv',encoding='utf-8', skiprows=10)

df_clean = df.iloc[:, [7,8,10,11]].copy() 
df_clean.columns = ['コード', '産業名', '男性', '女性']


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

filtered_df = df_clean[df_clean['コード'].astype(str).str.contains(str(selected_code), na=False)]

if not filtered_df.empty:
    target_row=filtered_df.iloc[0]
    if display_option == '表を表示':
        st.dataframe(filtered_df)
        
    else:
        st.write(f"{selected_job} の就業者数（男女比）")

        def to_num(x):
            s = str(x).replace(',', '').replace(' ', '').replace('　', '').replace('-', '0')
            return pd.to_numeric(s, errors='coerce')
        
        m = to_num(target_row['男性'])
        f = to_num(target_row['女性'])
        
        if pd.notnull(m) and pd.notnull(f):

            total = m + f
            ratio = (f / total) * 100 if total > 0 else 0
            col1, col2 = st.columns(2)
            with col1:
                st.metric("総就業者数", f"{int(total):,}人")
            with col2:
                st.metric("女性の割合", f"{ratio:.1f}%", delta=f"{ratio-50:.1f}% (基準50%)")
            
            st.divider() 
            fig, ax = plt.subplots(figsize=(8, 5))
            
            labels=['男性', '女性']
            values=[m, f]
            colors=['#0000ff', '#ff0000'] 
            
            bars=ax.bar(labels, values, color=colors)

            for bar in bars:
                height=bar.get_height()
                ax.annotate(f'{int(height):,}人',
                            xy=(bar.get_x() + bar.get_width() / 2, height),
                            xytext=(0, 3),  # 3ポイント上にずらす
                            textcoords="offset points",
                            ha='center', va='bottom', fontsize=12, fontweight='bold')
            ax.set_ylabel('人数')
            ax.set_title(f"{target_row['産業名']} の男女内訳")
            
            st.pyplot(fig)
            
            total = m + f
            if total > 0:
                ratio = (f / total) * 100
                st.subheader("💡 データからわかること")
                st.write(f"女性の割合は {ratio:.1f}% です。")
        else:
            st.error("データの数値化に失敗しました。")
else:
    st.warning('データが見つかりませんでした。')