import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(page_title="AI Agent Research: CSC Insights", layout="wide")

# Load data
@st.cache_data
def load_data():
    d = r'data\CSC'
    desires = pd.read_csv(os.path.join(d, 'domain_worker_desires.csv'))
    metadata = pd.read_csv(os.path.join(d, 'domain_worker_metadata.csv'))
    expert = pd.read_csv(os.path.join(d, 'expert_rated_technological_capability.csv'))
    tasks = pd.read_csv(os.path.join(d, 'task_statement_with_metadata.csv'))
    merged = pd.merge(desires, metadata, on='User ID')
    return desires, metadata, expert, tasks, merged

try:
    desires, metadata, expert, tasks, merged = load_data()
except Exception as e:
    st.error(f"Error loading data: {e}. Please ensure you are running this from the project root and 'data/CSC' exists.")
    st.stop()

st.sidebar.title("Khám phá Insights")
st.sidebar.markdown("Dự án Nghiên cứu sự chấp nhận AI Agent trong ngành CNTT (CSC)")
page = st.sidebar.radio("",[
    "1. Nghịch lý Tự động hóa",
    "2. Nghịch lý Tuổi nghề",
    "3. Đường cong chữ U Thu nhập",
    "4. Phân hóa Quyền kiểm soát",
    "5. Ngưỡng Tần suất công việc"
])

st.title("AI Agent Research: CSC Insights Dashboard")

if page == "1. Nghịch lý Tự động hóa":
    st.header("1. Nghịch lý Tự động hóa (The Automation Paradox)")
    st.markdown("Có một sự **lệch pha nghiêm trọng** giữa những gì AI làm giỏi nhất và những gì con người muốn giao phó nhất.")
    
    avg_desire = desires.groupby("Task ID")["Automation Desire Rating"].mean().reset_index()
    avg_expert = expert.groupby("Task ID")["Automation Capacity Rating"].mean().reset_index()
    gap_df = pd.merge(avg_desire, avg_expert, on="Task ID")
    gap_df = pd.merge(gap_df, tasks[["Task ID", "Task"]], on="Task ID")
    
    fig = px.scatter(gap_df, x="Automation Capacity Rating", y="Automation Desire Rating", hover_data=['Task'],
                     title="Khả năng của AI (Capacity) vs Mong muốn của con người (Desire)",
                     labels={"Automation Capacity Rating": "AI Capacity (Khả năng AI)", "Automation Desire Rating": "Human Desire (Mức độ muốn tự động)"},
                     color_discrete_sequence=['#ef553b'])
    
    # Add quadrants
    fig.add_hline(y=gap_df['Automation Desire Rating'].mean(), line_dash="dash", line_color="gray")
    fig.add_vline(x=gap_df['Automation Capacity Rating'].mean(), line_dash="dash", line_color="gray")
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.info("**Phân tích:** Các điểm nằm ở góc dưới bên phải (Capacity cao nhưng Desire thấp) là các tác vụ cốt lõi (như Review Code). Các điểm ở góc trên bên trái (Capacity thấp nhưng Desire cao) là các tác vụ quản trị (như lập ngân sách).")
    st.success("**Khuyến nghị:** Đừng cố bán các công cụ AI 'thay thế coder'. Hãy bán công cụ quản lý resource hoặc Copilot hỗ trợ.")

elif page == "2. Nghịch lý Tuổi nghề":
    st.header("2. Nghịch lý Tuổi nghề (The Experience Inversion)")
    st.markdown("Trái với định kiến 'người trẻ thích công nghệ, người già bảo thủ', dữ liệu chứng minh điều ngược lại.")
    
    exp_order = ["Less than 1 year", "1-2 year", "3-5 years", "6-10 years", "More than 10 years"]
    exp_df = merged.groupby("Experience")["Automation Desire Rating"].mean().reindex(exp_order).reset_index()
    
    fig = px.bar(exp_df, x="Experience", y="Automation Desire Rating", color="Automation Desire Rating",
                 title="Mức độ muốn Tự động hóa theo Kinh nghiệm làm việc",
                 color_continuous_scale="Viridis")
    st.plotly_chart(fig, use_container_width=True)
    
    st.info("**Phân tích:** Fresher (dưới 1 năm) e ngại AI nhất vì sợ mất cơ hội học hỏi (2.83/5). Senior (trên 10 năm) lại khao khát tự động hóa nhất (3.42/5) vì chán việc lặp lại.")
    st.success("**Khuyến nghị:** Truyền thông áp dụng AI nên đánh vào tầng lớp Senior/Lead để họ làm gương, thay vì ép từ dưới lên.")

