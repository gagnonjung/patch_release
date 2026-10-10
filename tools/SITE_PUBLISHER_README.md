# 한마루 한글패치 홈페이지 편집·배포 앱

실행: 루트 폴더의 **`00_SITE_PUBLISHER.cmd`** 더블클릭

Windows용 로컬 GUI (Python 3 기본 Tkinter 사용, 별도 pip 설치 없음)입니다. Git 설치와 기존 GitHub 인증을 그대로 사용하므로 앱에 GitHub 토큰·비밀번호를 입력하거나 저장하지 않습니다.

## 사용하는 방법

1. 프로젝트 `patch_release` 폴더에서 `00_SITE_PUBLISHER.cmd`를 실행합니다
2. **기본 정보**: 영문 URL 주소(slug), 게임명, 기종, 버전, 소개를 입력합니다
3. **배포·검수**: 원본 SHA-256과 Google Drive 링크, ZIP 정보, 한국어화 범위 등을 입력합니다. 아직 배포하지 않는 게임은 상태를 **배포 준비 중**으로 두면 링크 없이 게시할 수 있습니다
4. **표지·이미지**: PC에 저장된 PNG/JPG/WEBP 표지와 최대 3장의 스크린샷을 선택합니다
5. **초안 저장**: `%USERPROFILE%\.hanmaru_site_publisher\drafts`에 JSON 저장
6. **브라우저 미리보기**: 패치 페이지를 HTML로 렌더링해서 확인합니다
7. **GitHub에 게시 (푸시)**: 게시 대상 저장소/URL을 확인하고 승인하면 자동 반영됩니다

## 자동화 범위

- `<slug>/index.html`: 사이트 템플릿으로 상세 페이지 생성
- `index.html`: 기존 갤러리 상단에 게임 카드 추가 (앱 관리 카드 업데이트 시 중복 생성하지 않음)
- `assets/images/<slug>/`: 로컬 이미지 복사
- `site_publisher/entries/<slug>.json`: 재편집을 위한 입력 데이터 기록
- **하단 A~F 주의사항은 공통 `tools/site_legal.py` 원문 고정**. 게임마다 축약/변경하지 않습니다

**안전 규칙:** 기존 수작업 상세 페이지는 자동 편집기가 덮어쓰지 않습니다. 앱에서 만든 페이지만 후속 업데이트할 수 있습니다. Git 최신 `origin/main`에서 별도 임시 worktree를 만들고 **사이트에 필요한 파일만** 커밋/푸시합니다. 현재 로컬 `main`에 수정·스테이징된 파일이나 게임 패치 작업 폴더는 건드리지 않습니다. 푸시가 거부되면 강제 푸시는 하지 않으며 임시 작업 폴더를 남깁니다.

**앱은 정적 웹페이지를 GitHub에 게시합니다.** 패치 ZIP 자체를 Google Drive에 업로드하는 기능은 없습니다. 먼저 업로드하고 다운로드 링크를 입력합니다. GitHub Pages 갱신은 GitHub 측 배포 완료까지 시간이 걸릴 수 있습니다.

## 명령행 QA

```shell
python tools/site_legal.py
python -m unittest tools/test_site_publisher.py -v
```

개발 기본값: Python 3.10 이상 / Git CLI.
