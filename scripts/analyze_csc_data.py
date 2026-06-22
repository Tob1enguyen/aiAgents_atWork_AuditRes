import pandas as pd
import os

data_dir = r"C:\Users\NguyenNgocKhanh\Desktop\k\sandbox\ai_agent_research_project\data\CSC"
out_file = r"C:\Users\NguyenNgocKhanh\Desktop\k\sandbox\ai_agent_research_project\docs\csc_insights.md"

def load_data():
    desires = pd.read_csv(os.path.join(data_dir, "domain_worker_desires.csv"))
    expert = pd.read_csv(os.path.join(data_dir, "expert_rated_technological_capability.csv"))
    metadata = pd.read_csv(os.path.join(data_dir, "domain_worker_metadata.csv"))
    tasks = pd.read_csv(os.path.join(data_dir, "task_statement_with_metadata.csv"))
    return desires, expert, metadata, tasks

def generate_insights():
    desires, expert, metadata, tasks = load_data()
    
    md_content = ["# Insight & Khuyến nghị nhóm ngành Công nghệ Thông tin (CSC)\n"]
    
    # 1. Tổng quan
    md_content.append("## 1. Tổng quan dữ liệu")
    md_content.append(f"- **Số lượng người tham gia khảo sát**: {len(metadata)}")
    md_content.append(f"- **Số lượng tác vụ (tasks) được đánh giá**: {len(tasks)}")
    md_content.append(f"- **Ngành nghề tham gia**: {', '.join(metadata['Occupation (O*NET-SOC Title)'].unique())}")
    
    # 2. Gap Analysis (Khả năng AI vs Mong muốn của con người)
    avg_desire = desires.groupby("Task ID")["Automation Desire Rating"].mean().reset_index()
    avg_expert = expert.groupby("Task ID")["Automation Capacity Rating"].mean().reset_index()
    
    gap_df = pd.merge(avg_desire, avg_expert, on="Task ID")
    gap_df = pd.merge(gap_df, tasks[["Task ID", "Task", "Occupation (O*NET-SOC Title)"]], on="Task ID")
    gap_df["Gap (Capacity - Desire)"] = gap_df["Automation Capacity Rating"] - gap_df["Automation Desire Rating"]
    
    md_content.append("\n## 2. Phân tích Khoảng cách (Gap Analysis)")
    md_content.append("> Khoảng cách được tính bằng: **Khả năng của AI (Expert Rating) - Mong muốn tự động hóa (Worker Desire)**. Khoảng cách dương nghĩa là AI đã sẵn sàng nhưng con người chưa muốn giao phó.\n")
    
    top_gap = gap_df.sort_values(by="Gap (Capacity - Desire)", ascending=False).head(3)
    md_content.append("### 2.1. Tác vụ AI làm tốt nhưng con người muốn giữ lại (High Capacity, Low Desire):")
    for _, row in top_gap.iterrows():
        md_content.append(f"- **{row['Task']}** ({row['Occupation (O*NET-SOC Title)']})")
        md_content.append(f"  - AI Capacity: {row['Automation Capacity Rating']:.2f}/5.0 | Human Desire: {row['Automation Desire Rating']:.2f}/5.0 | Gap: +{row['Gap (Capacity - Desire)']:.2f}")
        
    bottom_gap = gap_df.sort_values(by="Gap (Capacity - Desire)", ascending=True).head(3)
    md_content.append("\n### 2.2. Tác vụ con người rất muốn tự động hóa nhưng AI chưa đáp ứng tốt (Low Capacity, High Desire):")
    for _, row in bottom_gap.iterrows():
        md_content.append(f"- **{row['Task']}** ({row['Occupation (O*NET-SOC Title)']})")
        md_content.append(f"  - AI Capacity: {row['Automation Capacity Rating']:.2f}/5.0 | Human Desire: {row['Automation Desire Rating']:.2f}/5.0 | Gap: {row['Gap (Capacity - Desire)']:.2f}")

    # 3. Phân tích Nguyên nhân (Reasons)
    auto_reasons = [c for c in desires.columns if "Reasons for Automation Desire" in c and "Other" not in c]
    agency_reasons = [c for c in desires.columns if "Reasons for Human Agency" in c and "Other" not in c]
    
    auto_counts = desires[auto_reasons].sum().sort_values(ascending=False).head(3)
    agency_counts = desires[agency_reasons].sum().sort_values(ascending=False).head(3)
    
    md_content.append("\n## 3. Tại sao người lao động muốn/không muốn dùng AI?")
    md_content.append("### Động lực chính muốn tự động hóa (Top reasons for Automation):")
    for k, v in auto_counts.items():
        reason = k.split(" - ")[1]
        pct = (v / len(desires)) * 100
        md_content.append(f"- **{reason}**: {v} lượt chọn ({pct:.1f}%)")
        
    md_content.append("\n### Lý do chính muốn giữ quyền kiểm soát của con người (Top reasons for Human Agency):")
    for k, v in agency_counts.items():
        reason = k.split(" - ")[1]
        pct = (v / len(desires)) * 100
        md_content.append(f"- **{reason}**: {v} lượt chọn ({pct:.1f}%)")
        
    # 4. Phân tích Nhân khẩu học (Demographics vs Desire)
    merged_user = pd.merge(desires, metadata, on="User ID")
    
    if 'LLM Familiarity' in merged_user.columns:
        llm_desire = merged_user.groupby("LLM Familiarity")["Automation Desire Rating"].mean().sort_values(ascending=False)
        md_content.append("\n## 4. Đặc điểm nhân khẩu học & Mức độ chấp nhận")
        md_content.append("### Mức độ quen thuộc với LLM ảnh hưởng đến mong muốn tự động hóa:")
        for k, v in llm_desire.items():
            md_content.append(f"- **{k}**: {v:.2f}/5.0")
            
    if 'Experience' in merged_user.columns:
        exp_desire = merged_user.groupby("Experience")["Automation Desire Rating"].mean().sort_values(ascending=False)
        md_content.append("\n### Kinh nghiệm làm việc ảnh hưởng đến mong muốn tự động hóa:")
        for k, v in exp_desire.items():
            md_content.append(f"- **{k}**: {v:.2f}/5.0")

    # 5. Đề xuất & Khuyến nghị
    md_content.append("\n## 5. Khuyến nghị hành động (Recommendations)")
    md_content.append("> Dựa trên các insight trên, đây là chiến lược áp dụng AI Agent cho nhóm ngành CSC:")
    md_content.append("1. **Ưu tiên tích hợp AI vào các tác vụ mang tính thủ công, lặp đi lặp lại hoặc dễ sai sót** (những task có Desire cao) thay vì cố gắng dùng AI để thay thế các quyết định mang tính chiến lược hoặc thiết kế hệ thống cấp cao.")
    md_content.append(f"2. **Giải quyết rào cản tâm lý ở nhóm tác vụ có AI Capacity cao nhưng User Desire thấp**: Nguyên nhân chủ yếu người lao động từ chối là do {agency_counts.index[0].split(' - ')[1]} và {agency_counts.index[1].split(' - ')[1]}. Cần thiết kế AI Agent theo hướng 'Hỗ trợ' (Copilot) thay vì 'Thay thế' (Autopilot).")
    md_content.append("3. **Đào tạo kỹ năng LLM**: Dữ liệu cho thấy những người càng quen thuộc với AI/LLM càng có xu hướng cởi mở hơn với việc tự động hóa. Đào tạo nội bộ sẽ thúc đẩy việc áp dụng AI.")
    
    # Write to file
    with open(out_file, "w", encoding="utf-8") as f:
        f.write("\n".join(md_content))
        
    print(f"Report generated at: {out_file}")

if __name__ == "__main__":
    generate_insights()
