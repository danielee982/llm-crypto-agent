# -*- coding: utf-8 -*-
import datetime
import pandas as pd
from pymongo import MongoClient
import random

# --- 1. 기본 설정 및 DB 연결 ---
client = MongoClient('mongodb://localhost:27017/')
db = client['crypto_agent_db']
# 이전 실행 데이터를 초기화하여 항상 새로운 상태에서 시작
for collection_name in db.list_collection_names():
    db[collection_name].drop()
print("Previous database data cleared.")

# --- 파라미터 변수 ---
# 5개 부서
DEPARTMENTS = [
    "Trend_Analyst",
    "Mean-Reversion_Specialist",
    "Volatility_Scout",
    "Fundamental_Reader",
    "News-Sentiment_Reader"
]
TODAY_STR = datetime.date(2025, 6, 30).strftime("%Y-%m-%d")
LOOP = 12
EPISODE = 5

def get_utc_timestamp():
    """현재 UTC 타임스탬프를 ISO 형식으로 반환"""
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

# --- 2. 더미 데이터 생성 함수 (스키마 기반) ---
# 이 함수들은 DB 스키마에 따라 Python 딕셔너리 또는 딕셔너리 리스트를 생성합니다.
# 각 부서의 특성을 반영하기 위해 일부 값을 동적으로 생성합니다.

def create_strategy_cases_checklist(dept):
    """부서(dept) 특성에 맞는 전략 케이스와 체크리스트를 생성합니다."""
    # 부서별로 다른 전략 케이스 예시
    cases = {
        "Trend_Analyst": {
            "id": "ma_cross_long",
            "name": "MA 골든크로스 추세추종",
            "condition": "MA5 > MA20",
            "confidence": 0.75
        },
        "Mean-Reversion_Specialist": {
            "id": "rsi_oversold_long",
            "name": "RSI 과매도 반전 매수",
            "condition": "RSI14 < 30",
            "confidence": 0.80
        },
        "Volatility_Scout": {
            "id": "bb_breakout_long",
            "name": "볼린저밴드 상단 돌파",
            "condition": "Price > BB_Upper",
            "confidence": 0.72
        },
        "Fundamental_Reader": {
            "id": "halving_narrative_long",
            "name": "반감기 내러티브 기반 매수",
            "condition": "days_to_halving < 180",
            "confidence": 0.85
        },
        "News-Sentiment_Reader": {
            "id": "positive_news_spike_long",
            "name": "긍정 뉴스 스파이크 매수",
            "condition": "sentiment_score > 0.8",
            "confidence": 0.68
        },
    }
    base_case = {
        "predicted_scenario": "상승 추세 전환 또는 지속 가능성",
        "recommended_response": "분할 매수 진입 후 2.0 RR 익절",
        "market": "futures",
        "position_side": "long",
        "preferred_action": "long"
    }
    specific_case = {**cases[dept], **base_case} # "**"은 딕셔너리 언패킹

    return {
        "version": f"{TODAY_STR}_1",
        "updated_at": get_utc_timestamp(),
        "cases": [specific_case],
        "checklists": [
            {
                "id": "min_rr",
                "item": "리스크/보상 비율 >= 1.5",
                "metric": "rr",
                "threshold": 1.5,
                "critical": True
            }
        ]
    }

def create_memory_guideline(dept):
    """부서(dept) 특성에 맞는 기억 지침을 생성합니다."""
    # 부서별로 집중하는 메모리 규칙이 다를 수 있습니다.
    style_guide_map = {
        "Trend_Analyst": "추세의 강도와 지속성을 중심으로 기록한다.",
        "Mean-Reversion_Specialist": "과매수/과매도 지표의 반전 성공/실패 사례를 중심으로 기록한다.",
        "Volatility_Scout": "변동성 확대/축소 국면과 주요 이벤트의 상관관계를 중심으로 기록한다.",
        "Fundamental_Reader": "온체인 데이터 및 거시 경제 지표 변화를 중심으로 기록한다.",
        "News-Sentiment_Reader": "주요 뉴스와 커뮤니티 반응이 시장 가격에 미친 영향을 중심으로 기록한다.",
    }
    return {
        "version": f"{TODAY_STR}_1",
        "updated_at": get_utc_timestamp(),
        "short_memory_rule": "최근 5일간의 주요 시장 이벤트와 PnL을 중심으로 요약한다.",
        "mid_memory_rule": "최근 20일간의 주요 전략 성공/실패 사례를 분석한다.",
        "long_memory_rule": "지난 60일 이상의 거시 경제 지표 변화와 장기 추세를 기록한다.",
        "length_limit_tokens": 350,
        "style_guide": style_guide_map[dept]
    }

