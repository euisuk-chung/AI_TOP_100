#!/usr/bin/env python3
"""
Q3-6: 얼굴 마커 갯수 분석
VLM (qwen3-vl:32b)을 사용하여 얼굴 마커 장면 분석
"""

import subprocess
import json
import base64
import os
from pathlib import Path

def encode_image(image_path):
    """이미지를 base64로 인코딩"""
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

def analyze_with_vlm(image_path, prompt):
    """Ollama VLM으로 이미지 분석"""
    image_base64 = encode_image(image_path)

    payload = {
        "model": "qwen3-vl:32b",
        "prompt": prompt,
        "images": [image_base64],
        "stream": False,
        "options": {
            "temperature": 0.1
        }
    }

    result = subprocess.run(
        ["curl", "-s", "http://localhost:11434/api/generate",
         "-d", json.dumps(payload)],
        capture_output=True, text=True
    )

    try:
        response = json.loads(result.stdout)
        return response.get("response", "")
    except:
        return result.stdout

def main():
    # 프레임 디렉토리
    frames_dir = Path("/home/euisuk.chung/repo/AI_TOP_100/source/q3/frames")

    # 두 영상 모두 확인
    videos = ["적정선은_어디인가", "사랑_예술_그리고_이야기"]

    prompt = """This image is from a documentary about AI and facial animation.

Look carefully at this image. If there are facial motion capture markers (dots) visible on a person's face:
1. Count the markers on the NOSE BRIDGE (콧등)
2. Count the markers around BOTH EYES (양쪽 눈)
3. Count the markers on BOTH EYEBROWS (양쪽 눈썹)

Please provide:
- Number of markers on nose bridge: X
- Number of markers around eyes (total for both): X
- Number of markers on eyebrows (total for both): X
- Total count: X

If no facial markers are visible, just say "No facial markers visible".

Be very precise in counting. Look for small dots or tracking points on the face."""

    results = []

    for video in videos:
        video_dir = frames_dir / video
        if not video_dir.exists():
            print(f"Directory not found: {video_dir}")
            continue

        # 프레임 목록 가져오기 (시간순 정렬)
        frames = sorted([f for f in video_dir.glob("*.jpg")])
        print(f"\n=== {video} ===")
        print(f"Total frames: {len(frames)}")

        # 얼굴 마커가 있을 것 같은 구간 분석
        # 적정선은 어디인가: Mark Sagar 인터뷰 + 얼굴 캡처 장면
        # 약 3분~5분 구간 (frame 180~300 정도)

        if video == "적정선은_어디인가":
            # 더 넓은 범위 샘플링
            sample_indices = list(range(150, 350, 10))  # 2.5분~5.8분
        else:
            # 사랑 예술 그리고 이야기 - 얼굴 인식 관련 장면
            sample_indices = list(range(400, 600, 10))

        for idx in sample_indices:
            if idx >= len(frames):
                break

            frame = frames[idx]
            print(f"\nAnalyzing: {frame.name}")

            response = analyze_with_vlm(str(frame), prompt)

            if "marker" in response.lower() or "dot" in response.lower() or "point" in response.lower():
                print(f"FOUND MARKERS!")
                print(response[:500])
                results.append({
                    "video": video,
                    "frame": frame.name,
                    "response": response
                })

                # 마커를 찾으면 주변 프레임도 분석
                for nearby in range(-5, 6):
                    nearby_idx = idx + nearby
                    if 0 <= nearby_idx < len(frames) and nearby_idx != idx:
                        nearby_frame = frames[nearby_idx]
                        print(f"  Checking nearby: {nearby_frame.name}")
                        nearby_response = analyze_with_vlm(str(nearby_frame), prompt)
                        if "marker" in nearby_response.lower():
                            print(f"  Also has markers!")
                            results.append({
                                "video": video,
                                "frame": nearby_frame.name,
                                "response": nearby_response
                            })

    # 결과 저장
    output_path = frames_dir.parent / "face_marker_results.json"
    with open(output_path, "w") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print(f"\n\nResults saved to: {output_path}")
    print(f"Total frames with markers found: {len(results)}")

if __name__ == "__main__":
    main()
