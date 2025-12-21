"""
Q3 영상 팩트 체크 - YouTube 영상 다운로드, 프레임 추출, VLM 분석 파이프라인
qwen3-vl:8b 모델을 사용하여 영상에서 시각적 정보 추출
"""
import os
import subprocess
import json
import time
from pathlib import Path
from typing import List, Dict, Optional
import cv2
import ollama

# 기본 경로 설정
BASE_DIR = Path(__file__).parent
VIDEOS_DIR = BASE_DIR / "videos"
FRAMES_DIR = BASE_DIR / "frames"
RESULTS_DIR = BASE_DIR / "results"

# 분석할 YouTube 영상들
VIDEOS = {
    "적정선은_어디인가": {
        "url": "https://www.youtube.com/watch?v=UwsrzCVZAb8",
        "questions": ["Q3-1"]  # Mark Sagar 음료
    },
    "사랑_예술_그리고_이야기": {
        "url": "https://www.youtube.com/watch?v=Kr1fmKVY3cA",
        "questions": ["Q3-4", "Q3-6"]  # Bobo 배우 직업, 얼굴 마커
    },
    "AI를_통한_치유": {
        "url": "https://www.youtube.com/watch?v=V5aZjsWM2wo",
        "questions": ["Q3-7"]  # 사실 확인
    }
}

# 문항별 VLM 프롬프트
VLM_PROMPTS = {
    "Q3-1": """이 영상 프레임에서 음료를 찾아주세요.
특히 Mark Sagar(킹콩, 아바타 안면 시뮬레이션 작업자)가 마시는 음료에 주목해주세요.

다음 중 어떤 음료인지 확인해주세요:
1. 콜라
2. 아이스 아메리카노
3. 카푸치노
4. 따뜻한 허브티
5. 오렌지 주스

한국어로 간결하게 답변해주세요. 음료가 보이지 않으면 "음료 없음"이라고 답해주세요.""",

    "Q3-4": """이 영상 프레임에서 배우나 인물을 찾아주세요.
특히 "Bobo" 역할을 맡은 배우(John Hennigan)의 과거 직업에 대한 단서를 찾아주세요.

다음 중 어떤 직업의 흔적이 보이는지 확인해주세요:
1. 프로레슬러 (WWE 관련 로고, 레슬링 동작, 근육질 체형)
2. 뮤지션 (악기, 마이크)
3. 레이서 (자동차, 헬멧)
4. AI 전문가 (컴퓨터, 연구실)
5. 댄서 (무대, 의상)

한국어로 간결하게 답변해주세요.""",

    "Q3-6": """이 영상 프레임에서 얼굴에 부착된 마커(marker)를 찾아 개수를 세어주세요.

마커란:
- 얼굴에 부착된 작은 점이나 센서
- 모션캡처용 트래킹 포인트
- 보통 녹색, 흰색, 또는 반사성 점으로 표시됨

특히 다음 위치의 마커를 세어주세요:
- 콧등 (nose bridge)
- 양쪽 눈 주변 (around both eyes)
- 눈썹 (eyebrows)

정확한 개수와 위치를 한국어로 답변해주세요.
마커가 보이지 않으면 "마커 없음"이라고 답해주세요.""",

    "Q3-7": """이 영상 프레임의 내용을 분석해주세요.

다음 사항들을 확인해주세요:
1. 화면에 보이는 텍스트나 숫자
2. 등장인물의 이름이나 정보
3. 특정 장소나 기관명
4. 기술적/과학적 정보

한국어로 상세히 답변해주세요."""
}


def create_directories():
    """필요한 디렉토리 생성"""
    for dir_path in [VIDEOS_DIR, FRAMES_DIR, RESULTS_DIR]:
        dir_path.mkdir(parents=True, exist_ok=True)


def download_video(video_name: str, url: str) -> Optional[Path]:
    """yt-dlp를 사용하여 YouTube 영상 다운로드"""
    output_path = VIDEOS_DIR / f"{video_name}.mp4"

    if output_path.exists():
        print(f"  이미 다운로드됨: {output_path}")
        return output_path

    print(f"  다운로드 중: {url}")
    cmd = [
        "yt-dlp",
        "-f", "bestvideo[height<=720][ext=mp4]+bestaudio[ext=m4a]/best[height<=720]",
        "-o", str(output_path),
        "--merge-output-format", "mp4",
        url
    ]

    try:
        subprocess.run(cmd, check=True, capture_output=True)
        print(f"  다운로드 완료: {output_path}")
        return output_path
    except subprocess.CalledProcessError as e:
        print(f"  다운로드 실패: {e}")
        return None


def extract_frames(video_path: Path, output_dir: Path,
                   interval_sec: float = 5.0,
                   scene_threshold: float = 30.0) -> List[Path]:
    """OpenCV를 사용하여 프레임 추출"""
    output_dir.mkdir(parents=True, exist_ok=True)

    # 이미 추출된 프레임이 있으면 재사용
    existing_frames = list(output_dir.glob("frame_*.jpg"))
    if existing_frames:
        print(f"  이미 추출된 프레임: {len(existing_frames)}개")
        return sorted(existing_frames)

    cap = cv2.VideoCapture(str(video_path))
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_interval = int(fps * interval_sec)

    print(f"  FPS: {fps:.2f}, 총 프레임: {total_frames}, 추출 간격: {frame_interval}")

    frame_paths = []
    prev_frame = None
    frame_idx = 0
    saved_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        should_save = False

        # 간격 기반 추출
        if frame_idx % frame_interval == 0:
            should_save = True
        # 장면 변화 감지
        elif prev_frame is not None:
            diff = calculate_frame_difference(prev_frame, frame)
            if diff > scene_threshold:
                should_save = True

        if should_save:
            timestamp = frame_idx / fps
            filename = f"frame_{saved_count:04d}_{timestamp:.2f}s.jpg"
            frame_path = output_dir / filename
            cv2.imwrite(str(frame_path), frame)
            frame_paths.append(frame_path)
            saved_count += 1

        prev_frame = frame.copy()
        frame_idx += 1

    cap.release()
    print(f"  프레임 추출 완료: {saved_count}개")
    return frame_paths


