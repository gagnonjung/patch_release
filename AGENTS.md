# 한마루 패치 배포 사이트 작업 규칙

게임별 한국어 패치 상세 페이지를 **새로 만들거나 수정·업로드할 때 반드시** `.agents/skills/hanmaru-patch-page/SKILL.md`를 읽고 적용한다.

- 트리거: "패치 페이지 만들어", "패치 페이지 업로드", "사이트에 게임 등록", "한글패치 페이지 수정", "홈페이지 작업" 중 게임별 상세 페이지 작업 전반
- 1:1 디자인 기준: `persona-2-innocent-sin/index.html`
- 새턴 페이지 참고: `slayers-royal/index.html`
- 고정 규정: `SITE_DETAIL_LAYOUT_STANDARD.md`
- 검증: `python tools/verify_detail_template.py <slug>` + 데스크톱·모바일 시각 검수
- 원본·패치 파일 및 검증된 해시·링크 보존. 테스트 환경의 정적/실기 여부 구별
- 사용자가 푸시를 지시한 경우에만 변경 범위 검증 후 커밋/푸시. 배포된 링크 그대로 사용

별도 상세 페이지 전용 CSS나 임의 레이아웃을 만들지 않는다. 예외는 사용자가 명시적으로 요청한 경우뿐이다.