def create_market_snapshot():
    """시장 스냅샷 데이터를 생성합니다."""
    return {
        "date": TODAY_STR,
        "timestamp_utc": get_utc_timestamp(),
        "symbols": {
            "BTCUSDT": {
                "p": 61234.5 + random.uniform(-100, 100),
                "v": 34750.2,
                "rsi14": 62.1,
                "macd": -45.3
            },
            "ETHUSDT": {
                "p": 3412.7,
                "v": 18210.1,
                "rsi14": 58.8,
                "macd": 3.4
            }
        },
        "research_reports": [
            "Glassnode Report (Summary): BTC futures open interest reaches 6-month high."
        ]
    }

def create_portfolio_snapshot():
    """포트폴리오 스냅샷 데이터를 생성합니다."""
    return {
        "timestamp_utc": get_utc_timestamp(),
        "cash": 20500.0,
        "positions": {
            "BTCUSDT": {
                "side": "long",
                "qty": 0.25,
                "avg_entry": 61120.0,
                "leverage": 3
            }
        },
        "pending_orders": []
    }

def create_decision(dept, strategy_id):
    """의사결정 데이터를 생성합니다."""
    return {
        "ts": get_utc_timestamp(),
        "symbol": "BTCUSDT",
        "market": "futures",
        "position_side": "long",
        "side": "buy",
        "qty": round(random.uniform(0.05, 0.2), 2),
        "price": 60500.0,
        "leverage": 3,
        "order_type": "limit",
        "strategy_case_id": strategy_id,
        "decision_reason": f"Decision by {dept}",
        "comment": "<ASSUMPTION: Market rebound>",
        "risk_reward": 2.4,
        "checklist_pass_rate": 0.83,
        "expected_drawdown_pct": 1.2
    }

def create_executions_data():
    """체결 데이터를 JSON(딕셔너리 리스트) 형식으로 생성합니다."""
    data = [
        {
            'ts': datetime.datetime(2025, 6, 30, 9, 18, 2, 317000),
            'order_id': 'o-abc123',
            'exec_id': 'e-x1',
            'symbol': 'BTCUSDT',
            'position_side': 'long',
            'side': 'buy',
            'price': 60500.0,
            'qty': 0.10,
            'fee': 0.030,
            'realized_pnl': 0.0,
            'status': 'filled'
        }
    ]
    return data

def create_trade_memory(period):
    """거래 기억 데이터를 생성합니다."""
    return {
        "updated_at": get_utc_timestamp(),
        "period": period,
        "lookback_days": {"short": 3, "mid": 20, "long": 90}[period],
        "market_summary": "Market is in a consolidation phase.",
        "strategy_notes": [],
        "risk_events": "None",
        "keywords": []
    }

def create_episode_trades_data():
    """에피소드 거래 데이터를 JSON(딕셔너리 리스트) 형식으로 생성합니다."""
    df = pd.DataFrame(
        {
            'ts': [pd.Timestamp.now()],
            'symbol': ['BTCUSDT'],
            'position_side': ['long'],
            'side': ['buy'],
            'price': [60500.0],
            'qty': [0.10],
            'notional_usd': [6050.0],
            'order_type': ['limit'],
            'fee': [0.03],
            'realized_pnl': [0.0],
            'cum_realized_pnl': [0.0],
            'slippage_pct': [0.0],
            'strategy_case_id': ['test_case'],
            'decision_ts': [pd.Timestamp.now()],
            'loop': LOOP,
            'episode': EPISODE
        }
    )
    return df.to_dict(orient='records')

def create_metrics():
    """성과 지표 데이터를 생성합니다."""
    return {
        "episode_id": f"{LOOP}_{EPISODE}",
        "start_ts": "2025-06-28T23:00:00Z",
        "end_ts": "2025-06-30T23:59:59Z",
        "total_realized_pnl": round(random.uniform(-50, 200), 2),
        "win_rate": round(random.uniform(0.4, 0.7), 2),
        "sharpe_ratio": round(random.uniform(0.5, 2.0), 2)
    }

