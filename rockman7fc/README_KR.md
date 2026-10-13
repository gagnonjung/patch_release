# 록맨7 FC — GitHub Pages 웹 플레이어

공개 페이지: https://gagnonjung.github.io/patch_release/rockman7fc/

소스 저장소: https://github.com/gagnonjung/patch_release/tree/main/rockman7fc

## 구동 방법

1. 위 페이지를 엽니다
2. **NES ROM 선택**을 누릅니다
3. 아래 개발 빌드의 NES ROM을 선택합니다

`release/20261013_Rockman7FC_Freeze_MM6_Player_Alpha/Rockman7FC_Freeze_MM6_Player_20261013.nes`

키보드: 방향키, 점프 X, 버스터 Z, 슬라이딩 아래+X, START Enter, SELECT 오른쪽 Ctrl

터치 버튼, 게임패드, 전체화면, 스크린샷, 일시정지, 리셋을 지원합니다

## 배포 원칙 및 검증

- 웹 공개본은 HTML과 JavaScript만 포함합니다. 게임 ROM 및 원본 게임 리소스는 공개하지 않습니다
- NES ROM은 로컬 브라우저 File API로 읽으며 서버 업로드 기능이 없습니다
- JSNES 2.1.0 (Apache-2.0)을 CDN에서 불러옵니다
- GitHub Pages 및 player.js 응답 HTTP 200, JavaScript 구문 검사 통과
- 실제 브라우저에서 포팅 ROM 구동 및 키 입력/소리/그래픽의 전수 런타임 QA는 미완료입니다
- 개발 ROM은 록맨6 조작계 적용 프리즈맨 29방 기술 테스트판이며 완성된 록맨7은 아닙니다
