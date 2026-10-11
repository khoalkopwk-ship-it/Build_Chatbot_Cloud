# Báo cáo tiến độ tuần 1 chatbot FAQ môn học

**Đề tài:** Xây dựng chatbot hỏi đáp FAQ môn học bằng tìm kiếm từ khóa hoặc TF-IDF trên Lambda.

**Mã môn học:** CLCO332779_05UTExMC

**Giảng viên hướng dẫn:** Huỳnh Xuân Phụng

**Tuần:** 01

| MSSV | Họ và tên | Vai trò |
|---|---|---|
| 24110253 | Đặng Nguyễn Minh Khoa | Nhóm trưởng |
| 24110166 | Ngô Anh Bằng | Thành viên |

## Mục tiêu và phạm vi

Nghiên cứu Lambda, API Gateway, S3, DynamoDB; thiết kế kiến trúc và dữ liệu; dựng nền tảng, gắn tag và kiểm thử truy cập. FAQ ban đầu tập trung vào quy định đồ án môn Cloud; nhóm rà soát đáp án theo yêu cầu.

## Kết quả thực hiện và phân công

| Thành viên | Công việc | Mức độ hoàn thành (%) | Số giờ | 
|---|---|---|---|
| Khoa | Nghiên cứu và thiết kế kiến trúc | 100 | 2 |
| Khoa | Vẽ sơ đồ | 100 | 2 |
| Khoa | Rà soát dữ liệu FAQ | 100 | 2 |
| Bằng | Tạo S3 private và website | 100 | 2 |
| Bằng | Tạo DynamoDB | 100 | 2 |
| Khoa | Kiểm tra LabRole, tạo Lambda | 100 | 2 |
| Bằng | Kiểm thử đọc S3 và ghi DynamoDB | 100 | 2 |
| Bằng | Gắn tag, Git, worklog và báo cáo | 100 | 2 |

# Quy tắc tên tài nguyên và tag

- Website endpoint: http://course-faq-web-24110253-24110166.s3-website-us-east-1.amazonaws.com
- API Invoke URL: https://ts6153n8b5.execute-api.us-east-1.amazonaws.com
- API route: POST /chat; payload 2.0; stage $default, auto-deploy
- CORS allowed origin: http://course-faq-web-24110253-24110166.s3-website-us-east-1.amazonaws.com
- FAQ key: faq/faq.json
- Lambda runtime / architecture / memory / timeout: Python 3.12 / x86_64 / 128 MB / 10 giây
- Execution role: LabRole
- Environment: FAQ_BUCKET=course-faq-data-24110253-24110166, FAQ_KEY=faq/faq.json, LOG_TABLE=course-faq-question-logs

## Repository

Link GitHub: https://github.com/khoalkopwk-ship-it/Build_Chatbot_Cloud.git


