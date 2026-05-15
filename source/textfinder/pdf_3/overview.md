# PDF 3 Overview

## 문서 정보
- **파일명**: pdf_3.pdf
- **페이지 수**: 25
- **추출된 이미지**: 28개

## 문서 제목
**EcAMSat – NASA's First 6U Biological Spacecraft: System Integration and Environmental Test**

## 저자
Matthew Chin, Stevan Spremo, Timothy V. Snyder, Chris Rogers, Antonio J. Ricco, Aaron Cohen, Tori N. Chinn, Michael R. Padgen, Charlie R. Friedericks, Mike Henschke, Macarena Parra, Leland Taylor, Matt Lera, Chris Lorenzen, Kimberly Jenks, Christopher Kitts, Mike Rasay

## 내용 요약
NASA Ames Research Center에서 설계한 최초의 6U 생물학 우주선 EcAMSat(E. coli AntiMicrobial Satellite)에 대한 기술 보고서입니다.

### 미션 개요
- EcAMSat은 GeneSat1, O/OREOS, PharmaSat, MisST 등 과거 큐브샛 유산을 활용
- 6U 산업 표준 정의에 기여
- NPR 7120.5E 및 NPR 8705.4 (Class D 미션) 표준 준수

### 주요 기술 내용

#### 기계 설계
- 2U 페이로드 + 1U BUS 구성
- 6개의 3U 바디 마운트 태양 패널 사용
- NLAS(Nanosat Launch Adapter System) 디스펜서 호환

#### ADCS (자세 제어 시스템)
- 영구 자석 및 히스테리시스 막대를 이용한 수동 자세 제어
- PharmaSat 대비 영구 자석 24개→54개, 히스테리시스 막대 16개→36개로 증가
- MatLab 및 STK 시뮬레이션 수행

#### 소프트웨어
- PIC18 마이크로컨트롤러용 임베디드 C 프로그래밍
- ISS 요구사항: 배치 후 90분간 라디오 오프 상태 유지

#### 열/전기 문제 해결
- 페이로드 히터 듀티 사이클 90%→59%로 감소
- 구리 호일 테이프를 이용한 열 균형 조정
- Tiger Team 구성하여 문제 해결

### 환경 테스트 프로그램
1. **ESS (Environmental Stress Screening)**: 열 사이클링 테스트
2. **TVPM (Thermal Vacuum Power Management)**: 비행 조건 시뮬레이션
3. **충격 테스트**: GEVS Protoflight 자격 수준
4. **진동 테스트**: 무작위 진동 테스트 (14.1 GRMS)
5. **RF 통신 테스트**: 안테나 주파수 튜닝 및 링크 마진 테스트

### 교훈
- 고고도 미션의 전력 예산 평가에는 콜드/핫 소크 대신 열 사이클링 권장
- 맞춤형 NPR 7120.5 접근 방식의 성공적 검증

## 추출된 자료
- **텍스트**: content.txt
- **메타데이터**: metadata.txt
- **이미지**: 28개 (`images/` 폴더)
