"""
Q4 전투 게임 시뮬레이션 - ML 예측 모델
RandomForest 기반 전투 결과 예측
"""
import json
import numpy as np
from collections import Counter
from pathlib import Path


def extract_features(battle):
    """전투 데이터에서 특성 추출"""
    features = {}

    for team in ['red', 'blue']:
        team_data = battle[team]
        units = [u['type'] for u in team_data]
        unit_counts = Counter(units)

        # 유닛별 개수
        for unit in ['aleo', 'bras', 'cbene', 'dgreg', 'eyanoo']:
            features[f'{team}_{unit}'] = unit_counts.get(unit, 0)

        features[f'{team}_size'] = len(team_data)
        features[f'{team}_dup'] = 1 if len(unit_counts) > 0 and max(unit_counts.values()) > 1 else 0

        # 위치 파싱 (at: "x,y")
        positions = [tuple(map(int, u['at'].split(','))) for u in team_data]
        xs, ys = [p[0] for p in positions], [p[1] for p in positions]

        features[f'{team}_avg_x'] = np.mean(xs)
        features[f'{team}_avg_y'] = np.mean(ys)
        features[f'{team}_spread_x'] = max(xs) - min(xs) if len(xs) > 1 else 0
        features[f'{team}_spread_y'] = max(ys) - min(ys) if len(ys) > 1 else 0
        features[f'{team}_x_form'] = 1 if features[f'{team}_spread_x'] > features[f'{team}_spread_y'] else 0
        features[f'{team}_front'] = sum(1 for p in positions if p[1] >= 10) / len(team_data)
        features[f'{team}_strong'] = unit_counts.get('dgreg', 0) + unit_counts.get('cbene', 0)

    # 비교 특성
    features['size_diff'] = features['red_size'] - features['blue_size']
    features['strong_diff'] = features['red_strong'] - features['blue_strong']
    features['dgreg_diff'] = features['red_dgreg'] - features['blue_dgreg']

    return features


def train_and_predict(train_path, test_path, output_path=None):
    """모델 학습 및 예측"""
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.model_selection import cross_val_score

    # 데이터 로드
    with open(train_path, 'r') as f:
        train_battles = json.load(f)

    with open(test_path, 'r') as f:
        test_battles = json.load(f)

    print(f"Train: {len(train_battles)} battles, Test: {len(test_battles)} battles")

    # 학습 데이터 준비
    X_train = np.array([list(extract_features(b).values()) for b in train_battles])
    y_train = np.array([1 if b['winner'] == 'red' else 0 for b in train_battles])

    # 모델 학습
    model = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42)
    scores = cross_val_score(model, X_train, y_train, cv=5)
    print(f"Cross-validation accuracy: {scores.mean():.4f} (+/- {scores.std():.4f})")

    model.fit(X_train, y_train)

    # 예측
    X_test = np.array([list(extract_features(b).values()) for b in test_battles])
    predictions = model.predict(X_test)

    results = [
        {"id": test_battles[i]['id'], "winner": "red" if p == 1 else "blue"}
        for i, p in enumerate(predictions)
    ]

    print(f"Predictions: Red {sum(p==1 for p in predictions)}, Blue {sum(p==0 for p in predictions)}")

    # 저장
    if output_path:
        with open(output_path, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"Saved to: {output_path}")

    return results


def analyze_1v1(train_path):
    """1v1 전투 분석"""
    with open(train_path, 'r') as f:
        train_battles = json.load(f)

    # 1v1 필터링
    battles_1v1 = [b for b in train_battles if len(b['red']) == 1 and len(b['blue']) == 1]
    print(f"1v1 battles: {len(battles_1v1)}")

    # 유닛별 승률
    unit_stats = {}
    for battle in battles_1v1:
        for team in ['red', 'blue']:
            unit = battle[team][0]['type']
            is_win = (battle['winner'] == team)

            if unit not in unit_stats:
                unit_stats[unit] = {'wins': 0, 'total': 0}
            unit_stats[unit]['total'] += 1
            if is_win:
                unit_stats[unit]['wins'] += 1

    print("\n=== 1v1 Unit Win Rates ===")
    for unit, stats in sorted(unit_stats.items(), key=lambda x: -x[1]['wins']/x[1]['total']):
        rate = stats['wins'] / stats['total'] * 100
        print(f"{unit}: {rate:.2f}% ({stats['wins']}/{stats['total']})")


if __name__ == "__main__":
    base_path = Path(__file__).parent.parent / "source" / "q4"
    train_path = base_path / "train_battles.json"
    test_path = base_path / "test_battles.json"
    output_path = base_path / "predictions.json"

    analyze_1v1(train_path)
    train_and_predict(train_path, test_path, output_path)
