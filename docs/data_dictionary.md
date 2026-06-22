# Data Dictionary

Tài liệu này mô tả chi tiết ý nghĩa của tất cả các cột trong 4 file dữ liệu thuộc thư mục `data`.

## 1. `domain_worker_metadata.csv`
File này chứa thông tin nhân khẩu học, thái độ và mức độ sử dụng AI/LLM của những người tham gia khảo sát (workers).

| Tên cột | Ý nghĩa / Mô tả |
| :--- | :--- |
| **User ID** | Mã định danh duy nhất của người tham gia khảo sát. |
| **Occupation (O\*NET-SOC Title)** | Chức danh nghề nghiệp của người tham gia (theo chuẩn O*NET). |
| **Gender** | Giới tính của người tham gia. |
| **Race** | Sắc tộc / chủng tộc. |
| **Income** | Mức thu nhập. |
| **Age** | Tuổi. |
| **Education** | Trình độ học vấn cao nhất. |
| **Experience** | Số năm kinh nghiệm trong nghề. |
| **AI Tedious Work Attitude** | Thái độ đối với việc AI xử lý các công việc nhàm chán (Thang điểm Likert). |
| **AI Job Importance Attitude** | Thái độ đối với tầm quan trọng của AI trong công việc. |
| **AI Daily Interest Attitude** | Mức độ quan tâm hàng ngày đối với AI. |
| **AI Suffering Attitude** | Thái độ về những rủi ro/tác động tiêu cực của AI. |
| **Zip Code** | Mã bưu điện nơi người tham gia sinh sống. |
| **Political Affiliation** | Quan điểm/khuynh hướng chính trị. |
| **LLM Familiarity** | Mức độ quen thuộc với các Mô hình ngôn ngữ lớn (LLMs). |
| **LLM Use in Work** | Tần suất sử dụng LLM trong công việc nói chung. |
| **LLM Usage by Type - Information Access** | Tần suất dùng LLM để tra cứu/tiếp cận thông tin. |
| **LLM Usage by Type - Edit** | Tần suất dùng LLM để chỉnh sửa văn bản/dữ liệu. |
| **LLM Usage by Type - Idea Generation** | Tần suất dùng LLM để lên ý tưởng. |
| **LLM Usage by Type - Communication** | Tần suất dùng LLM để hỗ trợ giao tiếp (viết email, tin nhắn...). |
| **LLM Usage by Type - Analysis** | Tần suất dùng LLM để phân tích dữ liệu/thông tin. |
| **LLM Usage by Type - Decision** | Tần suất dùng LLM để hỗ trợ ra quyết định. |
| **LLM Usage by Type - Coding** | Tần suất dùng LLM để lập trình. |
| **LLM Usage by Type - System Design** | Tần suất dùng LLM để thiết kế hệ thống. |
| **LLM Usage by Type - Data Processing** | Tần suất dùng LLM để xử lý dữ liệu. |
| **Recruitment Source** | Nguồn tuyển dụng người tham gia khảo sát (ví dụ: Prolific, Upwork). |

---

## 2. `domain_worker_desires.csv`
File này chứa các đánh giá của người lao động đối với từng tác vụ cụ thể trong công việc của họ (nhu cầu tự động hóa, yêu cầu kỹ năng, v.v.).

