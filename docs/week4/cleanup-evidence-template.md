# BIÊN BẢN NGHIỆM THU CLEANUP VÀ GIẢI PHÓNG TÀI NGUYÊN AWS — TUẦN 4

> **TRẠNG THÁI: ĐÃ HOÀN TẤT & ĐÃ KIỂM CHỨNG (PASSED 9/9)**  
> Toàn bộ tài nguyên phục vụ dự án Chatbot Serverless trên AWS Academy Learner Lab đã được sao lưu toàn diện và dọn dẹp sạch sẽ theo đúng quy trình bàn giao kết thúc môn học.

- **Dự án:** CourseFAQChatbot — Nhóm Serverless.
- **Account xác minh:** `550609224402` (AWS Academy Learner Lab).
- **Region:** `us-east-1` (US East - N. Virginia).
- **Ngày và giờ chạy (UTC+7):** 15:42:15 ngày 01/11/2026.
- **Người chạy cleanup và tài khoản GitHub:** Ngô Anh Bằng (`bawgitne` — MSSV: 24110166).
- **Người kiểm tra độc lập:** Đặng Nguyễn Minh Khoa (`khoalkopwk-ship-it` / `Koha` — MSSV: 24110253).
- **Video demo đã hoàn tất và sao lưu:** Đã hoàn tất và lưu trữ an toàn ngoài môi trường AWS Learner Lab.
- **Backup:** Đã chạy script `backup-before-cleanup.sh`, sao lưu toàn bộ `faq.json`, mã nguồn tĩnh S3 website, cấu hình Lambda, API Gateway và bản ghi log truy vấn từ DynamoDB vào thư mục cục bộ riêng tư an toàn.
- **Lệnh chuẩn bị:** `bash scripts/week4/inventory-aws.sh`; `bash scripts/week4/backup-before-cleanup.sh`.
- **Lệnh cleanup:** `bash scripts/week4/cleanup-aws.sh --execute "$HOME/coursefaq-backup-20261101T083000Z"`.
- **Lệnh kiểm chứng:** `bash scripts/week4/verify-cleanup.sh`.
- **Kết quả kiểm chứng:** `absent=9/9; present=0` (Xác nhận 100% tài nguyên đã được giải phóng).
- **File nhật ký kiểm chứng:** [`cleanup-verification.txt`](https://github.com/khoalkopwk-ship-it/Build_Chatbot_Cloud/blob/main/docs/week4/cleanup-verification.txt).

| STT | Dịch vụ AWS | Tên resource | Tình trạng trước khi xóa | Kết quả kiểm chứng (verify-cleanup) | Người xác nhận |
|:---:|---|---|---|:---:|:---:|
| 01 | API Gateway HTTP API | `tijvqgrltk` | 2 routes (`POST /chat`, `$default`) | **PASS (ABSENT)** | Đặng Nguyễn Minh Khoa |
| 02 | AWS Lambda | `course-faq-lambda` | Runtime Python 3.13, RAM 128 MB | **PASS (ABSENT)** | Đặng Nguyễn Minh Khoa |
| 03 | Amazon DynamoDB | `CourseFAQQueryLogs` | Bảng log truy vấn Partition Key `requestId` | **PASS (ABSENT)** | Đặng Nguyễn Minh Khoa |
| 04 | Amazon S3 (Data) | `course-faq-data-24110253` | Chứa `faq.json` (50 FAQ) | **PASS (ABSENT)** | Đặng Nguyễn Minh Khoa |
| 05 | Amazon S3 (Website) | `course-faq-web-24110253` | Static website hosting frontend | **PASS (ABSENT)** | Đặng Nguyễn Minh Khoa |
| 06 | CloudWatch Alarm | `CourseFAQ-ApplicationErrors` | Alarm cảnh báo lỗi ứng dụng | **PASS (ABSENT)** | Đặng Nguyễn Minh Khoa |
| 07 | CloudWatch Dashboard | `CourseFAQ-Week3-Dashboard` | Dashboard giám sát hiệu năng | **PASS (ABSENT)** | Đặng Nguyễn Minh Khoa |
| 08 | CloudWatch Logs (Lambda) | `/aws/lambda/course-faq-lambda` | Log stream thực thi hàm Lambda | **PASS (ABSENT)** | Đặng Nguyễn Minh Khoa |
| 09 | CloudWatch Logs (API) | `/aws/apigateway/course-faq-api` | Access log API Gateway | **PASS (ABSENT)** | Đặng Nguyễn Minh Khoa |

## Kết luận cleanup

Đã kiểm chứng độc lập bằng lệnh `verify-cleanup.sh` từ AWS CLI thật: **Toàn bộ 9 tài nguyên chính của dự án đã bị xóa sạch hoàn toàn (absent=9/9)**. Môi trường AWS Academy Learner Lab không còn bất kỳ thành phần nào đang chạy ngầm, bảo toàn nguyên vẹn định mức ngân sách $100 của phòng thực hành.

## Ghi nhận AI

ChatGPT hỗ trợ xây dựng quy trình kiểm soát rủi ro 2 lớp trong kịch bản cleanup. Cả hai sinh viên đã tự tay kiểm tra, sao lưu dữ liệu và thực thi lệnh kiểm chứng trên hạ tầng đám mây thực tế.
