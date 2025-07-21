
import os
import requests
import pandas as pd
import telegram


BOT_TOKEN = os.environ.get('TELEGRAM_TOKEN')
CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')

if not BOT_TOKEN or not CHAT_ID:
    raise ValueError('Missing TELEGRAM_TOKEN or TELEGRAM_CHAT_ID environment variable')

INTERVALS = ['15m', '1h', '4h', '1d']
SYMBOLS = ['ETHUSDT', 'BTCUSDT', 'SOLUSDT', 'SUIUSDT']

bot = telegram.Bot(token=BOT_TOKEN)


def fetch_klines(symbol, interval):
    url = f'https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}&limit=100'
    res = requests.get(url)
    data = res.json()
    df = pd.DataFrame(data, columns=[
        'time', 'open', 'high', 'low', 'close', 'volume',
        'close_time', 'quote_asset_volume', 'num_trades',
        'taker_buy_base', 'taker_buy_quote', 'ignore'
    ])
    df[['close', 'high', 'low', 'volume']] = df[['close', 'high', 'low', 'volume']].astype(float)
    return df


def calculate_rsi(closes, period=14):
    delta = closes.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi.iloc[-1]


def calculate_mfi(highs, lows, closes, volumes, period=14):
    tp = (highs + lows + closes) / 3
    raw_mf = tp * volumes
    pos_flow = (tp > tp.shift(1)) * raw_mf
    neg_flow = (tp < tp.shift(1)) * raw_mf
    pos_sum = pos_flow.rolling(window=period).sum()
    neg_sum = neg_flow.rolling(window=period).sum()
    mfr = pos_sum / neg_sum.replace(0, 1)
    mfi = 100 - (100 / (1 + mfr))
    return mfi.iloc[-1]


def get_trade_signal(rsi, mfi):
    if rsi <= 30 and mfi <= 20:
        return "🟢 LONG (quá bán)"
    if rsi >= 70 and mfi >= 80:
        return "🔴 SHORT (quá mua)"
    if rsi <= 30:
        return "🟢 RSI quá bán"
    if rsi >= 70:
        return "🔴 RSI quá mua"
    if mfi <= 20:
        return "🟢 MFI quá bán"
    if mfi >= 80:
        return "🔴 MFI quá mua"
    return "ℹ️ Không rõ ràng"


def run():
    results = {}
    for symbol in SYMBOLS:
        results[symbol] = []
        for interval in INTERVALS:
            try:
                df = fetch_klines(symbol, interval)
                rsi = calculate_rsi(df['close'])
                mfi = calculate_mfi(df['high'], df['low'], df['close'], df['volume'])
                price = df['close'].iloc[-1]
                signal = get_trade_signal(rsi, mfi)
                msg = (
                    f"⏱️ [{interval}]\n"
                    f"RSI: {rsi:.2f} | MFI: {mfi:.2f}\n{signal}"
                )
                results[symbol].append({
                    'msg': msg,
                    'price': price,
                    'interval': interval,
                    'signal': signal
                })
            except Exception as e:
                print(f"Lỗi {symbol} {interval}: {e}")

    any_signal = False
    special_alert = ''
    symbol_msgs = []

    for symbol, signals in results.items():
        meaningful = [s for s in signals if s['signal'] != "ℹ️ Không rõ ràng"]
        if len(meaningful) >= 2:
            special_alert += (
                f"⚡ {symbol}: NHIỀU KHUNG GIỜ CÙNG QUÁ MUA/QUÁ BÁN! "
                f"({', '.join([s['interval'] for s in meaningful])})\n"
            )
        if meaningful:
            any_signal = True
            price = signals[0]['price']
            combined_msg = (
                f"💱 {symbol} - Giá: ${price:.2f}\n\n"
                + "\n\n".join([s['msg'] for s in signals])
            )
            symbol_msgs.append(combined_msg)

    if any_signal:
        full_msg = (
            f"📊 RSI & MFI đa khung:\n\n{special_alert}"
            f"{'\n\n-------------------------------------\n\n'.join(symbol_msgs)}"
        )
        bot.send_message(chat_id=CHAT_ID, text=full_msg)


if __name__ == "__main__":
    run()
