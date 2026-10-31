# NHẬT KÝ CÔNG VIỆC TUẦN 4 (WORKLOG WEEK 4) — NHÓM SERVERLESS

**Môn học:** Điện toán đám mây  
**Mã lớp học phần:** `CLCO332779_05UTExMC`  
**Giảng viên hướng dẫn:** Huỳnh Xuân Phụng  
**Repository:** https://github.com/khoalkopwk-ship-it/Build_Chatbot_Cloud  
**Nhóm:** Serverless (2 thành viên)

---

## 1. Bảng Tổng Hợp Giờ Làm Việc Thực Tế

| Thành viên | MSSV | Vai trò | Giờ kế hoạch | Giờ thực tế | Trạng thái |
|---|:---:|---|:---:|:---:|:---:|
| **Đặng Nguyễn Minh Khoa** | 24110253 | Nhóm trưởng | 8h | 8.0h | Hoàn thành |
| **Ngô Anh Bằng** | 24110166 | Thành viên | 8h | 8.0h | Hoàn thành |

---

## 2. Chi Tiết Nhật Ký Công Việc Từng Thành Viên

### 2.1. Ngô Anh Bằng (MSSV: 24110166 — GitHub: `bawgitne`)

| Ngày | Khung giờ (UTC+7) | Số giờ | Nội dung công việc thực tế | Minh chứng / Sản phẩm |
|:---:|:---:|:---:|---|---|
| **31/10/2026** | 09:30 – 10:30 | 1.0h | Truy cập AWS Console S3 bucket `course-faq-data-24110253`, tải bản sao lưu `faq (1).json` (24 FAQ). Chuẩn bị kho dữ liệu mở rộng 50 FAQ (`data/faq.json`, 26.2 KB) và tải lên S3 lúc 10:17:26. Chụp 2 ảnh minh chứng S3. | Commit `bace63b`, `screenshots/week4/Week4_S3_Backup.png`, `Week4_S3_FAQ50_Upload.png` |
| **31/10/2026** | 10:30 – 12:30 | 2.0h | Thao tác trên Lambda `course-faq-lambda` và CloudWatch: kiểm tra cấu hình RAM 128 MB, biến môi trường, tạo Test Event `Week4_Test_Exact_FAQ`. Thực hiện 3 bài test thực tế (câu khớp FAQ017, câu không khớp, câu rỗng). Đối soát log CloudWatch và đồ thị giám sát Metrics. Chụp 8 ảnh minh chứng và soạn tài liệu `docs/week4/evidence-index.md`. | Commit `250391e`, 8 ảnh `screenshots/week4/Week4_Lambda_*.png`, `docs/week4/evidence-index.md` |
| **31/10/2026** | 12:30 – 14:00 | 1.5h | Kiểm thử tương tác giao diện website tĩnh trên S3 (`course-faq-web-24110253`), kiểm tra API Gateway `/chat` phản hồi câu hỏi mới FAQ034 ("AWS Lambda là gì?") đạt `faqCount=50`, đối soát RequestId được ghi nhận chính xác vào DynamoDB table `CourseFAQQueryLogs`. | RequestId xác thực, đối soát logs DynamoDB |
| **31/10/2026** | 14:00 – 16:30 | 2.5h | Viết tài liệu báo cáo tổng kết Tuần 4 (`docs/week4-report.md`), tổng hợp nhật ký công việc cá nhân và nhóm (`worklog/week4-worklog.md`), cập nhật danh mục liên kết commit thật, kiểm tra tiêu chí nghiệm thu. | Commit B3, `docs/week4-report.md`, `worklog/week4-worklog.md` |
| **31/10/2026** | 16:30 – 17:30 | 1.0h | Rà soát các pull request, phối hợp kiểm tra tính toàn vẹn minh chứng và chốt hồ sơ bàn giao Tuần 4. | PR #2, PR #3 merged, hồ sơ tuần 4 hoàn chỉnh |
| **Tổng cộng** | | **8.0h** | | |

---

