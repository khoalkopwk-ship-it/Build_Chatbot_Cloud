# BIÊN BẢN NGHIỆM THU CLEANUP VÀ GIẢI PHÓNG TÀI NGUYÊN AWS — TUẦN 4

> **TRẠNG THÁI: ĐÃ HOÀN TẤT & ĐÃ KIỂM CHỨNG (PASSED 9/9)**  
> Toàn bộ tài nguyên phục vụ dự án Chatbot Serverless trên AWS Academy Learner Lab đã được sao lưu toàn diện và dọn dẹp sạch sẽ theo đúng thứ tự tháo dỡ quy chuẩn kết thúc môn học.

- **Dự án:** CourseFAQChatbot — Nhóm Serverless.
- **Account xác minh:** `550609224402` (AWS Academy Learner Lab).
- **Region:** `us-east-1` (US East - N. Virginia).
- **Ngày và giờ chạy (UTC+7):** 11:33:53 ngày 04/11/2026 (UTC: 2026-11-04T04:33:53Z).
- **Người chạy cleanup và tài khoản GitHub:** Ngô Anh Bằng (`bawgitne` — MSSV: 24110166).
- **Người kiểm tra độc lập:** Đặng Nguyễn Minh Khoa (`khoalkopwk-ship-it` / `Koha` — MSSV: 24110253).
- **Video demo đã hoàn tất và sao lưu:** Đã quay video demo hỏi đáp + đối soát log thực tế dưới 10 phút, lưu trữ tại [Google Drive Demo Folder](https://drive.google.com/drive/folders/1sHl8H4BfK-NmiGBEJrDkyx8ODl4nMWLm?usp=sharing).
- **Thứ tự tháo dỡ hạ tầng chuẩn:** **API Gateway → Lambda → DynamoDB → S3 (Data & Web) → CloudWatch (Alarm, Dashboard, Logs)**.
- **Backup trước khi xóa:** Chạy `backup-before-cleanup.sh`, kiểm tra xác thực 50 FAQ, lưu trữ an toàn tại `/home/cloudshell-user/coursefaq-backup-20261104T032652Z.tar.gz`.
- **Lệnh chuẩn bị:** `bash scripts/week4/inventory-aws.sh`; `bash scripts/week4/backup-before-cleanup.sh`.
- **Lệnh cleanup:** `bash scripts/week4/cleanup-aws.sh --execute "/home/cloudshell-user/coursefaq-backup-20261104T032652Z"` (Token: `DELETE-COURSEFAQ-550609224402`).
- **Lệnh kiểm chứng:** `bash scripts/week4/verify-cleanup.sh`.
- **Kết quả kiểm chứng:** `absent=9/9; present=0` (Xác nhận 100% tài nguyên đã được giải phóng hoàn toàn).
- **File nhật ký kiểm chứng:** [`cleanup-verification.txt`](https://github.com/khoalkopwk-ship-it/Build_Chatbot_Cloud/blob/main/docs/week4/cleanup-verification.txt).

| STT | Thứ tự xóa | Dịch vụ AWS | Tên resource | Tình trạng trước khi xóa | Kết quả kiểm chứng (verify-cleanup) | Người xác nhận |
|:---:|:---:|---|---|---|:---:|:---:|
| 01 | 1 | API Gateway HTTP API | `tijvqgrltk` | 2 routes (`POST /chat`, `$default`) | **PASS (ABSENT)** | Đặng Nguyễn Minh Khoa |
| 02 | 2 | AWS Lambda | `course-faq-lambda` | Runtime Python 3.13, RAM 128 MB | **PASS (ABSENT)** | Đặng Nguyễn Minh Khoa |
| 03 | 3 | Amazon DynamoDB | `CourseFAQQueryLogs` | Bảng log truy vấn Partition Key `requestId` | **PASS (ABSENT)** | Đặng Nguyễn Minh Khoa |
| 04 | 4 | Amazon S3 (Data) | `course-faq-data-24110253` | Chứa `faq.json` (50 FAQ) | **PASS (ABSENT)** | Đặng Nguyễn Minh Khoa |
| 05 | 5 | Amazon S3 (Website) | `course-faq-web-24110253` | Static website hosting frontend (4 files) | **PASS (ABSENT)** | Đặng Nguyễn Minh Khoa |
| 06 | 6 | CloudWatch Alarm | `CourseFAQ-ApplicationErrors` | Alarm cảnh báo lỗi ứng dụng | **PASS (ABSENT)** | Đặng Nguyễn Minh Khoa |
| 07 | 7 | CloudWatch Dashboard | `CourseFAQ-Week3-Dashboard` | Dashboard giám sát hiệu năng | **PASS (ABSENT)** | Đặng Nguyễn Minh Khoa |
| 08 | 8 | CloudWatch Logs (Lambda) | `/aws/lambda/course-faq-lambda` | Log stream thực thi hàm Lambda | **PASS (ABSENT)** | Đặng Nguyễn Minh Khoa |
| 09 | 9 | CloudWatch Logs (API) | `/aws/apigateway/course-faq-api` | Access log API Gateway | **PASS (ABSENT)** | Đặng Nguyễn Minh Khoa |

## Minh chứng ảnh chụp dọn dẹp thực tế (04/11/2026)

1. [`Week4_Cleanup_Before.png`](https://github.com/khoalkopwk-ship-it/Build_Chatbot_Cloud/blob/main/screenshots/week4/Week4_Cleanup_Before.png): Thao tác pre-cleanup và chạy sao lưu `backup-before-cleanup.sh` trên AWS CloudShell, hiển thị Account `550609224402`, Region `us-east-1`, Session sinh viên và thời gian `03:26:48 UTC (10:26 UTC+7) ngày 04/11/2026`.
2. [`Week4_Cleanup_Backup_Detail.png`](https://github.com/khoalkopwk-ship-it/Build_Chatbot_Cloud/blob/main/screenshots/week4/Week4_Cleanup_Backup_Detail.png): Nhật ký kiểm tra gói sao lưu `coursefaq-backup-20261104T032652Z.tar.gz` đạt chuẩn đầy đủ 50 FAQ (`BACKUP_OK`).
3. [`Week4_Cleanup_Execution_Order.png`](https://github.com/khoalkopwk-ship-it/Build_Chatbot_Cloud/blob/main/screenshots/week4/Week4_Cleanup_Execution_Order.png): Thực thi lệnh xóa tuần tự theo đúng thứ tự an toàn: API Gateway → Lambda → DynamoDB → S3 FAQ → S3 Website → CloudWatch lúc `04:29:45 UTC (11:29 UTC+7) ngày 04/11/2026`.
4. [`Week4_Cleanup_After.png`](https://github.com/khoalkopwk-ship-it/Build_Chatbot_Cloud/blob/main/screenshots/week4/Week4_Cleanup_After.png): Kết quả kiểm chứng độc lập `verify-cleanup.sh` lúc `04:33:53 UTC (11:33 UTC+7) ngày 04/11/2026` xác nhận toàn bộ 9/9 tài nguyên đã bị xóa sạch (`VERIFY SUMMARY: 9/9 ABSENT`).

## Kết luận cleanup

Đã kiểm chứng độc lập bằng lệnh `verify-cleanup.sh` từ AWS CLI thật: **Toàn bộ 9 tài nguyên chính của dự án đã bị xóa sạch hoàn toàn (absent=9/9)**. Môi trường AWS Academy Learner Lab không còn bất kỳ thành phần nào đang chạy ngầm, bảo toàn nguyên vẹn định mức ngân sách $100 của phòng thực hành.
