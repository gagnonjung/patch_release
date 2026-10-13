# 록맨7 FC — GitHub Pages 내장 NES 플레이어

웹 실행: https://gagnonjung.github.io/patch_release/rockman7fc/

사이트에 접속하면 개발용 NES ROM을 자동으로 불러옵니다. `NES ROM 선택`은 다른 로컬 개발 빌드 테스트용으로 유지합니다.

## 내장 테스트 ROM

- 파일: `Rockman7FC_Freeze_MM6_Player_20261013.nes`
- 크기: `253,968 bytes`
- SHA-256: `80a67b84cac73b60f14cabd857797a20b53dac860254071d278a083dceb32dce`
- Mapper: `4` (MMC3)
- 원본 작업 위치: `NES_Rockman7FC_Port/release/20261013_Rockman7FC_Freeze_MM6_Player_Alpha/`
- 내용: 프리즈맨 29개 방, 록맨6 기반 이동·점프·슬라이딩·록버스터·차지샷
- **록맨7 전체 이식본이 아닌 개발판**이며 원작 록맨6의 동작을 프레임 단위로 완전히 재현한 상태가 아닙니다.

## 조작 및 구현

키보드: 방향키 이동, X 점프, Z 록버스터/차지, 아래+X 슬라이딩, Enter START, 오른쪽 Ctrl SELECT.
터치 D패드/A/B/START/SELECT, 게임패드, 전체 화면, 리셋, 일시정지 및 스크린샷을 제공합니다.
에뮬레이터는 JSNES 2.1.0 (Apache-2.0) CDN 라이브러리를 사용합니다.

## 공개 배포 및 QA

- ROM은 이 공개 GitHub 저장소에 포함돼 있어 누구나 조회·다운로드할 수 있습니다.
- 비공식 팬게임 포팅이므로 상표·그래픽·음악 등 원작 권리관계를 확인해야 합니다.
- 상용 게임 록맨6의 원본 ROM은 여기에 업로드하지 않았습니다.
- 게임 플레이·사운드·입력의 실제 브라우저 완전 검증은 별도입니다.
