# RSI & MFI Telegram Alert Bot

Bot Python cảnh báo tín hiệu giao dịch dựa trên chỉ báo RSI và MFI cho các cặp coin trên Binance, gửi thông báo qua Telegram.

## Tính năng
- Lấy dữ liệu giá các coin (ETHUSDT, BTCUSDT, SOLUSDT, SUIUSDT) từ Binance ở nhiều khung thời gian (15m, 1h, 4h, 1d)
- Tính toán chỉ số RSI và MFI
- Đưa ra tín hiệu giao dịch (LONG/SHORT/quá mua/quá bán)
- Gửi cảnh báo tổng hợp về Telegram nếu có tín hiệu rõ ràng
- Có thể tự động chạy định kỳ bằng GitHub Actions

## Cài đặt
1. Clone repo về máy:
   ```bash
   git clone <repo-url>
   cd rsi_mfi_bot_with_token
   ```
2. Cài đặt Python 3.10+ và các thư viện:
   ```bash
   pip install -r requirements.txt
   ```

## Thiết lập biến môi trường
Tạo file `.env` hoặc export biến môi trường trước khi chạy:
- `TELEGRAM_TOKEN`: Token của bot Telegram
- `TELEGRAM_CHAT_ID`: Chat ID để gửi cảnh báo

Ví dụ (Linux/macOS):
```bash
export TELEGRAM_TOKEN=your_bot_token
export TELEGRAM_CHAT_ID=your_chat_id
python alert.py
```

## Chạy bằng GitHub Actions
Repo đã có sẵn workflow mẫu tại `.github/workflows/alert.yml` để tự động chạy bot định kỳ.

### Thiết lập secrets:
1. Vào repo trên GitHub > Settings > Secrets and variables > Actions
2. Thêm hai secrets:
   - `TELEGRAM_TOKEN`: Token của bot Telegram
   - `TELEGRAM_CHAT_ID`: Chat ID Telegram

### Tùy chỉnh lịch chạy
Sửa trường `cron` trong file workflow để thay đổi lịch chạy (mặc định mỗi 30 phút).

## Đóng góp
Pull request và issue luôn được hoan nghênh! 