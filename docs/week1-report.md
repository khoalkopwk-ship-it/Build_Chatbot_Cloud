# BÁO CÁO TIẾN ĐỘ TUẦN 1

**Nhóm:** Serverless

**Môn học:** Điện toán đám mây

**Mã môn học:** CLCO332779_05UTExMC

**Giảng viên hướng dẫn:** Huỳnh Xuân Phụng

**Đề tài:** Xây dựng chatbot hỏi đáp FAQ môn học bằng tìm kiếm từ khóa/TF-IDF trên AWS Lambda.

**Repository:** https://github.com/khoalkopwk-ship-it/Build_Chatbot_Cloud

## 1. Thành viên

| MSSV | Họ và tên | Vai trò |
|---|---|---|
| 24110253 | Đặng Nguyễn Minh Khoa | Nhóm trưởng |
| 24110166 | Ngô Anh Bằng | Thành viên |

## 2. Mục tiêu tuần 1

Nghiên cứu các dịch vụ AWS Lambda, API Gateway, S3, DynamoDB và CloudWatch; thiết kế kiến trúc Serverless, chuẩn bị dữ liệu FAQ, triển khai nền tảng trên AWS Academy Learner Lab và kiểm thử kết nối giữa các thành phần.

Link báo cáo tuần 1: https://github.com/khoalkopwk-ship-it/Build_Chatbot_Cloud/blob/main/docs/week1-report.md

## 3. Công việc và kết quả thực hiện

### 3.1. Đặng Nguyễn Minh Khoa (24110253)

**Công việc 1: Nghiên cứu và thiết kế kiến trúc Serverless (4 giờ – 100%)**

- Nghiên cứu chức năng của AWS Lambda, API Gateway, Amazon S3 và DynamoDB.
- Thiết kế kiến trúc tổng thể và sơ đồ luồng xử lý.
- Xác định cách giao tiếp giữa các dịch vụ trong hệ thống.

Minh chứng:

Sơ đồ kiến trúc hệ thống – Architectural https://github.com/khoalkopwk-ship-it/Build_Chatbot_Cloud/blob/main/architecture/Architectural.png

**Công việc 2: Rà soát cấu trúc và nội dung dữ liệu FAQ (1 giờ – 100%)**

- Kiểm tra cấu trúc JSON và các trường dữ liệu.
- Rà soát danh sách 24 câu hỏi FAQ phục vụ kiểm thử.

Minh chứng:

Ảnh kiểm tra nội dung FAQ JSON https://github.com/khoalkopwk-ship-it/Build_Chatbot_Cloud/blob/main/screenshots/week1/Check_FAQ_JSON_content.png

**Công việc 3: Kiểm tra quyền IAM và xây dựng Lambda (2 giờ – 100%)**

- Kiểm tra LabRole trong AWS Learner Lab.
- Xây dựng Lambda Python đọc FAQ từ S3 và ghi bản ghi kiểm thử vào DynamoDB.
- Sử dụng biến môi trường để cấu hình tài nguyên.

Minh chứng:

- Ảnh kiểm tra LabRole https://github.com/khoalkopwk-ship-it/Build_Chatbot_Cloud/blob/main/screenshots/week1/Kiem_tra_quyen_LabRole_trong_IAM.png
- Mã nguồn Lambda https://github.com/khoalkopwk-ship-it/Build_Chatbot_Cloud/blob/main/backend/lambda_function.py

**Công việc 4: Kết nối API Gateway và kiểm thử API (2 giờ – 100%)**

- Cấu hình route `POST /chat` thông qua API Gateway.
- Thực hiện gửi HTTP POST bằng PowerShell.
- Kiểm tra mã trạng thái HTTP và nội dung JSON phản hồi.

Kết quả: API trả về HTTP 200 và số lượng 24 FAQ.

Minh chứng:

- Ảnh kiểm thử API PowerShell https://github.com/khoalkopwk-ship-it/Build_Chatbot_Cloud/blob/main/screenshots/week1/Test_API_PowerShell.png
- Script kiểm thử API https://github.com/khoalkopwk-ship-it/Build_Chatbot_Cloud/blob/main/scripts/Kiem_thu_API_Powershell.sh

**Tổng thời gian: 9 giờ.**

### 3.2. Ngô Anh Bằng (24110166)

**Công việc 1: Triển khai S3 lưu dữ liệu FAQ (2 giờ – 100%)**

- Cấu hình bucket S3 lưu trữ dữ liệu FAQ.
- Bật Block Public Access nhằm hạn chế truy cập công khai.
- Upload file `faq.json` lên S3.

Minh chứng:

- Ảnh cấu hình Block Public Access https://github.com/khoalkopwk-ship-it/Build_Chatbot_Cloud/blob/main/screenshots/week1/Enable_Block_Public_Access_for_FAQ_bucket.png
- Ảnh upload FAQ lên S3 https://github.com/khoalkopwk-ship-it/Build_Chatbot_Cloud/blob/main/screenshots/week1/Upload_FAQ_JSON_to_S3.png

**Công việc 2: Xây dựng và triển khai website tĩnh trên S3 (2 giờ – 100%)**

- Chuẩn bị giao diện HTML/CSS phục vụ kiểm thử.
- Cấu hình S3 Static Website Hosting.
- Cấu hình bucket policy để website có thể được truy cập công khai.
- Kiểm tra giao diện website trên trình duyệt.

Minh chứng:

