# llm-crypto-agent

## 🗂️ .env 파일 작성법

아래와 같이 프로젝트 루트 디렉터리에 `.env` 파일을 생성합니다.

```env
# Binance API
BINANCE_API_KEY=your_binance_api_key
BINANCE_SECRET_KEY=your_binance_secret_key

# OpenAI API (또는 기타 LLM API)
OPENAI_API_KEY=your_openai_api_key

# MongoDB
MONGO_URI=mongodb://localhost:27017/
```

## 🕒 시작 날짜 / 끝 날짜
- 날짜 조정은 daily_market_pipeline.py 내부에서 바로 변경할 수 있습니다.
- 지표 계산을 위해, 코드에서 START_DATE 기준 250일 전부터 데이터를 불러와 모든 기술 지표를 START_DATE 시점부터 정확히 계산할 수 있도록 구현되었습니다.

## 📄 Example Document Structure

```json
{
  "_id": { "$oid": "68551f6f9490240c8cae626e" },
  "date": "YYYY-MM-DD",
  "community_summary": "...",
  "macro_summary": "...",
  "market_data": {
    "BTCUSDT": {
      "chart_data": {
        "open": 16541.77,
        "high": 16628.00,
        "low": 16499.01,
        "close": 16616.75,
        "volume": 96925.41374
      },
      "technical_indicators": {
        "MA": {
          "MA-5": 16589.482,
          "MA-10": 16701.989
        },
        "EMA": {
          "EMA-5": 16620.6906,
          "EMA-10": 16682.5802
        }
      }
    }
  }
}

```
