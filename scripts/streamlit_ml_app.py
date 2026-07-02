import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as stns
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import Ridge
import os

st.set_page_config(page_title="IT Worker AI Insights", layout="wide")

st.title("Phân tích Dữ liệu Ứng dụng AI ngành Công nghệ Thông tin")
st.markdown("---")

@st.cache_data
def load_data():
    base_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'CSC')
    desires_df = pd.read_csv(os.path.join(base_path, 'domain_worker_desires.csv'))
    metadata_df = pd.read_csv(os.path.join(base_path, 'domain_worker_metadata.csv'))
    # Merge datasetsKhuyến nghị hành động:
    merged_df = pd.merge(desires_df, metadata_df, on='User ID', how='inner')
    return desires_df, metadata_df, merged_df

try:
    desires_df, metadata_df, merged_df = load_data()
except Exception as e:
    st.error(f"Lỗi khi tải dữ liệu: {e}")
    st.stop()

st.sidebar.header("Thông tin dữ liệu")
st.sidebar.write(f"Số lượng bản ghi sau khi gộp: {len(merged_df)}")
st.sidebar.write(f"Số lượng người tham gia: {merged_df['User ID'].nunique()}")

# -------------------------------------------------------------
# PHẦN 1: Random Forest - Feature Importance
# -------------------------------------------------------------
st.header("1. Dự đoán mong muốn tự động hóa (Random Forest)")
st.write("Sử dụng mô hình Random Forest để tìm ra các yếu tố có sức ảnh hưởng lớn nhất đến điểm số **Automation Desire Rating**.")

with st.spinner("Đang huấn luyện mô hình Random Forest..."):
    target = 'Automation Desire Rating'
    features = [
        'Core Skill Rating', 'Job Security Rating', 'Enjoyment Rating',
        'Experience', 'Human Agency Scale Rating',
        'Physical Action Requirement', 'Interpersonal Communication Requirement',
        'Involved Uncertainty', 'Domain Expertise Requirement'
    ]
    
    # Chuẩn bị dữ liệu
    model_data = merged_df[features + [target]].dropna()
    X = model_data[features].copy()
    
    # Chuyển đổi các cột chữ (categorical) sang số để RandomForest có thể xử lý
    for col in X.select_dtypes(include=['object', 'category', 'bool']).columns:
        X[col] = pd.factorize(X[col])[0]
        
    y = model_data[target]
    
    if len(X) < 50:
        st.warning("Dữ liệu không đủ để huấn luyện mô hình.")
    else:
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
        rf_model.fit(X_train, y_train)
        predictions = rf_model.predict(X_test)
        mse = mean_squared_error(y_test, predictions)
        
        st.success(f" Mean Squared Error trên tập test: **{mse:.2f}**")
        
        feature_importance = pd.DataFrame({
            'Feature': features,
            'Importance': rf_model.feature_importances_
        }).sort_values(by='Importance', ascending=False)
        
        fig, ax = plt.subplots(figsize=(10, 5))
        stns.barplot(data=feature_importance, x='Importance', y='Feature', ax=ax, palette='viridis')
        ax.set_title("Mức độ quan trọng của các đặc trưng (Feature Importance)")
        ax.set_xlabel("Độ quan trọng")
        ax.set_ylabel("Đặc trưng")
        st.pyplot(fig)
        
        st.info("""
        **Giải thích Insight:** 
        - Các yếu tố nằm trên cùng của biểu đồ là những động lực chính chi phối mong muốn tự động hóa của nhân sự IT. 
        Ví dụ, nếu `Enjoyment Rating` (Mức độ yêu thích) hoặc `Job Security Rating` (An toàn việc làm) có độ quan trọng cao, điều này có nghĩa là khi một tác vụ nhàm chán hoặc không đe dọa trực tiếp đến việc làm, nhân sự sẽ rất sẵn lòng giao nó cho AI.
        
        **Khuyến nghị hành động:**
        - **Cho Quản lý:** Khi triển khai AI, hãy ưu tiên tự động hóa các tác vụ lặp đi lặp lại (ít Enjoyment) trước tiên để tạo sự ủng hộ từ nhân viên, thay vì ép áp dụng AI vào các khâu cốt lõi đòi hỏi tính sáng tạo.
        - **Cho Nhân sự IT:** Hãy tập trung trau dồi các kỹ năng chuyên môn sâu và giao tiếp, vì AI gặp nhiều khó khăn nhất trong việc thay thế con người ở các khía cạnh này.
        """)