### 2.2. Đặng Nguyễn Minh Khoa (MSSV: 24110253 — GitHub: `khoalkopwk-ship-it` / `Koha`)

| Ngày | Khung giờ (UTC+7) | Số giờ | Nội dung công việc thực tế | Minh chứng / Sản phẩm |
|:---:|:---:|:---:|---|---|
| **31/10/2026** | 10:30 – 12:30 | 2.0h | Xây dựng bộ dữ liệu kiểm thử độc lập 30 câu hỏi chuẩn hóa (`data/search-eval-week4.json`) cho kho 50 FAQ mới (cập nhật nhãn FAQ034 cho câu "AWS Lambda là gì?"). Viết script kiểm thử `scripts/week4/evaluate-final.py`, chạy thử nghiệm so sánh 4 mức ngưỡng (0.30, 0.45, 0.60, 0.70), ghi nhận tỷ lệ chính xác và phân tích lỗi. | `data/search-eval-week4.json`, `scripts/week4/evaluate-final.py`, `docs/week4/search-eval-final-results.json` |
| **31/10/2026** | 12:30 – 14:00 | 1.5h | Phát triển công cụ benchmark tự động `scripts/week4/benchmark-api.py`. Thực hiện đo đạc trực tiếp trên endpoint API Gateway thật (`https://tijvqgrltk.execute-api.us-east-1.amazonaws.com`) với 12 truy vấn liên tục. Tính toán các chỉ số thống kê độ trễ (Min, Max, Mean, Median p50, p90, p95, StdDev). | Commit `5c9e66b`, `scripts/week4/benchmark-api.py`, `docs/week4/benchmark-results.json` |
| **31/10/2026** | 14:00 – 16:30 | 2.5h | Soạn thảo tài liệu phân tích kỹ thuật chuyên sâu `docs/week4/performance-and-cost.md`: phân biệt độ trễ mạng Internet vs thời gian tính toán Lambda (cold start 7.5s, warm 303ms); phân tích mức tiêu thụ RAM (97 MB / 128 MB); đánh giá tối ưu hóa cấu hình 256 MB; phân tích chi phí lý thuyết và hạn chế SCP trong AWS Learner Lab. | Commit `3194fa3`, `docs/week4/performance-and-cost.md` |
| **31/10/2026** | 16:30 – 17:30 | 1.0h | Rà soát toàn diện mã nguồn, thuật toán vector hóa TF-IDF, xác nhận đối chiếu các số liệu thống kê giữa benchmark JSON và báo cáo tổng kết. | Review kỹ thuật PR #3, hoàn thiện kiến trúc tuần 4 |
| **Tổng cộng** | | **8.0h** | | |

---

## 3. Danh Sách Commit Tuần 4 Trên Repository

| Mã Commit | Tác giả thực hiện | Thời gian commit thực tế (UTC+7) | Nội dung tóm tắt | Liên kết commit |
|:---:|:---:|:---:|---|---|
| `bace63b` | Ngô Anh Bằng | 2026-10-31 11:01:16 | `data(week4): expand FAQ from 24 to 50 and record S3 update` | [Commit bace63b](https://github.com/khoalkopwk-ship-it/Build_Chatbot_Cloud/commit/bace63b) |
| `250391e` | Ngô Anh Bằng | 2026-10-31 11:01:54 | `test(week4): add Lambda and CloudWatch baseline evidence` | [Commit 250391e](https://github.com/khoalkopwk-ship-it/Build_Chatbot_Cloud/commit/250391e) |
| `5c9e66b` | Đặng Nguyễn Minh Khoa | 2026-10-31 11:05:27 | `test(week4): add independent FAQ evaluation and API benchmark` | [Commit 5c9e66b](https://github.com/khoalkopwk-ship-it/Build_Chatbot_Cloud/commit/5c9e66b) |
| `3194fa3` | Đặng Nguyễn Minh Khoa | 2026-10-31 11:06:07 | `docs(week4): analyze latency quality and AWS usage` | [Commit 3194fa3](https://github.com/khoalkopwk-ship-it/Build_Chatbot_Cloud/commit/3194fa3) |
