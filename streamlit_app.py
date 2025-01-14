import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

class XiaohongshuStats:
    def __init__(self):
        self.data = {
            'date': [],
            'note_count': [],
            'views': [],
            'likes': [],
            'comments': [],
            'ad_cost': [],
            'engagement_rate': []
        }

    def calculate_engagement_rate(self, views, likes, comments):
        return round((likes + comments) / views * 100, 2) if views > 0 else 0

def main():
    st.set_page_config(page_title="小红书数据统计", layout="wide")
    st.title("小红书数据统计分析")

    # 创建两列布局
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("数据录入")
        note_count = st.number_input("笔记数量", min_value=0, value=0)
        views = st.number_input("浏览量", min_value=0, value=0)
        likes = st.number_input("点赞数", min_value=0, value=0)
        comments = st.number_input("评论数", min_value=0, value=0)
        ad_cost = st.number_input("广告费用", min_value=0.0, value=0.0)

        if st.button("提交数据"):
            # 获取或创建会话状态中的数据
            if 'data' not in st.session_state:
                st.session_state.data = {
                    'date': [],
                    'note_count': [],
                    'views': [],
                    'likes': [],
                    'comments': [],
                    'ad_cost': [],
                    'engagement_rate': []
                }
            
            # 计算互动率
            engagement_rate = XiaohongshuStats().calculate_engagement_rate(views, likes, comments)
            
            # 添加数据
            today = datetime.now().strftime('%Y-%m-%d')
            st.session_state.data['date'].append(today)
            st.session_state.data['note_count'].append(note_count)
            st.session_state.data['views'].append(views)
            st.session_state.data['likes'].append(likes)
            st.session_state.data['comments'].append(comments)
            st.session_state.data['ad_cost'].append(ad_cost)
            st.session_state.data['engagement_rate'].append(engagement_rate)
            
            st.success("数据添加成功！")

    with col2:
        st.subheader("数据统计")
        if 'data' in st.session_state and len(st.session_state.data['date']) > 0:
            df = pd.DataFrame(st.session_state.data)
            st.dataframe(df)
            
            # 绘制互动率趋势图
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.plot(df['date'], df['engagement_rate'], marker='o')
            ax.set_title('互动率趋势')
            ax.set_xlabel('日期')
            ax.set_ylabel('互动率 (%)')
            plt.xticks(rotation=45)
            st.pyplot(fig)
            
            # 显示统计摘要
            st.subheader("数据摘要")
            col3, col4, col5 = st.columns(3)
            with col3:
                st.metric("总笔记数", df['note_count'].sum())
            with col4:
                st.metric("总浏览量", df['views'].sum())
            with col5:
                st.metric("平均互动率", f"{df['engagement_rate'].mean():.2f}%")

if __name__ == "__main__":
    main()