def calculate_frame_difference(frame1, frame2) -> float:
    """히스토그램 비교를 통한 프레임 차이 계산"""
    gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
    hist1 = cv2.calcHist([gray1], [0], None, [256], [0, 256])
    hist2 = cv2.calcHist([gray2], [0], None, [256], [0, 256])
    return cv2.compareHist(hist1, hist2, cv2.HISTCMP_BHATTACHARYYA) * 100


def analyze_frame_with_vlm(image_path: Path, prompt: str) -> str:
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


def analyze_frames_for_question(frame_paths: List[Path],
                                 question_id: str,
                                 sample_size: int = 20) -> List[Dict]:
    """특정 문항에 대해 프레임들 분석"""
    prompt = VLM_PROMPTS.get(question_id, "이 이미지를 분석해주세요.")

    # 샘플링 (너무 많은 프레임 분석 방지)
    if len(frame_paths) > sample_size:
        step = len(frame_paths) // sample_size
        sampled_frames = frame_paths[::step][:sample_size]
    else:
        sampled_frames = frame_paths

    print(f"  {question_id} 분석 중 ({len(sampled_frames)}개 프레임)...")

    results = []
    for i, frame_path in enumerate(sampled_frames):
        print(f"    [{i+1}/{len(sampled_frames)}] {frame_path.name}", end=" ", flush=True)

        response = analyze_frame_with_vlm(frame_path, prompt)
        results.append({
            "frame": str(frame_path),
            "timestamp": frame_path.stem.split("_")[-1],
            "response": response
        })

        # 관련 정보 발견시 표시
        if "음료" in response or "마커" in response or "레슬" in response:
            print(f"-> 관련 정보 발견!")
        else:
            print("-> 분석 완료")

        # API 호출 간 딜레이
        time.sleep(0.5)

    return results


def summarize_results(results: List[Dict], question_id: str) -> str:
    """분석 결과 요약"""
    prompt_summary = f"""다음은 영상 프레임들을 분석한 결과입니다.

문항: {question_id}
{VLM_PROMPTS.get(question_id, '')}

분석 결과들:
"""
    for r in results:
        prompt_summary += f"\n[{r['timestamp']}] {r['response'][:200]}"

    prompt_summary += "\n\n위 분석 결과들을 종합하여 최종 답변을 한국어로 작성해주세요."

    try:
        response = ollama.chat(
            model='qwen3-vl:8b',
            messages=[{'role': 'user', 'content': prompt_summary}]
        )
        return response['message']['content']
    except Exception as e:
        return f"요약 오류: {e}"


def process_video(video_name: str, video_info: Dict) -> Dict:
    """단일 영상 처리 파이프라인"""
    print(f"\n{'='*60}")
    print(f"처리 중: {video_name}")
    print(f"{'='*60}")

    # 1. 영상 다운로드
    print("\n[1] YouTube 영상 다운로드")
    video_path = download_video(video_name, video_info["url"])
    if not video_path:
        return {"error": "다운로드 실패"}

    # 2. 프레임 추출
    print("\n[2] 프레임 추출")
    frames_output = FRAMES_DIR / video_name
    frame_paths = extract_frames(video_path, frames_output)

    # 3. VLM 분석
    print("\n[3] VLM 분석")
    all_results = {}
    for question_id in video_info["questions"]:
        results = analyze_frames_for_question(frame_paths, question_id)
        summary = summarize_results(results, question_id)
        all_results[question_id] = {
            "frame_analyses": results,
            "summary": summary
        }
        print(f"\n  {question_id} 요약: {summary[:200]}...")

    return all_results


def main():
    """메인 실행 함수"""
    print("=" * 60)
    print("Q3 영상 팩트 체크 - VLM 분석 파이프라인")
    print("=" * 60)

    # 디렉토리 생성
    create_directories()

    # 전체 결과
    all_video_results = {}

    # 각 영상 처리
    for video_name, video_info in VIDEOS.items():
        results = process_video(video_name, video_info)
        all_video_results[video_name] = results

    # 결과 저장
    output_file = RESULTS_DIR / "q3_vlm_analysis.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_video_results, f, ensure_ascii=False, indent=2)

    print(f"\n\n{'='*60}")
    print(f"분석 완료! 결과 저장: {output_file}")
    print(f"{'='*60}")

    # 최종 요약 출력
    print("\n최종 분석 결과:")
    for video_name, results in all_video_results.items():
        print(f"\n[{video_name}]")
        if isinstance(results, dict) and "error" not in results:
            for q_id, q_result in results.items():
                print(f"  {q_id}: {q_result.get('summary', 'N/A')[:100]}...")


if __name__ == "__main__":
    main()
