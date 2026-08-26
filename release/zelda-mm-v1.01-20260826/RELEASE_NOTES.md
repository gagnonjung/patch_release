# 젤다의 전설: 무쥬라의 가면 한국어 패치 v1.01

- Edition: **v1.01 (2026-08-26)**
- `Nintendo 64` / `현대 컴보이 64` 로고 선택 패치를 한 패키지로 제공한다.
- xdelta 파일명과 ZIP 파일명에 버전 `v1.01`을 명시한다.
- 기준 원본은 일본판 Rev A BigEndian `.z64`이며 MD5/SHA-256을 모두 검증한다.

## v1.01
- `푸른물약`을 `파란 물약`으로 통일하고 아이템 이름 그래픽도 갱신했다.
- `마니야` / `전당포`를 `장물점`으로 통일했다.
- 데크 공주, 우유, 페더 소드, 진실의 가면, 가로 가면의 설명을 수정했다.
- 진실의 가면 설명을 `[C]로 쓰면 가십 스톤과 동물의 / 마음을 읽을 수 있다`로 정정했다.
- 봄버즈 수첩 번호 표기를 `1.` / `2.` / `3.` / `4.` 형식으로 수정했다.
- 키튼 퀴즈의 팅글 주문 선택지를 `바피푸페포 / 쿠루링파 / 빙글빙글빠`로 수정했다.
- `기～나긴 회의를 끝내 준 답례` 문구를 수정했다.
- 데크 공주 대사의 과도한 유아체를 정중한 공주 말투로 정리했다.
- `폭발 가면` 용어 통일 상태를 재검증했다.
- 기존 이름 입력, 황금 스탈튤라 카운터, 활공의 노래 목적지 런타임 패치가 보존됨을 정적 검증했다.
- v1.01 재빌드 중 발생한 런타임 DMA6 폰트/charmap 불일치를 수정했다. 현재 canonical DMA6과 짝인 `ko_charmap_owlwarp.json`으로 전체 메시지를 재컴파일했다.
- 이후 재발 방지를 위해 canonical ROM의 DMA6 SHA와 charmap SHA/mapping_count를 함께 검증하는 preflight를 추가했다.

## 검증
- 전체 메시지 4529/4529
- 레이아웃 hard failure 0
- 메시지 컴파일 PASS
- Yaz0 round-trip byte-exact PASS
- DMA16 / DMA26 / DMA28 readback byte-exact PASS
- DMADATA 및 ROM 크기 보존 PASS
- xdelta Nintendo 64 / 현대 컴보이 64 양쪽 decode 결과가 canonical ROM과 byte-exact PASS

패키지에는 원본 ROM이나 패치 완료 ROM을 포함하지 않는다.