def create_feedback():
    """피드백 데이터를 생성합니다."""
    return {
        "episode_id": f"{LOOP}_{EPISODE}",
        "generated_at": get_utc_timestamp(),
        "summary": {
            "overall_grade": random.choice(["A", "B+", "B-", "C"]),
            "key_stat": "PnL +102.5, Sharpe 1.43"
        },
        "problem_recognition": [],
        "hypotheses": [],
        "recommendations": {}
    }

def create_strategy_update_agent_config():
    """전략 업데이트 에이전트의 설정 데이터를 생성합니다."""
    return {
        "last_updated": get_utc_timestamp(),
        "update_frequency_days": 7,
        "strategy_model_version": "v1.2.0",
        "parameters": {
            "learning_rate": 0.001,
            "epochs": 100,
            "dataset_size": "latest_30_days"
        },
        "status": "active"
    }

def create_memory_guideline_update_agent_config():
    """기억 지침 업데이트 에이전트의 설정 데이터를 생성합니다."""
    return {
        "last_updated": get_utc_timestamp(),
        "review_interval_days": 30,
        "guideline_version": "v1.0.1",
        "metrics_for_review": ["win_rate", "sharpe_ratio"],
        "status": "active"
    }


# --- 3. 컬렉션별 데이터 삽입 함수 ---
# 각 함수는 특정 컬렉션의 역할과 데이터 구조를 명확히 보여줍니다.

def insert_central_memory(db, dept, strategy_doc, guideline_doc):
    """
    [Collection: central_memory]
    에이전트의 핵심 두뇌 역할을 하는 전략 케이스와 기억 지침을 저장합니다.
    데이터는 부서(dept)별로 격리됩니다.
    """
    collection = db['central_memory']
    collection.update_one(
        {'dept': dept, 'type': 'strategy_cases_checklist'},
        {'$set': {'dept': dept, 'type': 'strategy_cases_checklist', **strategy_doc}},
        upsert=True
    )
    collection.update_one(
        {'dept': dept, 'type': 'memory_guideline'},
        {'$set': {'dept': dept, 'type': 'memory_guideline', **guideline_doc}},
        upsert=True
    )
    # print(f"   - Upserted central_memory for '{dept}'.")

def insert_daily_snapshots(db, dept, snapshot_meta, data_docs):
    """
    [Collection: snapshots]
    매일의 시장 상황, 포트폴리오, 의사결정, 업데이트된 기억의 스냅샷을 저장합니다.
    """
    collection = db['snapshots']
    for doc_type, doc_data in data_docs.items():
        collection.update_one(
            {**snapshot_meta, 'type': doc_type},
            {'$set': {'type': doc_type, **doc_data, **snapshot_meta}},
            upsert=True
        )
    # print(f"   - Upserted daily_snapshots for '{dept}' on {snapshot_meta['date']}.")

def insert_executions_into_snapshots(db, snapshot_meta, executions_list):
    """
    [Collection: snapshots]
    체결 로그 데이터를 기존 'snapshots' 컬렉션 내에 'executions' 타입의 문서로 저장합니다.
    """
    collection = db['snapshots']
    # 'snapshots' 컬렉션에 새로운 타입의 문서로 체결 내역을 추가
    collection.update_one(
        {'dept': snapshot_meta['dept'], 'date': snapshot_meta['date'],
         'loop': snapshot_meta['loop'], 'episode': snapshot_meta['episode'],
         'type': 'executions'}, # 고유한 타입으로 구분
        {'$set': {
            'dept': snapshot_meta['dept'],
            'date': snapshot_meta['date'],
            'loop': snapshot_meta['loop'],
            'episode': snapshot_meta['episode'],
            'type': 'executions', # 문서 타입 지정
            'executions_data': executions_list, # 체결 내역 리스트
            'updated_at': get_utc_timestamp()
        }},
        upsert=True
    )
    # print(f"   - Upserted executions_data into 'snapshots' collection for '{snapshot_meta['dept']}'.")

def insert_episode_summary(db, dept, episode_meta, data_docs):
    """
    [Collection: episodes]
    에피소드 종료 후 집계된 성과 지표(metrics)와 피드백 에이전트의 분석 결과를 저장합니다.
    여기에 전략 및 기억 지침 업데이트 에이전트의 설정도 함께 저장합니다.
    """
    collection = db['episodes']
    for doc_type, doc_data in data_docs.items():
        collection.update_one(
            {**episode_meta, 'type': doc_type},
            {'$set': {'type': doc_type, **doc_data, **episode_meta}},
            upsert=True
        )
    # print(f"   - Upserted episode_summary for '{dept}'.")

