from binance.client import Client
from common import api_key, api_secret, fetch_historical_klines, calculate_all_indicators, upsert_daily_market_document, call_gpt_community_summary, call_gpt_macro_summary, prepare_market_data_documents_for_mongo
from datetime import datetime, timedelta
import time

if __name__ == "__main__":
    SYMBOLS = ['BTCUSDT', 'ETHUSDT']
    INTERVAL = Client.KLINE_INTERVAL_1DAY
    START_DATE_STR = '2023-01-01'
    END_DATE_STR = '2023-01-05'
    PERPLEXITY_SLEEP_SECONDS = 3 * 60

    start_date = datetime.strptime(START_DATE_STR, '%Y-%m-%d').date()
    end_date = datetime.strptime(END_DATE_STR, '%Y-%m-%d').date()

    for current_date in (start_date + timedelta(days=n) for n in range((end_date - start_date).days + 1)):
        date_str = current_date.strftime('%Y-%m-%d')
        market_data_dict = {}
        for symbol in SYMBOLS:
            lookback_start = (current_date - timedelta(days=250)).strftime('%Y-%m-%d')
            df = fetch_historical_klines(Client(api_key, api_secret), symbol, INTERVAL, lookback_start, date_str)
            if df.empty:
                continue
            
            df = calculate_all_indicators(df)
            # open_time의 date만 비교해서 해당 날짜의 모든 캔들 추출
            # print(f"[{symbol}][{date_str}] open_time 인덱스 샘플: {[t.strftime('%Y-%m-%d') for t in df.index[-5:]]}")
            daily_row = df[df.index.date == current_date]
            if daily_row.empty:
                print(f"{symbol} {date_str}에 해당하는 open_time 데이터 없음")
                continue
            market_data_dict[symbol] = prepare_market_data_documents_for_mongo(daily_row, symbol, INTERVAL)
        # GPT-4o API로 요약 생성
        community_summary = call_gpt_community_summary(date_str)
        macro_summary = call_gpt_macro_summary(date_str)
        upsert_daily_market_document(
            date_str,
            market_data=market_data_dict,
            community_summary=community_summary,
            macro_summary=macro_summary
        )
        print(f"{current_date} 저장 완료 (market_data count: {len(market_data_dict)})")
        if current_date < end_date:
            print(f"--- {PERPLEXITY_SLEEP_SECONDS // 60}분 휴식 ---\n")
            time.sleep(PERPLEXITY_SLEEP_SECONDS)
    print("통합 파이프라인 실행 완료.") 