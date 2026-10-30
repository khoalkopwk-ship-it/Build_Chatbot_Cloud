# Phân Tích Hiệu Năng, Chất Lượng Tìm Kiếm và Chi Phí Tuần 4 — Nhóm Serverless

> **Người thực hiện:** Đặng Nguyễn Minh Khoa (`khoalkopwk-ship-it` / `Koha`)  
> **Thời điểm đánh giá:** 31/10/2026 (UTC+7)  
> **AWS Account ID:** `550609224402` | **Region:** `us-east-1` (N. Virginia)  
> **Mã nguồn/Dữ liệu đo:** `scripts/week4/benchmark-api.py`, `scripts/week4/evaluate-final.py`, `docs/week4/benchmark-results.json`, `docs/week4/search-eval-final-results.json`

---

## 1. Phân Tích Độ Trễ (Latency & Performance Analysis)

### 1.1. Bảng số liệu đo đạc thực tế

Từ kết quả benchmark 12 mẫu liên tục qua endpoint HTTP API Gateway `https://tijvqgrltk.execute-api.us-east-1.amazonaws.com` (đo trực tiếp từ client tại Việt Nam đến Region `us-east-1`):

| Chỉ số độ trễ | Giá trị đo được (Client Round-trip) | Ghi chú kỹ thuật |
|---|:---:|---|
| **Mẫu nhỏ nhất (Min)** | **767.16 ms** | Request kiểm thử validation rỗng (HTTP 400), trả lời ngay lập tức không qua xử lý TF-IDF. |
| **Mẫu lớn nhất (Max)** | **1,233.64 ms** | Request đầu tiên trong chuỗi kiểm thử, chịu ảnh hưởng kết nối socket ban đầu. |
| **Trung bình (Mean)** | **903.45 ms** | Mức độ trễ trung bình của các câu hỏi hợp lệ. |
| **Trung vị (p50 / Median)** | **876.93 ms** | 50% số lượt truy vấn hoàn thành dưới 877 ms. |
| **Phân vị 90 (p90)** | **902.89 ms** | 90% số lượt truy vấn hoàn thành dưới 903 ms. |
| **Phân vị 95 (p95)** | **918.99 ms** | 95% số lượt truy vấn hoàn thành dưới 919 ms. |
| **Độ lệch chuẩn (StdDev)** | **110.47 ms** | Độ trễ rất ổn định, không có hiện tượng jitter nghiêm trọng. |

### 1.2. Phân tích thành phần thời gian: Client Round-trip vs Lambda Duration

Cần phân biệt rõ hai khái niệm thời gian:
1. **Lambda Billed Duration (Thời gian xử lý nội bộ AWS):**
   - **Cold Start (Khởi động lạnh):** Đo được trong ảnh minh chứng `Week4_Lambda_Exact_FAQ017.png` là **7,510.40 ms** (Billed: 7,594 ms, Init duration: 83.24 ms). Nguyên nhân do Lambda phải khởi tạo môi trường Python 3.13, nạp SDK `boto3`, tải file `faq.json` (26.2 KB) từ S3 bucket và xây dựng ma trận từ vựng TF-IDF lần đầu tiên.
   - **Warm Execution (Thực thi khi container đã ấm):** Đo được trong ảnh minh chứng `Week4_Lambda_Unmatched.png` là **303.43 ms** (Billed: 304 ms). Khi container còn sống trong bộ nhớ, ma trận FAQ đã nạp sẵn, thời gian xử lý vector hóa và ghi log DynamoDB chỉ mất xấp xỉ ~300 ms.
   - **Validation Error:** Đo được trong `Week4_Lambda_Empty_Input.png` là **1.55 ms** (Billed: 2 ms).
2. **Client Round-trip Overhead (~500–600 ms):**
   - Khoảng cách địa lý từ Việt Nam tới US East (N. Virginia) tạo ra độ trễ mạng mạng đường truyền vật lý (RTT cáp quang biển) tối thiểu ~220–250 ms mỗi chiều (tổng cộng ~450–500 ms).
   - Thêm thời gian thiết lập TLS/HTTPS handshake và API Gateway chuyển tiếp sự kiện sang Lambda (~50–80 ms).
   - Do đó, khi Lambda chạy mất ~300 ms thì Client nhận kết quả sau ~870 ms là hoàn toàn hợp lý và phản ánh chính xác hạ tầng serverless xuyên lục địa.

---

## 2. Đánh Giá Chất Lượng Tìm Kiếm TF-IDF Trên 50 FAQ

### 2.1. Kiểm thử tính nhất quán (Top-1 Exact Consistency)
- Đã chạy kiểm thử với toàn bộ 50 câu hỏi gốc trong `data/faq.json`.
- **Kết quả:** **50/50 câu hỏi gốc (100%)** đều tìm về chính xác ID tương ứng ở vị trí Top-1 với độ tương đồng `similarity = 1.0`.

### 2.2. So sánh các ngưỡng tương đồng (`SIMILARITY_THRESHOLD`)