def insert_episode_trades_into_episodes(db, episode_meta, episode_trades_list):
    """
    [Collection: episodes]
    에피소드 전체의 거래 데이터를 기존 'episodes' 컬렉션 내에 'trades_data' 타입의 문서로 저장합니다.
    """
    collection = db['episodes']
    # 'episodes' 컬렉션에 새로운 타입의 문서로 거래 내역을 추가
    collection.update_one(
        {'dept': episode_meta['dept'], 'loop': episode_meta['loop'],
         'episode': episode_meta['episode'], 'type': 'trades_data'}, # 고유한 타입으로 구분
        {'$set': {
            'dept': episode_meta['dept'],
            'loop': episode_meta['loop'],
            'episode': episode_meta['episode'],
            'type': 'trades_data', # 문서 타입 지정
            'trades_data': episode_trades_list, # 거래 내역 리스트
            'updated_at': get_utc_timestamp()
        }},
        upsert=True
    )
    # print(f"   - Upserted episode_trades_data into 'episodes' collection for '{episode_meta['dept']}'.")


# --- 4. 메인 실행 함수 ---

def seed_database_for_presentation():
    """
    모든 부서에 대한 더미 데이터를 생성하고, 구조화된 삽입 함수를 호출하여
    데이터베이스의 전체 뼈대를 구축합니다.
    """
    print("="*50)
    print("Starting database seeding for all 5 departments...")
    print("="*50)

    for dept in DEPARTMENTS:
        print(f"\nProcessing Department: [ {dept} ]")

        # 1. 중앙 기억 데이터 생성 및 삽입
        strategy_doc = create_strategy_cases_checklist(dept)
        guideline_doc = create_memory_guideline(dept)
        insert_central_memory(db, dept, strategy_doc, guideline_doc)
        print(f"   - Inserted central_memory (Strategies & Guidelines).")

        # 2. 일일 스냅샷 데이터 생성 및 삽입
        snapshot_meta = {
            'dept': dept,
            'date': TODAY_STR,
            'loop': LOOP,
            'episode': EPISODE
        }
        snapshot_docs = {
            'market': create_market_snapshot(),
            'portfolio': create_portfolio_snapshot(),
            'decision': create_decision(dept, strategy_doc['cases'][0]['id']),
            'trade_memory_short': create_trade_memory('short'),
            'trade_memory_mid': create_trade_memory('mid'),
            'trade_memory_long': create_trade_memory('long'),
        }
        insert_daily_snapshots(db, dept, snapshot_meta, snapshot_docs)
        print(f"   - Inserted daily_snapshots (Market, Portfolio, Decision, Memory).")

        # 3. 체결 데이터 (JSON) 생성 및 스냅샷 컬렉션에 삽입
        executions_list = create_executions_data()
        insert_executions_into_snapshots(db, snapshot_meta, executions_list) # 함수명 변경 및 스냅샷 컬렉션에 삽입
        print(f"   - Inserted executions_data into 'snapshots' collection (type: 'executions').")

        # 4. 에피소드 요약 및 에이전트 설정 데이터 생성 및 삽입
        episode_meta = {
            'dept': dept,
            'loop': LOOP,
            'episode': EPISODE
        }
        episode_docs = {
            'metrics': create_metrics(),
            'feedback': create_feedback(),
            'strategy_update_agent_config': create_strategy_update_agent_config(), # 새로운 에이전트 설정 추가
            'memory_guideline_update_agent_config': create_memory_guideline_update_agent_config(), # 새로운 에이전트 설정 추가
        }
        insert_episode_summary(db, dept, episode_meta, episode_docs)
        print(f"   - Inserted episode_summary (Metrics & Feedback) and Agent configs.")

        # 5. 에피소드 통합 거래 데이터 (JSON) 생성 및 에피소드 컬렉션에 삽입
        episode_trades_list = create_episode_trades_data()
        insert_episode_trades_into_episodes(db, episode_meta, episode_trades_list) # 함수명 변경 및 에피소드 컬렉션에 삽입
        print(f"   - Inserted episode_trades_data into 'episodes' collection (type: 'trades_data').")

    print("\n" + "="*50)
    print("Database seeding completed successfully for all departments.")
    print("="*50)
    client.close()


if __name__ == "__main__":
    seed_database_for_presentation()