- Mã nguồn giao diện https://github.com/khoalkopwk-ship-it/Build_Chatbot_Cloud/blob/main/frontend/index.html
- Ảnh cấu hình Static Website Hosting https://github.com/khoalkopwk-ship-it/Build_Chatbot_Cloud/blob/main/screenshots/week1/Enable_S3_static_website_hosting.png
- Ảnh cấu hình Bucket Policy https://github.com/khoalkopwk-ship-it/Build_Chatbot_Cloud/blob/main/screenshots/week1/Add_S3_website_bucket_policy.png
- Ảnh giao diện website https://github.com/khoalkopwk-ship-it/Build_Chatbot_Cloud/blob/main/screenshots/week1/Check_S3_website_interface.png

**Công việc 3: Tạo bảng DynamoDB lưu nhật ký (2 giờ – 100%)**

- Tạo bảng `course-faq-question-logs`.
- Thiết lập partition key `request_id` kiểu String.
- Chuẩn bị bảng để lưu kết quả kiểm thử hạ tầng.

Minh chứng:

Ảnh tạo bảng DynamoDB https://github.com/khoalkopwk-ship-it/Build_Chatbot_Cloud/blob/main/screenshots/week1/Create_DynamoDB_table.png

**Công việc 4: Kiểm thử kết nối Lambda, S3 và DynamoDB (2 giờ – 100%)**

- Thực hiện test event trên AWS Lambda.
- Kiểm tra Lambda đọc dữ liệu FAQ từ S3.
- Kiểm tra việc ghi và truy xuất bản ghi trong DynamoDB.

Kết quả: Lambda trả về HTTP 200, đọc được 24 FAQ và có bản ghi kiểm thử thành công trên DynamoDB.

Minh chứng:

- Ảnh kiểm thử Lambda https://github.com/khoalkopwk-ship-it/Build_Chatbot_Cloud/blob/main/screenshots/week1/Test_Lambda_read_S3_and_write_DynamoDB.png
- Ảnh kiểm tra nhật ký DynamoDB https://github.com/khoalkopwk-ship-it/Build_Chatbot_Cloud/blob/main/screenshots/week1/Check_logs_in_DynamoDB.png

**Công việc 5: Gắn tag tài nguyên và cập nhật tài liệu (1 giờ – 100%)**

- Gắn tag quản lý tài nguyên cho các bucket S3.
- Tổng hợp kết quả thực hiện và cập nhật báo cáo trên GitHub.

Minh chứng:

- Ảnh gắn tag bucket FAQ https://github.com/khoalkopwk-ship-it/Build_Chatbot_Cloud/blob/main/screenshots/week1/Add_tags_for_S3_FAQ_bucket.png
- Ảnh gắn tag bucket website https://github.com/khoalkopwk-ship-it/Build_Chatbot_Cloud/blob/main/screenshots/week1/Add_tags_for_S3_website_bucket.png
- Báo cáo tuần 1 trên GitHub https://github.com/khoalkopwk-ship-it/Build_Chatbot_Cloud/blob/main/docs/week1-report.md

**Tổng thời gian: 9 giờ.**

## 4. Tổng hợp phân công

| MSSV | Số công việc | Hoàn thành | Số giờ |
|---|---:|---:|---:|
| 24110253 | 4 | 100% | 9 |
| 24110166 | 5 | 100% | 9 |
| **Tổng** | **9** | | **18** |

## 5. Kết quả đạt được

Trong tuần 1, nhóm đã chuẩn bị bộ dữ liệu 24 FAQ, xây dựng mã nguồn Lambda, triển khai website tĩnh trên S3, cấu hình DynamoDB và kiểm thử kết nối hạ tầng thông qua API Gateway.

Kết quả kiểm thử API và Lambda đều trả HTTP 200. DynamoDB đã ghi nhận bản ghi kiểm thử thành công.

Chức năng tìm kiếm từ khóa/TF-IDF và trả lời FAQ thực tế chưa được triển khai trong tuần 1.

## 6. Kế hoạch tuần 2

- Xây dựng thuật toán tìm kiếm FAQ bằng từ khóa hoặc TF-IDF.
- Hoàn thiện xử lý câu hỏi trong Lambda.
- Tích hợp giao diện website với API Gateway.
- Kiểm thử các trường hợp câu hỏi khớp, không khớp và dữ liệu không hợp lệ.
- Hoàn thiện ghi nhật ký truy vấn và giám sát CloudWatch.

## 7. Kết luận

Nhóm Serverless đã xây dựng và kiểm thử nền tảng ban đầu của hệ thống chatbot FAQ trên AWS Academy Learner Lab. Các công việc được phân chia theo nhiệm vụ và có liên kết mã nguồn hoặc ảnh minh chứng cụ thể trên GitHub, làm cơ sở triển khai chức năng chatbot trong tuần tiếp theo.

## 8. Quy tắc tên tài nguyên và cấu hình

- Website endpoint: http://course-faq-web-24110253-24110166.s3-website-us-east-1.amazonaws.com
- API Invoke URL: https://ts6153n8b5.execute-api.us-east-1.amazonaws.com
- API route: POST /chat; payload 2.0; stage $default, auto-deploy
- CORS allowed origin: http://course-faq-web-24110253-24110166.s3-website-us-east-1.amazonaws.com
- FAQ key: faq/faq.json
- Lambda runtime / architecture / memory / timeout: Python 3.12 / x86_64 / 128 MB / 10 giây
- Execution role: LabRole
- Environment: FAQ_BUCKET=course-faq-data-24110253-24110166, FAQ_KEY=faq/faq.json, LOG_TABLE=course-faq-question-logs
