from binance.client import Client
from common import api_key, api_secret, fetch_historical_klines, calculate_all_indicators, upsert_daily_market_document, call_gpt_community_summary, call_gpt_macro_summary, prepare_market_data_documents_for_mongo
from datetime import datetime, timedelta
import time

if __name__ == "__main__":
    SYMBOLS = ['BTCUSDT', 'ETHUSDT'] # 여기에 원하는 심볼을 추가
    INTERVAL = Client.KLINE_INTERVAL_1DAY
    START_DATE_STR = '2023-01-01' # 시작 날짜
    END_DATE_STR = '2023-01-05' # 종료 날짜
    PERPLEXITY_SLEEP_SECONDS = 3 * 60

    start_date = datetime.strptime(START_DATE_STR, '%Y-%m-%d').date()
    end_date = datetime.strptime(END_DATE_STR, '%Y-%m-%d').date()

    # 날짜 범위 내의 모든 날짜에 대해 반복
    for current_date in (start_date + timedelta(days=n) for n in range((end_date - start_date).days + 1)):
        date_str = current_date.strftime('%Y-%m-%d')
        market_data_dict = {}
        for symbol in SYMBOLS:
            lookback_start = (current_date - timedelta(days=250)).strftime('%Y-%m-%d')
            df = fetch_historical_klines(Client(api_key, api_secret), symbol, INTERVAL, lookback_start, date_str) # 가격 데이터 가져오기
            if df.empty:
                continue
            
            df = calculate_all_indicators(df) # 가격 데이터로 기술 지표 계산해 추가

            # open_time의 date만 비교해서 해당 날짜의 모든 캔들 추출
            daily_row = df[df.index.date == current_date]
            if daily_row.empty:
                print(f"{symbol} {date_str}에 해당하는 open_time 데이터 없음")
                continue
            market_data_dict[symbol] = prepare_market_data_documents_for_mongo(daily_row, symbol, INTERVAL) # 시장 데이터 문서 준비
        
        community_summary = call_gpt_community_summary(date_str) # 커뮤니티 요약 생성
        macro_summary = call_gpt_macro_summary(date_str) # 거시경제 요약 생성

        # MongoDB에 문서 삽입 또는 업데이트
        upsert_daily_market_document(
            date_str,
            market_data=market_data_dict,
            community_summary=community_summary,
            macro_summary=macro_summary
        )
        print(f"{current_date} 저장 완료 (market_data count: {len(market_data_dict)})")

        # 3분 간격으로 호출
        if current_date < end_date:
            print(f"--- {PERPLEXITY_SLEEP_SECONDS // 60}분 휴식 ---\n")
            time.sleep(PERPLEXITY_SLEEP_SECONDS)

    print("통합 파이프라인 실행 완료.") 