Tập kiểm thử độc lập gồm 30 câu (15 câu dev, 15 câu test) bao gồm câu hỏi khớp chính xác, câu hỏi không dấu, câu hỏi diễn giải, và các câu hỏi ngoài phạm vi môn học:

| Ngưỡng | Số ca đạt (Accuracy) | False Positive (FP) | False Negative (FN) | Wrong Match (WM) | Đánh giá kỹ thuật |
|:---:|:---:|:---:|:---:|:---:|---|
| **0.30** | 22/30 (73.3%) | 1 | 2 | 5 | Quá nhạy; nhận nhầm 1 câu ngoài lề và ghép sai chủ đề 5 câu do trùng một vài từ khóa chung. |
| **0.45** | 22/30 (73.3%) | 1 | 4 | 3 | Vẫn có 1 ca False Positive (trả lời bừa cho câu hỏi ngoài phạm vi). |
| **0.60** *(Đang chọn)* | **20/30 (66.7%)** | **0** | **8** | **2** | **Độ an toàn cao nhất (FP = 0):** Tuyệt đối không trả lời sai lệch cho các câu hỏi ngoài phạm vi. Chấp nhận 8 ca False Negative (từ chối khi câu hỏi diễn giải quá ngắn hoặc thiếu từ khóa cốt lõi). |
| **0.70** | 18/30 (60.0%) | 0 | 11 | 1 | Quá khắt khe; bỏ sót nhiều câu hỏi hợp lệ của sinh viên nếu câu chữ không khớp gần như hoàn toàn. |

> **Kết luận lựa chọn ngưỡng:** Ngưỡng `0.60` là cấu hình tối ưu và an toàn nhất cho chatbot hỗ trợ học tập (ưu tiên tính chính xác, không đưa ra thông tin sai lệch hoặc bịa đặt).

---

## 3. Phân Tích Cấu Hình Bộ Nhớ (Memory & Compute Optimization)

- **Cấu hình hiện tại:** RAM **128 MB**, Ephemeral Storage 512 MB.
- **Bộ nhớ sử dụng thực tế (CloudWatch Max Memory Used):** **97 MB** (tương đương 75.8% hạn mức 128 MB).
- **Thảo luận tối ưu hóa lên 256 MB:**
  - *Lợi ích:* AWS phân bổ vCPU cho Lambda tỷ lệ thuận với dung lượng RAM. Khi tăng lên 256 MB, vCPU tăng gấp đôi (~0.16 vCPU thay vì ~0.08 vCPU), giúp giảm Cold Start từ 7.5s xuống dự kiến khoảng 3.8–4.2s.
  - *Cân nhắc thực tế:* Trong ngữ cảnh bài tập lớn và AWS Academy Learner Lab (ngân sách $100 dùng chung cho cả kỳ), mức RAM 128 MB có đơn giá rẻ nhất ($0.0000000021/ms) và hoàn toàn đủ bộ nhớ để chạy thuật toán TF-IDF không bị tràn RAM (OOM). Nhóm quyết định duy trì cấu hình 128 MB để đảm bảo tiêu chí tiết kiệm tài nguyên.

---

## 4. Báo Cáo Chi Phí và Giới Hạn AWS Learner Lab

### 4.1. Giới hạn truy cập quản trị chi phí
- Tài khoản AWS Academy Learner Lab (`550609224402`) áp dụng SCP (Service Control Policy) chặt chẽ. Quyền truy cập vào AWS Billing Console, Cost Explorer và Budgets bị từ chối (`AccessDenied`).
- Theo nguyên tắc học thuật trung thực, nhóm **không tự bịa số liệu hóa đơn USD**.

### 4.2. Định mức chi phí lý thuyết ước tính (Theoretical Cost Estimation)

Dựa trên biểu giá chính thức của AWS khu vực `us-east-1`:

1. **Amazon API Gateway (HTTP API):**
   - Đơn giá: $1.00 / 1,000,000 requests.
   - Ước tính 500 requests phục vụ phát triển và kiểm thử Tuần 4:  
     $$\text{Chi phí} = 500 \times \frac{\$1.00}{1,000,000} = \$0.0005\text{ USD}$$
2. **AWS Lambda:**
   - Free Tier bao gồm 1,000,000 requests/tháng và 3,200,000 giây tính toán cho cấu hình 128 MB.
   - Với khoảng 500 invocations và trung bình 500 ms/invocation:  
     $$\text{Chi phí thực tế} = \$0.00\text{ USD (nằm trọn trong Free Tier)}$$
3. **Amazon S3:**
   - Lưu trữ `faq.json` (26.2 KB) và file web tĩnh frontend (~100 KB):  
     $$\text{Chi phí} < \$0.0001\text{ USD}$$
4. **Amazon DynamoDB:**
   - Lưu trữ vài trăm bản ghi log trong bảng `CourseFAQQueryLogs`:  
     $$\text{Chi phí} = \$0.00\text{ USD (nằm trong mức miễn phí 25 GB)}$$

**Tổng chi phí dự kiến cho toàn bộ hệ thống trong Tuần 4:** Không vượt quá **0.01 USD**.