st.markdown("---")

# -------------------------------------------------------------
# PHẦN 2: TF-IDF & Ridge Regression - Semantic Analysis
# -------------------------------------------------------------
st.header("2. Phân tích ngữ nghĩa mô tả tác vụ")
st.write("Sử dụng kỹ thuật NLP (TF-IDF) trên cột mô tả công việc (Task) và mô hình Ridge Regression để tìm ra những từ khóa thúc đẩy hoặc cản trở tự động hóa.")

with st.spinner("Đang xử lý văn bản và huấn luyện mô hình Regression..."):
    text_data = merged_df[['Task', 'Automation Desire Rating']].dropna()
    
    if len(text_data) < 50:
        st.warning("Không đủ dữ liệu văn bản để huấn luyện.")
    else:
        X_text = text_data['Task']
        y_text = text_data['Automation Desire Rating']
        
        # TF-IDF
        vectorizer = TfidfVectorizer(stop_words='english', max_features=1000)
        X_vec = vectorizer.fit_transform(X_text)
        
        # Train-test split
        X_tr, X_te, y_tr, y_te = train_test_split(X_vec, y_text, test_size=0.2, random_state=42)
        
        # Regression
        ridge = Ridge(alpha=1.0)
        ridge.fit(X_tr, y_tr)
        
        feature_names = vectorizer.get_feature_names_out()
        coefficients = ridge.coef_
        
        word_coef_df = pd.DataFrame({
            'Word': feature_names,
            'Coefficient': coefficients
        })
        
        top_positive = word_coef_df.sort_values(by='Coefficient', ascending=False).head(15)
        top_negative = word_coef_df.sort_values(by='Coefficient', ascending=True).head(15)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Từ khóa thúc đẩy tự động hóa")
            fig_pos, ax_pos = plt.subplots(figsize=(6, 5))
            stns.barplot(data=top_positive, x='Coefficient', y='Word', ax=ax_pos, palette='Greens_r')
            ax_pos.set_title("Top từ khóa có trọng số dương nhất")
            st.pyplot(fig_pos)
            
        with col2:
            st.subheader("Từ khóa cản trở tự động hóa")
            fig_neg, ax_neg = plt.subplots(figsize=(6, 5))
            # Để vẽ biểu đồ dễ nhìn hơn cho số âm, có thể dùng giá trị tuyệt đối hoặc để nguyên
            stns.barplot(data=top_negative, x='Coefficient', y='Word', ax=ax_neg, palette='Reds_r')
            ax_neg.set_title("Top từ khóa có trọng số âm nhất")
            st.pyplot(fig_neg)

        st.info("""
        **Giải thích Insight:** 
        - **Màu xanh (Thúc đẩy tự động hóa):** Đại diện cho những mô tả công việc mang tính thủ công, xử lý số liệu lặp lại, hoặc giám sát. Nhân sự IT thường muốn giải phóng bản thân khỏi những tác vụ này để AI làm thay.
        - **Màu đỏ (Cản trở tự động hóa):** Đại diện cho các tác vụ mang tính chiến lược, thiết kế kiến trúc, hoặc liên quan đến con người/bảo mật. Đây là "vùng an toàn" mà con người muốn giữ lại sự kiểm soát tuyệt đối.
        
        **Khuyến nghị hành động:**
        - **Tối ưu quy trình phần mềm:** Đầu tư mạnh vào các công cụ AI hỗ trợ viết test tự động, sinh báo cáo , và theo dõi lỗi để tăng hiệu suất.
        - **Định hướng công cụ AI:** Trong các tác vụ thiết kế hoặc ra quyết định, AI chỉ nên đóng vai trò Trợ lý đưa ra gợi ý, nhường lại quyền quyết định cuối cùng (Human Agency) cho kỹ sư.
        """)