| Tên cột | Ý nghĩa / Mô tả |
| :--- | :--- |
| **Task ID** | Mã định danh của tác vụ. |
| **Occupation (O\*NET-SOC Title)** | Chức danh nghề nghiệp liên quan đến tác vụ. |
| **Task** | Mô tả chi tiết tác vụ bằng văn bản. |
| **User ID** | Mã định danh của người đánh giá tác vụ này. |
| **Date** | Ngày thực hiện đánh giá. |
| **Self-reported Expertise** | Mức độ chuyên môn tự đánh giá của người lao động đối với tác vụ (Expert, Average, Novice). |
| **Automation Desire Rating** | Mức độ mong muốn tự động hóa tác vụ này. |
| **Time** | Đánh giá về thời gian tiêu tốn cho tác vụ. |
| **Core Skill Rating** | Đánh giá mức độ kỹ năng cốt lõi cần thiết. |
| **Job Security Rating** | Đánh giá mức độ an toàn việc làm liên quan đến tác vụ. |
| **Enjoyment Rating** | Mức độ yêu thích/tận hưởng khi làm tác vụ này. |
| **Reasons for Automation Desire - [Various]** | Các cột True/False chỉ định lý do muốn tự động hóa (Free Time, Repetitive, Human Error, Stress, Difficulty, Scale). |
| **Physical Action Requirement** | Đánh giá yêu cầu về hành động thể chất của tác vụ. |
| **Interpersonal Communication Requirement** | Đánh giá yêu cầu về giao tiếp giữa các cá nhân. |
| **Involved Uncertainty** | Đánh giá mức độ không chắc chắn/bất định của tác vụ. |
| **Domain Expertise Requirement** | Đánh giá yêu cầu về chuyên môn chuyên ngành. |
| **Human Agency Scale Rating** | Đánh giá mức độ cần thiết của sự can thiệp/vai trò con người. |
| **Reasons for Human Agency - [Various]** | Các cột True/False chỉ định lý do cần con người thực hiện (Physical, Control, Domain Knowledge, Empathy, Quality Oversight, Dynamic, Ethical). |
| **Other Reason for Automation Desire** | Lý do khác muốn tự động hóa (dạng văn bản tự do). |
| **Other Reason for Human Agency** | Lý do khác cần con người thực hiện (dạng văn bản tự do). |

---

## 3. `expert_rated_technological_capability.csv`
File này chứa các đánh giá từ các chuyên gia AI/Công nghệ về khả năng tự động hóa và các yêu cầu của các tác vụ.

| Tên cột | Ý nghĩa / Mô tả |
| :--- | :--- |
| **Task ID** | Mã định danh của tác vụ. |
| **Occupation (O\*NET-SOC Title)** | Chức danh nghề nghiệp tương ứng. |
| **Task** | Mô tả chi tiết tác vụ. |
| **User ID** | Mã định danh của chuyên gia đánh giá. |
| **Date** | Ngày thực hiện đánh giá. |
| **Automation Capacity Rating** | Đánh giá của chuyên gia về khả năng/tiềm năng tự động hóa tác vụ này bằng công nghệ hiện tại. |
| **Physical Action Requirement** | Đánh giá của chuyên gia về yêu cầu hành động thể chất. |
| **Involved Uncertainty** | Đánh giá của chuyên gia về mức độ bất định trong tác vụ. |
| **Domain Expertise Requirement** | Đánh giá của chuyên gia về yêu cầu kiến thức chuyên ngành. |
| **Interpersonal Communication Requirement** | Đánh giá của chuyên gia về yêu cầu giao tiếp. |
| **Human Agency Scale Rating** | Đánh giá của chuyên gia về mức độ cần thiết sự can thiệp của con người. |

---

## 4. `task_statement_with_metadata.csv`
File này chứa danh sách các tác vụ theo tiêu chuẩn của O*NET kèm theo các siêu dữ liệu (metadata) về nghề nghiệp và thị trường lao động.

| Tên cột | Ý nghĩa / Mô tả |
| :--- | :--- |
| **O\*NET-SOC Code** | Mã nghề nghiệp theo hệ thống phân loại O*NET. |
| **Occupation (O\*NET-SOC Title)** | Tên chức danh nghề nghiệp. |
| **Task ID** | Mã định danh của tác vụ. |
| **Task** | Mô tả chi tiết tác vụ. |
| **Task Type** | Loại tác vụ (ví dụ: Core - cốt lõi, Supplemental - bổ sung). |
| **Date** | Ngày cập nhật dữ liệu tác vụ này trên O*NET. |
| **Category** | Danh mục của tác vụ. |
| **Frequency** | Tần suất thực hiện tác vụ trong nghề nghiệp. |
| **Importance** | Độ quan trọng của tác vụ đối với nghề nghiệp. |
| **Relevance** | Độ liên quan của tác vụ. |
| **Occupation Mean Annual Wage** | Mức lương trung bình hàng năm của nghề nghiệp này. |
| **Occupation Employment** | Tổng số lượng việc làm/người lao động trong nghề nghiệp này. |
| **Skill (O\*NET Work Activity)** | Các kỹ năng hoặc hoạt động làm việc chung (Generalized Work Activity) liên quan đến tác vụ. |
| **Skill ID (O\*NET Generalized Work Activity ID)** | Mã định danh tương ứng của các kỹ năng/hoạt động làm việc được liệt kê ở cột trên. |
