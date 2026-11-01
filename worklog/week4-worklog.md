# NHẬT KÝ CÔNG VIỆC TUẦN 4 (WORKLOG WEEK 4) — NHÓM SERVERLESS

**Môn học:** Điện toán đám mây  
**Mã lớp học phần:** `CLCO332779_05UTExMC`  
**Giảng viên hướng dẫn:** Huỳnh Xuân Phụng  
**Repository:** https://github.com/khoalkopwk-ship-it/Build_Chatbot_Cloud  
**Nhóm:** Serverless (2 thành viên)

---

## 1. Bảng Tổng Hợp Giờ Làm Việc Thực Tế

| Thành viên | MSSV | Vai trò | Giờ kế hoạch | Giờ thực tế | Phân bổ các ngày trong tuần | Trạng thái |
|---|:---:|---|:---:|:---:|:---:|:---:|
| **Đặng Nguyễn Minh Khoa** | 24110253 | Nhóm trưởng | 8h | 10.0h | 28/10, 29/10, 30/10, 31/10 | Hoàn thành |
| **Ngô Anh Bằng** | 24110166 | Thành viên | 8h | 10.5h | 27/10, 28/10, 30/10, 31/10, 01/11 | Hoàn thành |

---

## 2. Chi Tiết Nhật Ký Công Việc Từng Thành Viên

### 2.1. Ngô Anh Bằng (MSSV: 24110166 — GitHub: `bawgitne`)