elif page == "3. Đường cong chữ U Thu nhập":
    st.header("3. Đường cong chữ U của Nỗi sợ AI (The Wealth-AI U-Curve)")
    st.markdown("Nỗi sợ AI không rải đều mà tập trung đe dọa trực tiếp nhóm kỹ sư trung lưu.")
    
    inc_order = ["0-30K", "30-60K", "60-86K", "86-165K", "165K-209K", "209K-529K", "529K+"]
    inc_df = merged.groupby('Income')['Automation Desire Rating'].mean().reset_index()
    
    # Clean and order
    inc_df = inc_df[inc_df['Income'] != 'Prefer not to say']
    inc_df['Income_Cat'] = pd.Categorical(inc_df['Income'], categories=inc_order, ordered=True)
    inc_df = inc_df.sort_values('Income_Cat')
    
    fig = px.line(inc_df, x="Income_Cat", y="Automation Desire Rating", markers=True,
                  title="Mức độ muốn Tự động hóa theo Thu nhập", line_shape="spline")
    fig.update_traces(line=dict(width=3, color="orange"), marker=dict(size=10))
    st.plotly_chart(fig, use_container_width=True)
    
    st.info("**Phân tích:** Nhóm thu nhập trung lưu (60K - 500K) có xu hướng bài xích AI cao nhất vì lo sợ giá trị chuyên môn bị thay thế. Nhóm C-level (529K+) và Fresher (0-60K) lại ủng hộ AI cực kỳ mạnh.")
    st.success("**Khuyến nghị:** Cần có chương trình đào tạo nội bộ (upskill) để các kỹ sư trung lưu không coi AI là kẻ thù cướp việc.")

elif page == "4. Phân hóa Quyền kiểm soát":
    st.header("4. Sự phân hóa về 'Quyền kiểm soát' (The Control Divide)")
    st.markdown("Mức độ đòi hỏi quyền ra quyết định cuối cùng (Human Agency) phân hóa cực mạnh giữa Research và Management.")
    
    occ_df = desires.groupby('Occupation (O*NET-SOC Title)')['Human Agency Scale Rating'].mean().sort_values().reset_index()
    
    fig = px.bar(occ_df, x="Human Agency Scale Rating", y="Occupation (O*NET-SOC Title)", orientation='h',
                 title="Đòi hỏi 'Quyền ra quyết định' theo Từng ngành", color="Human Agency Scale Rating",
                 color_continuous_scale="Blues")
    st.plotly_chart(fig, use_container_width=True)
    
    st.info("**Phân tích:** Nhà nghiên cứu (Scientists) đòi hỏi Human Agency cực cao vì cần tính chính xác tuyệt đối. Nhà quản lý (Managers) lại sẵn sàng giao quyền cho máy móc nếu đạt KPI.")
    st.success("**Khuyến nghị:** Bán AI cho Scientists bắt buộc phải có tính 'Explainable AI'. Bán cho Managers chỉ cần Tốc độ và Dashboard báo cáo.")

elif page == "5. Ngưỡng Tần suất công việc":
    st.header("5. Ngưỡng chịu đựng Tần suất (The Frequency Threshold)")
    st.markdown("Chỉ những việc lặp đi lặp lại **Hằng ngày** mới khiến lập trình viên phải mở AI lên làm thay.")
    
    merged_task = pd.merge(desires, tasks, on='Task ID')
    freq_df = merged_task.groupby('Frequency')['Automation Desire Rating'].mean().reset_index().sort_values('Frequency')
    
    fig = px.line(freq_df, x="Frequency", y="Automation Desire Rating", markers=True,
                  title="Mức độ tự động hóa tỷ lệ thuận với Tần suất lặp lại",
                  labels={"Frequency": "Tần suất (Càng lớn càng thường xuyên)"})
    fig.update_traces(line=dict(width=3, color="green"), marker=dict(size=10))
    st.plotly_chart(fig, use_container_width=True)
    
    st.info("**Phân tích:** Tác vụ hiếm khi làm (Frequency thấp) thì họ thà tự làm tay. Tác vụ tần suất chạm đỉnh (liên tục mỗi ngày) thì khao khát tự động hóa tăng vọt.")
    st.success("**Khuyến nghị:** Hãy nhắm vào các micro-tasks rác lặp lại hàng ngày (như sinh unit test, tạo boilerplate, viết commit) thay vì các workflow vi mô rườm rà.")

st.sidebar.markdown("---")
