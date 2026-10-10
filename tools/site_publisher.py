"""한마루 홈페이지 편집·배포 앱 (Python 3 + Tkinter, 표준 라이브러리만 사용).

Run 00_SITE_PUBLISHER.cmd from the repository root.
Push uses your preconfigured Git credentials, never stores a token.
"""
from __future__ import annotations

from pathlib import Path
import json
import threading
import webbrowser

from site_publisher_core import (
    DEFAULT, FIELDS, PLATFORMS, PublishError, draft_directory,
    preview, publish, load_published, run_git, validate,
)

REPO = Path(__file__).resolve().parent.parent
BASIC = ("slug", "title_ko", "title_en", "platform", "region", "genre",
         "original_release", "patch_version", "patch_date", "status", "credits", "intro")
PATCH = ("original_filename", "original_sha256", "patch_filename", "patch_sha256",
         "download_url", "features", "notes", "known_issues")
MEDIA = ("cover_file", "screenshot1", "screenshot2", "screenshot3")
MULTILINE = {"intro", "features", "notes", "known_issues"}

def main():
    import tkinter as tk
    from tkinter import filedialog, messagebox, ttk
    from tkinter.scrolledtext import ScrolledText

    class Editor(tk.Tk):
        def __init__(self):
            super().__init__()
            self.title("한마루 · 한국어 패치 홈페이지 편집기")
            self.geometry("970x790")
            self.minsize(830, 650)
            self.vars = {}
            self.inputs = {}
            self.busy = False
            self.repo = tk.StringVar(value=str(REPO))

            header = ttk.Frame(self, padding=(16, 13))
            header.pack(fill="x")
            ttk.Label(header, text="홈페이지 원클릭 편집·배포", font=("Malgun Gothic", 15, "bold")).pack(anchor="w")
            ttk.Label(header, text="새 게임 페이지를 작성하거나 앱으로 만든 페이지를 수정할 수 있습니다. 기존 수동 제작 페이지는 덮어쓰지 않습니다.").pack(anchor="w", pady=(4, 0))
            pathbar = ttk.Frame(header)
            pathbar.pack(fill="x", pady=(10, 0))
            ttk.Label(pathbar, text="Git 저장소").pack(side="left")
            ttk.Entry(pathbar, textvariable=self.repo, width=70).pack(side="left", fill="x", expand=True, padx=8)
            ttk.Button(pathbar, text="선택", command=self.choose_repo).pack(side="left")

            book = ttk.Notebook(self)
            book.pack(fill="both", expand=True, padx=16, pady=4)
            self.make_tab(book, "① 기본 정보", BASIC)
            self.make_tab(book, "② 배포·검수", PATCH)
            self.make_tab(book, "③ 표지·이미지", MEDIA)

            buttons = ttk.Frame(self, padding=(16, 8))
            buttons.pack(fill="x")
            ttk.Button(buttons, text="기본값 초기화", command=self.reset).pack(side="left", padx=(0, 8))
            ttk.Button(buttons, text="초안 불러오기", command=self.load_draft).pack(side="left", padx=(0, 8))
            ttk.Button(buttons, text="게시본 불러오기", command=self.load_remote).pack(side="left", padx=(0, 8))
            ttk.Button(buttons, text="초안 저장", command=self.save_draft).pack(side="left", padx=(0, 8))
            ttk.Button(buttons, text="브라우저 미리보기", command=self.show_preview).pack(side="left", padx=(0, 8))
            self.push_button = ttk.Button(buttons, text="GitHub에 게시 (푸시)", command=self.push)
            self.push_button.pack(side="right")

            footer = ttk.Frame(self, padding=(16, 0, 16, 12))
            footer.pack(fill="both")
            ttk.Label(footer, text="진행 기록", font=("Malgun Gothic", 10, "bold")).pack(anchor="w")
            self.log_box = ScrolledText(footer, height=6, wrap="word", state="disabled", font=("Consolas", 9))
            self.log_box.pack(fill="both", expand=True)
            self.log("배포 대상: GitHub origin/main · 기존 작업 브랜치와 dirty 파일은 건드리지 않습니다")
            self.log("주의사항 A~F는 다른 프로젝트의 정식 원문으로 고정되어 자동 포함됩니다")
            self.reset()

        def make_tab(self, book, title, keys):
            viewport = ttk.Frame(book)
            book.add(viewport, text=title)
            viewport.columnconfigure(0, weight=1)
            viewport.rowconfigure(0, weight=1)
            canvas = tk.Canvas(viewport, borderwidth=0, highlightthickness=0)
            canvas.grid(row=0, column=0, sticky="nsew")
            scrollbar = ttk.Scrollbar(viewport, orient="vertical", command=canvas.yview)
            scrollbar.grid(row=0, column=1, sticky="ns")
            canvas.configure(yscrollcommand=scrollbar.set)
            panel = ttk.Frame(canvas, padding=14)
            window = canvas.create_window((0, 0), window=panel, anchor="nw")
            panel.bind("<Configure>", lambda _e: canvas.configure(scrollregion=canvas.bbox("all")))
            canvas.bind("<Configure>", lambda e: canvas.itemconfigure(window, width=e.width))
            panel.columnconfigure(1, weight=1)
            for row, key in enumerate(keys):
                ttk.Label(panel, text=FIELDS[key], width=30).grid(row=row, column=0, sticky="nw", padx=(0, 10), pady=7)
                if key in MULTILINE:
                    widget = tk.Text(panel, height=4 if key == "intro" else 3, wrap="word", font=("Malgun Gothic", 10), undo=True)
                    widget.grid(row=row, column=1, sticky="nsew", padx=0, pady=4)
                    self.inputs[key] = widget
                else:
                    var = tk.StringVar()
                    self.vars[key] = var
                    if key == "platform":
                        widget = ttk.Combobox(panel, textvariable=var, values=list(PLATFORMS), state="readonly")
                    elif key == "status":
                        widget = ttk.Combobox(panel, textvariable=var, values=["배포 준비 중", "배포 중"], state="readonly")
                    else:
                        widget = ttk.Entry(panel, textvariable=var)
                    widget.grid(row=row, column=1, sticky="ew", pady=7)
                    if key in MEDIA:
                        ttk.Button(panel, text="이미지 선택", command=lambda k=key: self.choose_image(k)).grid(
                            row=row, column=2, sticky="w", padx=8)
            if title.startswith("③"):
                ttk.Label(panel, text="이미지는 PNG / JPG / WEBP · 16MB 이하\n선택한 파일은 게시 시 홈페이지 assets/images/<게임주소>/ 아래로 복사됩니다.",
                          foreground="#666").grid(row=8, column=0, columnspan=3, sticky="w", pady=10)

        def choose_repo(self):
            folder = filedialog.askdirectory(title="patch_release Git 저장소 선택", initialdir=self.repo.get())
            if folder:
                self.repo.set(folder)

        def choose_image(self, key):
            picked = filedialog.askopenfilename(title=FIELDS[key],
                filetypes=[("이미지", "*.png *.jpg *.jpeg *.webp"), ("모든 파일", "*.*")])
            if picked:
                self.vars[key].set(picked)

        def gather(self):
            data = {key: var.get().strip() for key, var in self.vars.items()}
            for key, widget in self.inputs.items():
                data[key] = widget.get("1.0", "end-1c").strip()
            return data

        def populate(self, data):
            merged = {**DEFAULT, **data}
            for key, var in self.vars.items():
                var.set(str(merged.get(key, "") or ""))
            for key, widget in self.inputs.items():
                widget.delete("1.0", "end")
                widget.insert("1.0", str(merged.get(key, "") or ""))

        def reset(self):
            self.populate(DEFAULT)

        def log(self, msg):
            self.log_box.configure(state="normal")
            self.log_box.insert("end", str(msg) + "\n")
            self.log_box.see("end")
            self.log_box.configure(state="disabled")

        def load_draft(self):
            selected = filedialog.askopenfilename(title="초안 JSON 불러오기", initialdir=str(draft_directory()),
                filetypes=[("사이트 초안", "*.json")])
            if not selected:
                return
            try:
                data = json.loads(Path(selected).read_text(encoding="utf-8"))
                if not isinstance(data, dict):
                    raise ValueError("잘못된 초안 형식입니다")
                self.populate(data)
                self.log(f"초안 불러옴: {selected}")
            except (OSError, ValueError) as exc:
                messagebox.showerror("불러오기 실패", str(exc))

        def load_remote(self):
            slug = self.vars["slug"].get().strip()
            if not slug:
                messagebox.showinfo("게시본 불러오기", "먼저 기본 정보 탭에 게임 페이지 주소(slug)를 입력하세요")
                return
            try:
                data = load_published(Path(self.repo.get()), slug)
                self.populate(data)
                self.log(f"게시본 불러옴: {slug} · 이미지 파일을 다시 고르지 않으면 공개된 기존 이미지를 유지합니다")
            except (OSError, ValueError, PublishError) as exc:
                messagebox.showerror("게시본 불러오기 실패", str(exc))

        def save_draft(self):
            try:
                d = validate(self.gather())
                file = draft_directory() / (d["slug"] + ".json")
                file.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
                self.log(f"초안 저장: {file}")
                return True
            except (ValueError, OSError, PublishError) as exc:
                messagebox.showerror("입력 확인", str(exc))
                return False

        def show_preview(self):
            try:
                d = self.gather()
                doc = preview(d)
                webbrowser.open(doc.as_uri())
                self.log(f"미리보기: {doc}")
            except (OSError, ValueError, PublishError) as exc:
                messagebox.showerror("미리보기 실패", str(exc))

        def push(self):
            if self.busy:
                return
            try:
                data = validate(self.gather())
                repo = Path(self.repo.get())
                if not repo.is_dir():
                    raise PublishError("저장소 경로를 찾지 못했습니다")
                origin = run_git(repo, ["remote", "get-url", "origin"])
            except (OSError, ValueError, PublishError) as exc:
                messagebox.showerror("게시 준비 실패", str(exc))
                return
            if not messagebox.askyesno("GitHub 게시 확인",
                    f"{data['title_ko']} · {data['patch_version']}\n"
                    f"대상: {origin}\n경로: {data['slug']}/index.html\n\n"
                    "미리보기를 확인했나요?\n"
                    "이 작업은 원격 main에 커밋을 게시합니다. 진행할까요?"):
                return
            self.save_draft()
            self.busy = True
            self.push_button.configure(state="disabled")

            def work():
                try:
                    commit = publish(repo, data,
                        progress=lambda line: self.after(0, self.log, line))
                except Exception as exc:
                    self.after(0, lambda err=str(exc): messagebox.showerror("게시 실패", err))
                else:
                    self.after(0, lambda: messagebox.showinfo("게시 완료",
                        f"GitHub origin/main 게시 완료\n커밋: {commit}\n\n"
                        f"페이지: {data['slug']}/"))
                finally:
                    self.after(0, self.finish_push)

            threading.Thread(target=work, daemon=True).start()

        def finish_push(self):
            self.busy = False
            self.push_button.configure(state="normal")

    Editor().mainloop()

if __name__ == "__main__":
    main()
