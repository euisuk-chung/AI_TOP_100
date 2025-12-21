"""
Q3 VLM 분석 - Q3-4 (Bobo 역 배우 직업), Q3-6 (얼굴 마커 개수)
qwen3-vl:8b 모델 사용
"""
import os
import sys
from pathlib import Path
import ollama

FRAMES_DIR = Path("/home/euisuk.chung/repo/AI_TOP_100/source/q3/frames/사랑_예술_그리고_이야기")

# Q3-6: 얼굴 마커 카운트 프롬프트
MARKER_PROMPT = """이 이미지에서 얼굴에 부착된 마커(marker)를 찾아 개수를 세어주세요.

마커란:
- 얼굴에 부착된 작은 점이나 센서
- 모션캡처용 트래킹 포인트
- 보통 녹색, 흰색, 또는 반사성 점으로 표시됨

특히 다음 위치의 마커를 세어주세요:
- 콧등 (nose bridge)
- 양쪽 눈 주변 (around both eyes)
- 눈썹 (eyebrows)

정확한 개수와 위치를 한국어로 답변해주세요.
마커가 보이지 않으면 "마커 없음"이라고 답해주세요."""

# Q3-4: Bobo 역 배우 직업 프롬프트
ACTOR_PROMPT = """이 이미지에서 배우나 인물을 찾아주세요.
특히 "Bobo" 역할을 맡은 배우(John Hennigan)의 과거 직업에 대한 단서를 찾아주세요.

John Hennigan은 WWE 프로레슬러 출신입니다. 다음 단서를 찾아주세요:
1. 프로레슬러 관련 (WWE 로고, 레슬링 동작, 근육질 체형)
2. 이름이나 텍스트 (John Hennigan, WWE, Johnny)
3. 레슬링 경기장면이나 관련 이미지

한국어로 간결하게 답변해주세요."""


def analyze_frame(image_path: Path, prompt: str) -> str:
    """qwen3-vl:8b를 사용하여 이미지 분석"""
    try:
        response = ollama.chat(
            model='qwen3-vl:8b',
            messages=[{
                'role': 'user',
                'content': prompt,
                'images': [str(image_path)]
            }],
            options={'temperature': 0}
        )
        return response['message']['content']
    except Exception as e:
        return f"분석 오류: {e}"


def analyze_for_markers():
    """Q3-6: 얼굴 마커 분석"""
    print("=" * 60)
    print("Q3-6: 얼굴 마커 분석")
    print("=" * 60)

    frames = sorted(FRAMES_DIR.glob("frame_*.jpg"))
    print(f"총 {len(frames)}개 프레임")

    # 샘플링 (50개 프레임만)
    sample_size = 50
    step = len(frames) // sample_size if len(frames) > sample_size else 1
    sampled = frames[::step][:sample_size]

    results = []
    for i, frame in enumerate(sampled):
        print(f"[{i+1}/{len(sampled)}] {frame.name}", end=" ", flush=True)
        response = analyze_frame(frame, MARKER_PROMPT)

        # 마커 발견시 출력
        if "마커" in response and "없음" not in response:
            print(f"-> 마커 발견!")
            print(f"   {response[:200]}")
            results.append((frame.name, response))
        else:
            print("-> 마커 없음")

    print("\n" + "=" * 60)
    print("마커 발견 프레임:")
    for name, resp in results:
        print(f"\n[{name}]")
        print(resp)

    return results


def analyze_for_actor():
    """Q3-4: Bobo 역 배우 분석"""
    print("=" * 60)
    print("Q3-4: Bobo 역 배우 (John Hennigan) 분석")
    print("=" * 60)

    frames = sorted(FRAMES_DIR.glob("frame_*.jpg"))
    print(f"총 {len(frames)}개 프레임")

    # 샘플링 (30개 프레임만)
    sample_size = 30
    step = len(frames) // sample_size if len(frames) > sample_size else 1
    sampled = frames[::step][:sample_size]

    results = []
    for i, frame in enumerate(sampled):
        print(f"[{i+1}/{len(sampled)}] {frame.name}", end=" ", flush=True)
        response = analyze_frame(frame, ACTOR_PROMPT)

        # 관련 정보 발견시 출력
        if any(kw in response.lower() for kw in ["레슬", "wwe", "johnn", "hennig", "근육", "wrestler"]):
            print(f"-> 관련 정보 발견!")
            print(f"   {response[:200]}")
            results.append((frame.name, response))
        else:
            print("-> 정보 없음")

    print("\n" + "=" * 60)
    print("관련 프레임:")
    for name, resp in results:
        print(f"\n[{name}]")
        print(resp)

    return results


if __name__ == "__main__":
    task = sys.argv[1] if len(sys.argv) > 1 else "markers"

    if task == "markers":
        analyze_for_markers()
    elif task == "actor":
        analyze_for_actor()
    else:
        print(f"Unknown task: {task}")
        print("Usage: python q3_vlm_analyze.py [markers|actor]")
