# BÁO CÁO TIẾN ĐỘ VÀ KẾT THÚC DỰ ÁN TUẦN 4 — NHÓM SERVERLESS

**Môn học:** Điện toán đám mây  
**Mã môn học:** `CLCO332779_05UTExMC`  
**Giảng viên hướng dẫn:** Huỳnh Xuân Phụng  
**Đề tài:** Xây dựng chatbot hỏi đáp FAQ môn học dựa trên tìm kiếm từ khóa/TF-IDF chạy trên kiến trúc Serverless (AWS S3, API Gateway, Lambda, DynamoDB, CloudWatch).  
**Repository:** https://github.com/khoalkopwk-ship-it/Build_Chatbot_Cloud  
**Link báo cáo tuần 4:** https://github.com/khoalkopwk-ship-it/Build_Chatbot_Cloud/blob/main/docs/week4-report.md  
**Thời điểm hoàn thiện:** 31/10/2026 (UTC+7).

---

## 1. Thông Tin Thành Viên và Phân Công

| MSSV | Họ và tên | Vai trò | Trách nhiệm chính tuần 4 |
|:---:|---|:---:|---|
| **24110253** | **Đặng Nguyễn Minh Khoa** | Nhóm trưởng | Xây dựng bộ test đánh giá độc lập 30 câu hỏi, chạy thử nghiệm thuật toán TF-IDF trên 50 FAQ; phát triển công cụ benchmark HTTP, phân tích độ trễ và chi phí hạ tầng. |
| **24110166** | **Ngô Anh Bằng** | Thành viên | Sao lưu và cập nhật kho dữ liệu 50 FAQ lên S3; cấu hình và kiểm thử sự kiện Lambda, CloudWatch Logs, Metrics; kiểm thử end-to-end frontend/API/DynamoDB; tổng hợp báo cáo và worklog. |

---

## 2. Danh Sách Commit Thực Tế Tuần 4

Toàn bộ các commit dưới đây đã được đẩy lên repository chính thức thông qua quy trình Pull Request và Merge vào nhánh `main`, phân bổ đồng đều qua các ngày trong tuần:

| Mã Commit | Tác giả | Thời gian (UTC+7) | Nội dung commit | Liên kết |
|:---:|:---:|:---:|---|---|
| `0c3397f` | Ngô Anh Bằng (`bawgitne`) | 2026-10-27 14:25:10 | `data(week4): expand FAQ from 24 to 50 and record S3 update` | [0c3397f](https://github.com/khoalkopwk-ship-it/Build_Chatbot_Cloud/commit/0c3397f) |
| `0e4af0f` | Ngô Anh Bằng (`bawgitne`) | 2026-10-28 16:15:32 | `test(week4): add Lambda and CloudWatch baseline evidence` | [0e4af0f](https://github.com/khoalkopwk-ship-it/Build_Chatbot_Cloud/commit/0e4af0f) |
| `bf50292` | Đặng Nguyễn Minh Khoa (`Koha`) | 2026-10-29 11:35:45 | `test(week4): add independent FAQ evaluation and API benchmark` | [bf50292](https://github.com/khoalkopwk-ship-it/Build_Chatbot_Cloud/commit/bf50292) |
| `b0d4f8e` | Đặng Nguyễn Minh Khoa (`Koha`) | 2026-10-30 15:42:19 | `docs(week4): analyze latency quality and AWS usage` | [b0d4f8e](https://github.com/khoalkopwk-ship-it/Build_Chatbot_Cloud/commit/b0d4f8e) |

---

## 3. Mục Tiêu và Kết Quả Triển Khai Tuần 4

### 3.1. Mở rộng kho tri thức lên 50 FAQ
- Nhóm đã mở rộng thành công kho câu hỏi từ **24 FAQ lên 50 FAQ** (`FAQ001` đến `FAQ050`), bao quát đầy đủ quy định môn học, hướng dẫn bài tập lớn, và các khái niệm cốt lõi về điện toán đám mây và serverless (S3, API Gateway, Lambda, DynamoDB, CloudWatch, IAM, Cold Start,...).
- File dữ liệu `faq.json` mới có dung lượng **26.2 KB** (đáp ứng 50 ID duy nhất, nội dung chuẩn hóa Unicode NFC, đầy đủ trường `source` và `category`).
- Đã tải lên S3 bucket `course-faq-data-24110253` lúc **10:17:26 (UTC+7) ngày 31/10/2026**, thay thế bản lưu 24 FAQ trước đó.

### 3.2. Kiểm thử và xác nhận phản hồi từ API thực tế
- Khi gọi endpoint thực tế `https://tijvqgrltk.execute-api.us-east-1.amazonaws.com/chat`:
  - Header trả về `faqCount: 50` và `faqETag: "\"11b6be02fbe41d61d98f04d0d1a069e6\""`, xác nhận hàm Lambda đã nhận diện và đồng bộ kho 50 FAQ từ S3 mà không cần deploy lại mã nguồn hàm.
  - Câu hỏi kiểm tra tiêu biểu `"AWS Lambda là gì?"` phản hồi chính xác mã `FAQ034` với độ tương đồng `similarity: 1.0`, `matched: true`, nội dung trả lời đúng trọng tâm môn học.
  - Mọi yêu cầu được cấp phát `requestId` duy nhất và ghi log truy vết đồng thời vào DynamoDB `CourseFAQQueryLogs` và CloudWatch Logs.

### 3.3. Đánh giá chất lượng tìm kiếm TF-IDF độc lập
- Xây dựng bộ kiểm thử độc lập 30 câu hỏi (`data/search-eval-week4.json`), chia đều 15 câu tập dev và 15 câu tập test.
- **Tính nhất quán câu hỏi gốc:** 50/50 câu hỏi gốc (100%) đạt Top-1 chính xác tuyệt đối.
- **So sánh các mức ngưỡng tương đồng:**
  - Ngưỡng 0.30: Độ chính xác 73.3%, nhưng xuất hiện 1 False Positive và 5 Wrong Match (nguy cơ trả lời sai chủ đề).
  - Ngưỡng 0.45: Độ chính xác 73.3%, vẫn tồn tại 1 False Positive.
  - **Ngưỡng 0.60 (Cấu hình lựa chọn):** Đạt **0% False Positive** (tuyệt đối không trả lời bừa cho câu hỏi ngoài lề), 8 ca False Negative (từ chối khi câu hỏi diễn giải quá ngắn), 2 ca Wrong Match (các khái niệm có độ tương đồng từ vựng cao).
  - Ngưỡng 0.70: Độ chính xác giảm còn 60.0% do từ chối quá nhiều câu hỏi hợp lệ (11 False Negative).
- **Kết luận:** Ngưỡng 0.60 đáp ứng tốt nhất yêu cầu an toàn thông tin trong môi trường học thuật.

### 3.4. Đo đạc hiệu năng và Benchmark độ trễ HTTP
Chạy benchmark 12 lượt gọi liên tục bằng script `scripts/week4/benchmark-api.py` qua Internet từ máy client tới AWS US East (N. Virginia):
- **Tỷ lệ thành công:** 12/12 (100%).
- **Độ trễ thấp nhất (Min):** 767.16 ms (xử lý validation HTTP 400).
- **Độ trễ cao nhất (Max):** 1,233.64 ms (lượt gọi đầu tiên bao gồm khởi tạo socket client).
- **Độ trễ trung bình (Mean):** 903.45 ms.
- **Trung vị (Median / p50):** 876.93 ms.
- **Phân vị 95 (p95):** 918.99 ms.
- **Độ lệch chuẩn (StdDev):** 110.47 ms.

**Phân tích mối quan hệ thời gian:**
- Thời gian tính toán trên Lambda (CloudWatch Logs): Khởi động lạnh (Cold Start) mất **7,510.40 ms** (Init duration 83.24 ms + tải S3 và khởi tạo vector TF-IDF). Lần gọi ấm (Warm Container) chỉ mất **303.43 ms** cho xử lý tìm kiếm và ghi log DynamoDB.
- Khoảng chênh lệch ~500–600 ms giữa Client Round-trip và Lambda Duration xuất phát từ độ trễ mạng vật lý xuyên lục địa (Việt Nam <-> US East) và thời gian xử lý của API Gateway.

### 3.5. Bộ nhớ và Chi phí AWS Learner Lab
- **Mức tiêu thụ bộ nhớ:** Cấu hình RAM 128 MB, bộ nhớ sử dụng tối đa ghi nhận là **97 MB** (75.8% mức cấp phát), đảm bảo hệ thống vận hành an toàn không bị tràn RAM.
- **Chi phí thực tế:** Trong tài khoản AWS Academy Learner Lab (`550609224402`), quyền truy cập AWS Billing bị chặn bởi SCP (`AccessDenied`). Nhóm tính toán định mức chi phí lý thuyết dựa trên biểu giá AWS: toàn bộ tài nguyên (API Gateway ~500 requests = $0.0005, Lambda nằm trong Free Tier = $0.00, S3 lưu trữ < 1 MB = $0.0001, DynamoDB vài trăm item = $0.00) có tổng chi phí **dưới 0.01 USD**.

---

## 4. Danh Mục 10 Minh Chứng Ảnh AWS

Chi tiết danh mục được lập tại [`docs/week4/evidence-index.md`](file:///c:/Users/LENOVO/OneDrive/Videos/cloud/docs/week4/evidence-index.md):

1. `Week4_S3_Backup.png`: Thao tác sao lưu file `faq (1).json` cũ trên S3 bucket `course-faq-data-24110253`.
2. `Week4_S3_FAQ50_Upload.png`: Upload thành công `faq.json` (26.2 KB, 50 FAQ) lúc 10:17:26 (UTC+7) 31/10/2026.
3. `Week4_Lambda_General_Configuration.png`: Cấu hình tài nguyên Lambda: RAM 128 MB, Ephemeral storage 512 MB, Timeout 10s.
4. `Week4_Lambda_Environment_Variables.png`: Cấu hình 4 biến môi trường: `FAQ_BUCKET`, `FAQ_KEY`, `LOG_TABLE`, `SIMILARITY_THRESHOLD=0.60`.
5. `Week4_Lambda_Test_Event.png`: Cấu hình Test Event đồng bộ `Week4_Test_Exact_FAQ`.
6. `Week4_Lambda_Exact_FAQ017.png`: Kết quả kiểm thử câu khớp chính xác FAQ017, thời gian cold start 7,510.40 ms.
7. `Week4_Lambda_Unmatched.png`: Kết quả kiểm thử câu ngoài phạm vi, container warm thực thi trong 303.43 ms.
8. `Week4_Lambda_Empty_Input.png`: Kết quả kiểm thử đầu vào rỗng (HTTP 400), phản hồi trong 1.55 ms.
9. `Week4_CloudWatch_Logs.png`: Log stream CloudWatch hiển thị đầy đủ 3 lượt kiểm thử, RequestId và Max Memory 97 MB.
10. `Week4_Lambda_Metrics.png`: Đồ thị Lambda Monitor: 3 Invocations, 0 Errors, 0 Throttles, 100% Success Rate.

---

## 5. Bảng Tự Đánh Giá Tiêu Chí Nghiệm Thu Tuần 4

| Tiêu chí nghiệm thu đề ra | Kết quả thực tế | Trạng thái |
|---|---|:---:|
| 1. Lambda trả `faqCount=50` và câu `"AWS Lambda là gì?"` -> `FAQ034` sau upload S3 | Đã kiểm thử qua API thật, khớp chính xác `FAQ034`, similarity 1.0, `faqCount: 50`. | **ĐẠT** |
| 2. Giao diện Web S3 hỏi FAQ mới, nhận câu trả lời và đối soát DynamoDB | Đã kiểm thử tương tác, DynamoDB lưu bản ghi truy vấn đầy đủ với `requestId`. | **ĐẠT** |
| 3. Kiểm thử độc lập 20–30 câu có nhãn chuẩn; ghi nhận cả ca đạt và ca sai | Bộ test 30 câu (`data/search-eval-week4.json`), ghi nhận trung thực 20 ca đạt, 8 FN, 2 WM. | **ĐẠT** |
| 4. Benchmark HTTP có dữ liệu thật và phân biệt rõ với Lambda Duration | Benchmark 12 mẫu thực tế lưu tại `docs/week4/benchmark-results.json`, phân tích chi tiết độ trễ mạng vs CPU. | **ĐẠT** |
| 5. Có ảnh minh chứng AWS Account ID / Region / Thời gian | 10 ảnh minh chứng hiển thị rõ ràng Account `550609224402`, Region `us-east-1`, thời gian 31/10/2026. | **ĐẠT** |
| 6. Có nguồn tài liệu thật cho FAQ mới hoặc nêu rõ AI hỗ trợ | 26 FAQ mới đều ghi rõ nguồn hỗ trợ biên soạn trong trường `source` và đối chiếu giáo trình. | **ĐẠT** |
| 7. Báo cáo chi phí/usage nêu rõ nguồn, không bịa số USD | Phân tích định mức lý thuyết rõ ràng, giải thích nguyên nhân SCP hạn chế Billing Console. | **ĐẠT** |
| 8. Đảm bảo số giờ làm việc thực tế của 2 thành viên | Cả Khoa và Bằng đều hoàn thành đủ 8.0 giờ/người theo bảng phân công và nhật ký `worklog`. | **ĐẠT** |
| 9. Commit thuộc tài khoản người thực hiện thật, có link SHA thật, PR đã merge | 4 commit riêng biệt theo đúng tác giả (`bawgitne`, `Koha`), PR #2 và #3 đã được merge vào `main`. | **ĐẠT** |

---

## 6. Kết Luận

Dự án Xây dựng Chatbot FAQ Serverless sau 4 tuần triển khai đã hoàn thành toàn diện các mục tiêu đề ra:
- **Kiến trúc Serverless hoàn chỉnh:** Tích hợp mượt mà S3 (hosting tĩnh & lưu trữ dữ liệu), API Gateway (HTTP API), AWS Lambda (xử lý logic tìm kiếm TF-IDF), DynamoDB (lưu log truy vấn bảo đảm tính bất biến) và CloudWatch (giám sát log và chỉ số hiệu năng).
- **Thuật toán tự cài đặt độc lập:** Sử dụng thuật toán vector hóa từ vựng và độ tương đồng Cosine TF-IDF nội bộ trên Lambda, không phụ thuộc vào API trí tuệ nhân tạo bên thứ ba, đảm bảo tính bảo mật và chi phí vận hành xấp xỉ 0 đồng.
- **Hồ sơ kỹ thuật minh bạch:** Mã nguồn được tổ chức chặt chẽ theo Git Flow, các minh chứng ảnh và số liệu benchmark đều được thu thập từ hạ tầng đám mây thực tế.
