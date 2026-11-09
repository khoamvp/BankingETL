# Banking ETL

Pipeline Python trích xuất dữ liệu nghiệp vụ ngân hàng từ PostgreSQL và nạp vào BigQuery. Phiên bản hiện tại tập trung vào tầng **raw**, theo cơ chế full load.

## Kiến trúc

```text
                         ┌────────────────────────┐
                         │ .env + Google ADC      │
                         │ cấu hình và xác thực   │
                         └───────────┬────────────┘
                                     │
                                     ▼
┌───────────────┐   SELECT toàn bộ   ┌────────────────────┐
│ PostgreSQL    │ ─────────────────▶ │ main.py            │
│ nguồn banking │                    │ điều phối pipeline │
└───────────────┘                    └─────────┬──────────┘
                                               │
                                  khởi tạo      │      full load
                                               ▼
                                     ┌────────────────────┐
                                     │ BigQuery           │
                                     │ dataset raw        │
                                     │ 11 bảng nguồn      │
                                     └────────────────────┘
```

### Luồng chạy

1. `main.py` gọi `etl.load.run()` để tạo dataset raw và các bảng BigQuery nếu chưa tồn tại.
2. `etl.extract.run()` kết nối PostgreSQL và BigQuery.
3. Với từng bảng khai báo, pipeline tạo câu `SELECT` lấy tất cả cột, đọc toàn bộ dữ liệu vào bộ nhớ, chuyển thành DataFrame rồi tải lên bảng raw.
4. Bảng có dữ liệu được ghi bằng `WRITE_TRUNCATE`, tức thay thế dữ liệu cũ. Nếu nguồn trả về rỗng, bước tải bỏ qua bảng đó.

Các bảng nguồn: `branches`, `customers`, `products`, `accounts`, `channels`, `transaction_types`, `currencies`, `merchants`, `cards`, `transactions` và `transaction_status_history`.

## Cấu trúc mã nguồn

| Tệp | Trách nhiệm |
|---|---|
| `main.py` | Điểm vào và thứ tự chạy các bước pipeline. |
| `etl/settings.py` | Đọc `.env`, kiểm tra biến bắt buộc và tạo cấu hình kết nối. |
| `etl/clients.py` | Tạo client PostgreSQL/BigQuery, tên bảng và dataset BigQuery. |
| `etl/tables.py` | Khai báo tên bảng, cột, kiểu dữ liệu, khóa chính và watermark. |
| `etl/schema.py` | Tạo schema nullable và khởi tạo bảng raw BigQuery. |
| `etl/load.py` | Khởi tạo dataset raw và bảng raw. |
| `etl/extract.py` | Trích xuất từ PostgreSQL, tạo DataFrame và nạp dữ liệu vào BigQuery. |
| `requirements.txt` | Các thư viện Python cần thiết. |

## Phạm vi hiện tại

- Chỉ triển khai luồng PostgreSQL → BigQuery raw; chưa có bước làm sạch/biến đổi hay nạp vào tầng clean.
- `BQ_CLEAN_DATASET`, `BQ_OPS_DATASET`, khóa chính, watermark, `METADATA_COLUMNS`, `HASH_SALT` và `SOURCE_SYSTEM` đã có khai báo cấu hình/mô hình nhưng chưa được dùng trong luồng hiện tại.
- Đây là full load và đọc toàn bộ kết quả vào bộ nhớ; chưa có incremental load, chia lô, lịch chạy hoặc cơ chế retry riêng.
- Không có test hay cấu hình triển khai tự động được cung cấp trong project hiện tại.

## Cài đặt và chạy

Yêu cầu Python, quyền truy cập cơ sở dữ liệu nguồn và Google Cloud BigQuery.

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Tạo `.env` tại thư mục gốc. Các biến bắt buộc:

```dotenv
SOURCE_DB_HOST=
SOURCE_DB_PASSWORD=
BQ_PROJECT_ID=
HASH_SALT=
```

Các biến tùy chọn (giá trị mặc định trong ngoặc):

| Biến | Mặc định |
|---|---|
| `PIPELINE_NAME` | `banking_bigquery_elt` |
| `SOURCE_DB_PORT` | `15432` |
| `SOURCE_DB_NAME` | `core_banking` |
| `SOURCE_DB_USER` | `de_source_exporter` |
| `BQ_LOCATION` | `asia-southeast1` |
| `BQ_RAW_DATASET` | `banking_raw` |
| `BQ_CLEAN_DATASET` | `banking_clean` |
| `BQ_OPS_DATASET` | `banking_ops` |
| `SOURCE_SYSTEM` | `CORE_BANKING` |

Thiết lập Google Application Default Credentials cho tài khoản có quyền truy cập BigQuery, sau đó chạy:

```bash
python main.py
```

Không commit `.env` hoặc thông tin xác thực vào repository.
