### Q6. 얼굴 마커 갯수 (콧등 + 양쪽 눈 + 눈썹)

#### 답안: (영상에서 직접 확인 필요)

#### 근거

영상 "사랑, 예술 그리고 이야기를 이해하다"에서 얼굴에 마커를 표시하여 감정표현을 해석하는 장면 분석이 필요합니다.

##### 문제 요구사항

다음 부위의 마커 갯수 합계:
- 콧등
- 양쪽 눈
- 눈썹

##### 트랜스크립트 관련 내용

```
[el Kaliouby] Only 10% of the signal we use to communicate with one another is the choice of words we use.
90% is non-verbal. About half of that is your facial expressions, your use of gestures.

So what people in the field of machine learning and computer vision have done
is they've trained a machine or an algorithm to become a certified face-reader.

Computer vision is this idea that our machines are able to see.
Maybe it detects that there's a face in the image.
Once you find the face, you want to identify these building blocks of these emotional expressions.

You wanna know that there's a smirk, or a there's a brow raise,
or, you know, an asymmetric lip corner pull.
```

##### 확인 방법

영상에서 얼굴 마커가 표시된 장면을 찾아 다음을 세어야 합니다:
1. 콧등(nose bridge)의 마커 수
2. 왼쪽 눈 주변 마커 수
3. 오른쪽 눈 주변 마커 수
4. 왼쪽 눈썹 마커 수
5. 오른쪽 눈썹 마커 수

※ 이 문제는 영상의 특정 프레임에서 마커를 직접 세어야 정확한 답을 얻을 수 있습니다.
