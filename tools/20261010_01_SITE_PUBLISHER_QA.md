# 2026-10-10 홈페이지 편집기 검증 체크포인트

## 대상
- `00_SITE_PUBLISHER.cmd`
- `tools/site_publisher.py`: Tkinter 입력·초안·미리보기·원격 게시 GUI
- `tools/site_publisher_core.py`: HTML 템플릿, 이미지·입력 검증, 임시 worktree/커밋/푸시
- `tools/site_legal.py`: 다른 프로젝트와 **동일한 A~F 고지 단일 기준**
- `tools/test_site_publisher.py`: 테스트용 로컬 bare Git 원격을 사용한 무외부망 검증

## 완료
1. `getter-robo-daikessen/index.html`, `slayers-royal/index.html`, `persona-2-innocent-sin/index.html`의 주의사항 A~F를 메탈 기어·젤다 기존 원문과 동일하게 정리
2. 실 서비스 5개 게임 상세 페이지 × 6항목 전수 감사 PASS
3. Windows Python 3.14.5 스크립트 문법 검사 PASS
4. Windows Git 2.40.1 환경에서 단위 테스트 5건 PASS
5. 미리보기 이스케이프(XSS 방지) 및 필수 입력·SHA-256·HTTPS URL 검증 PASS
6. 테스트용 Git 원격에서 신규 등록·수정 게시·원격 Git push·갤러리 카드 중복 방지 PASS
7. 로컬 `main`에 미반영 수정이 있는 상태에서도 편집기 게시가 기존 파일을 훼손하지 않는지 확인 PASS
8. 앱 관리 이력이 없는 기존 수동 페이지를 덮어쓰지 않도록 차단 PASS

## 비고
- 실제 공개 GitHub로 GUI에서 테스트 데이터를 게시하지 않음 (의도적으로 테스트 원격 사용)
- 실 사이트는 기존 정식 디자인을 보존하고 고지 전문만 통일
- GitHub 토큰은 앱에서 저장·요구하지 않음. Git CLI의 기존 인증 사용
- 패치 ZIP의 Google Drive 업로드는 별도 작업: 앱은 URL을 받아 HTML을 게시
- 에뮬레이터·게임 BIN/CUE 및 번역 프로젝트 파일 작업 없음