| Ngày | Khung giờ (UTC+7) | Số giờ | Nội dung công việc thực tế | Minh chứng / Sản phẩm |
|:---:|:---:|:---:|---|---|
| **27/10/2026** | 14:00 – 16:00 | 2.0h | Truy cập AWS Console S3 bucket `course-faq-data-24110253`, tải bản sao lưu `faq (1).json` (24 FAQ). Chuẩn bị kho dữ liệu mở rộng 50 FAQ (`data/faq.json`, 26.2 KB) và tải lên S3. Chụp 2 ảnh minh chứng S3. | Commit [`0c3397f`](https://github.com/khoalkopwk-ship-it/Build_Chatbot_Cloud/commit/0c3397f), [`Week4_S3_Backup.png`](https://github.com/khoalkopwk-ship-it/Build_Chatbot_Cloud/blob/main/screenshots/week4/Week4_S3_Backup.png), [`Week4_S3_FAQ50_Upload.png`](https://github.com/khoalkopwk-ship-it/Build_Chatbot_Cloud/blob/main/screenshots/week4/Week4_S3_FAQ50_Upload.png) |
| **28/10/2026** | 14:30 – 17:00 | 2.5h | Thao tác trên Lambda `course-faq-lambda` và CloudWatch: kiểm tra cấu hình RAM 128 MB, biến môi trường, tạo Test Event `Week4_Test_Exact_FAQ`. Thực hiện 3 bài test thực tế (câu khớp FAQ017, câu không khớp, câu rỗng). Đối soát log CloudWatch và đồ thị giám sát Metrics. Chụp 8 ảnh minh chứng và soạn tài liệu `docs/week4/evidence-index.md`. | Commit [`0e4af0f`](https://github.com/khoalkopwk-ship-it/Build_Chatbot_Cloud/commit/0e4af0f), [8 ảnh `screenshots/week4/`](https://github.com/khoalkopwk-ship-it/Build_Chatbot_Cloud/tree/main/screenshots/week4), [`docs/week4/evidence-index.md`](https://github.com/khoalkopwk-ship-it/Build_Chatbot_Cloud/blob/main/docs/week4/evidence-index.md) |
| **30/10/2026** | 14:00 – 15:30 | 1.5h | Kiểm thử tương tác giao diện website tĩnh trên S3 (`course-faq-web-24110253`), kiểm tra API Gateway `/chat` phản hồi câu hỏi mới FAQ034 ("AWS Lambda là gì?") đạt `faqCount=50`, đối soát RequestId được ghi nhận chính xác vào DynamoDB table `CourseFAQQueryLogs`. Kiểm tra giao diện quản trị chi phí AWS Cost Explorer / Billing và ngân sách AWS Academy Learner Lab. | RequestId xác thực, đối soát logs DynamoDB, [`Week4_AWS_Cost_or_Usage.png`](https://github.com/khoalkopwk-ship-it/Build_Chatbot_Cloud/blob/main/screenshots/week4/Week4_AWS_Cost_or_Usage.png), [`Week4_AWS_Learner_Lab_Budget.png`](https://github.com/khoalkopwk-ship-it/Build_Chatbot_Cloud/blob/main/screenshots/week4/Week4_AWS_Learner_Lab_Budget.png) |
| **31/10/2026** | 09:00 – 11:00 | 2.0h | Viết tài liệu báo cáo tổng kết Tuần 4 (`docs/week4-report.md`), tổng hợp nhật ký công việc cá nhân và nhóm (`worklog/week4-worklog.md`), cập nhật danh mục liên kết commit thật, kiểm tra tiêu chí nghiệm thu. | Commit B3, `docs/week4-report.md`, `worklog/week4-worklog.md` |
| **01/11/2026** | 14:00 – 16:30 | 2.5h | Thực hiện quy trình backup và dọn dẹp tài nguyên AWS sau khi hoàn tất demo: chạy `backup-before-cleanup.sh`, kiểm tra marker xác thực, chạy `cleanup-aws.sh --execute`, xác nhận token xóa `DELETE-COURSEFAQ-550609224402`, chạy `verify-cleanup.sh` đạt 9/9 absent. Lập biên bản nghiệm thu giải phóng tài nguyên. | [`docs/week4/cleanup-verification.txt`](https://github.com/khoalkopwk-ship-it/Build_Chatbot_Cloud/blob/main/docs/week4/cleanup-verification.txt), [`docs/week4/cleanup-evidence-template.md`](https://github.com/khoalkopwk-ship-it/Build_Chatbot_Cloud/blob/main/docs/week4/cleanup-evidence-template.md) |
| **Tổng cộng** | | **10.5h** | | |

---

### 2.2. Đặng Nguyễn Minh Khoa (MSSV: 24110253 — GitHub: `khoalkopwk-ship-it` / `Koha`)

| Ngày | Khung giờ (UTC+7) | Số giờ | Nội dung công việc thực tế | Minh chứng / Sản phẩm |
|:---:|:---:|:---:|---|---|
| **28/10/2026** | 09:00 – 11:00 | 2.0h | Xây dựng bộ dữ liệu kiểm thử độc lập 30 câu hỏi chuẩn hóa (`data/search-eval-week4.json`) cho kho 50 FAQ mới (cập nhật nhãn FAQ034 cho câu "AWS Lambda là gì?"). | `data/search-eval-week4.json` |
| **29/10/2026** | 10:00 – 12:00 | 2.0h | Viết script kiểm thử `scripts/week4/evaluate-final.py`, chạy thử nghiệm so sánh 4 mức ngưỡng (0.30, 0.45, 0.60, 0.70), ghi nhận tỷ lệ chính xác và phân tích lỗi. | `scripts/week4/evaluate-final.py`, `docs/week4/search-eval-final-results.json` |
| **29/10/2026** | 14:00 – 16:00 | 2.0h | Phát triển công cụ benchmark tự động `scripts/week4/benchmark-api.py`. Thực hiện đo đạc trực tiếp trên endpoint API Gateway thật (`https://tijvqgrltk.execute-api.us-east-1.amazonaws.com`) với 12 truy vấn liên tục. Tính toán các chỉ số thống kê độ trễ (Min, Max, Mean, Median p50, p90, p95, StdDev). | Commit [`bf50292`](https://github.com/khoalkopwk-ship-it/Build_Chatbot_Cloud/commit/bf50292), `scripts/week4/benchmark-api.py`, `docs/week4/benchmark-results.json` |
| **30/10/2026** | 14:00 – 16:00 | 2.0h | Soạn thảo tài liệu phân tích kỹ thuật chuyên sâu `docs/week4/performance-and-cost.md`: phân biệt độ trễ mạng Internet vs thời gian tính toán Lambda (cold start 7.5s, warm 303ms); phân tích mức tiêu thụ RAM (97 MB / 128 MB); đánh giá tối ưu hóa cấu hình 256 MB; phân tích chi phí lý thuyết và hạn chế SCP trong AWS Learner Lab. | Commit [`b0d4f8e`](https://github.com/khoalkopwk-ship-it/Build_Chatbot_Cloud/commit/b0d4f8e), `docs/week4/performance-and-cost.md` |
| **31/10/2026** | 15:00 – 17:00 | 2.0h | Xây dựng bộ script kiểm kê tài nguyên, sao lưu tự động và cơ chế dọn dẹp an toàn có bảo vệ 2 lớp (`scripts/week4/`). Viết tài liệu quy trình `cleanup-guide.md`, `cleanup-checklist.md` và mẫu biên bản nghiệm thu `cleanup-evidence-template.md`. | Commit [`25d4c87`](https://github.com/khoalkopwk-ship-it/Build_Chatbot_Cloud/commit/25d4c87), [`scripts/week4/`](https://github.com/khoalkopwk-ship-it/Build_Chatbot_Cloud/tree/main/scripts/week4), [`docs/week4/cleanup-guide.md`](https://github.com/khoalkopwk-ship-it/Build_Chatbot_Cloud/blob/main/docs/week4/cleanup-guide.md) |
| **Tổng cộng** | | **10.0h** | | |

---

## 3. Danh Sách Commit Tuần 4 Trên Repository

| Mã Commit | Tác giả thực hiện | Thời gian commit thực tế (UTC+7) | Nội dung tóm tắt | Liên kết commit |
|:---:|:---:|:---:|---|---|
| `0c3397f` | Ngô Anh Bằng | 2026-10-27 14:25:10 | `data(week4): expand FAQ from 24 to 50 and record S3 update` | [Commit 0c3397f](https://github.com/khoalkopwk-ship-it/Build_Chatbot_Cloud/commit/0c3397f) |
| `0e4af0f` | Ngô Anh Bằng | 2026-10-28 16:15:32 | `test(week4): add Lambda and CloudWatch baseline evidence` | [Commit 0e4af0f](https://github.com/khoalkopwk-ship-it/Build_Chatbot_Cloud/commit/0e4af0f) |
| `bf50292` | Đặng Nguyễn Minh Khoa | 2026-10-29 11:35:45 | `test(week4): add independent FAQ evaluation and API benchmark` | [Commit bf50292](https://github.com/khoalkopwk-ship-it/Build_Chatbot_Cloud/commit/bf50292) |
| `b0d4f8e` | Đặng Nguyễn Minh Khoa | 2026-10-30 15:42:19 | `docs(week4): analyze latency quality and AWS usage` | [Commit b0d4f8e](https://github.com/khoalkopwk-ship-it/Build_Chatbot_Cloud/commit/b0d4f8e) |
| `25d4c87` | Đặng Nguyễn Minh Khoa | 2026-10-31 16:45:20 | `ops(week4): add guarded AWS cleanup and verification` | [Commit 25d4c87](https://github.com/khoalkopwk-ship-it/Build_Chatbot_Cloud/commit/25d4c87) |
| `22943a3` | Ngô Anh Bằng | 2026-11-01 15:30:10 | `evidence(week4): record actual AWS cleanup verification` | [Xem minh chứng](https://github.com/khoalkopwk-ship-it/Build_Chatbot_Cloud/blob/main/docs/week4/cleanup-verification.txt) |
