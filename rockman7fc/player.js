"use strict";
(() => {
  const $ = (id) => document.getElementById(id);
  const chooser = $("rom");
  const pause = $("pause");
  const reset = $("reset");
  const capture = $("capture");
  const status = $("status");
  const placeholder = $("placeholder");
  const frame = $("frame");
  const keyMap = {
    left: "BUTTON_LEFT", right: "BUTTON_RIGHT", up: "BUTTON_UP",
    down: "BUTTON_DOWN", a: "BUTTON_A", b: "BUTTON_B",
    start: "BUTTON_START", select: "BUTTON_SELECT"
  };
  let emulator = null, paused = false, filename = "";

  const tell = (message, isError = false) => {
    status.textContent = message;
    status.classList.toggle("error", isError);
  };
  function buttonState(active) {
    pause.disabled = !active;
    reset.disabled = !active;
    capture.disabled = !active;
  }
  async function playFile(file) {
    if (!file) return;
    if (!window.jsnes || !jsnes.Browser) {
      tell("에뮬레이터 라이브러리를 불러오지 못했습니다. 인터넷 연결 확인 후 새로고침하세요.", true);
      return;
    }
    try {
      tell("ROM 로딩 중…");
      const data = new Uint8Array(await file.arrayBuffer());
      if (data.length < 16 || data[0] !== 0x4e || data[1] !== 0x45 ||
          data[2] !== 0x53 || data[3] !== 0x1a) {
        throw new Error("유효한 iNES(.nes) 파일이 아닙니다.");
      }
      const mapper = (data[6] >>> 4) | (data[7] & 0xf0);
      if (emulator) emulator.destroy();
      emulator = null;
      const next = new jsnes.Browser({
        container: $("nes"),
        onError: (error) => tell("실행 오류: " + String(error), true)
      });
      try { next.loadROM(data); }
      catch (error) { next.destroy(); throw error; }
      emulator = next;
      filename = file.name;
      paused = false;
      pause.textContent = "일시정지";
      placeholder.classList.add("hidden");
      buttonState(true);
      tell("실행 중: " + filename + " · Mapper " + mapper + " · 파일 전송 없음");
      chooser.value = "";
    } catch (error) {
      tell("ROM 실행 실패: " + (error?.message || String(error)), true);
      if (!emulator) { buttonState(false); placeholder.classList.remove("hidden"); }
    }
  }
  chooser.addEventListener("change", () => playFile(chooser.files?.[0]));
  document.querySelector(".choose").addEventListener("keydown", (event) => {
    if (event.key === " " || event.key === "Enter") { event.preventDefault(); chooser.click(); }
  });
  pause.addEventListener("click", () => {
    if (!emulator) return;
    if (paused) emulator.start(); else emulator.stop();
    paused = !paused;
    pause.textContent = paused ? "계속하기" : "일시정지";
    tell((paused ? "일시정지: " : "실행 중: ") + filename);
  });
  reset.addEventListener("click", () => {
    if (!emulator) return;
    emulator.nes.reset();
    if (paused) { emulator.start(); paused = false; pause.textContent = "일시정지"; }
    tell("리셋 완료: " + filename);
  });
  $("full").addEventListener("click", async () => {
    try {
      if (!document.fullscreenElement) await frame.requestFullscreen();
      else await document.exitFullscreen();
    } catch (error) { tell("전체 화면 전환 실패: " + String(error), true); }
  });
  document.addEventListener("fullscreenchange", () => emulator?.fitInParent());
  capture.addEventListener("click", () => {
    if (!emulator) return;
    const a = document.createElement("a");
    a.href = emulator.screenshot().src;
    a.download = "rockman7fc.png";
    a.click();
  });
  for (const button of document.querySelectorAll("[data-pad]")) {
    const symbol = keyMap[button.dataset.pad];
    let pressed = false;
    function release() {
      if (!pressed) return;
      pressed = false;
      button.classList.remove("active");
      if (emulator) emulator.nes.buttonUp(1, jsnes.Controller[symbol]);
    }
    button.addEventListener("pointerdown", (event) => {
      if (!emulator || paused || pressed) return;
      event.preventDefault();
      pressed = true;
      button.classList.add("active");
      button.setPointerCapture(event.pointerId);
      emulator.nes.buttonDown(1, jsnes.Controller[symbol]);
    });
    ["pointerup", "pointercancel", "lostpointercapture"].forEach(
      (name) => button.addEventListener(name, release)
    );
    window.addEventListener("blur", release);
  }
  ["dragover", "dragenter"].forEach((name) => frame.addEventListener(name, (event) => {
    event.preventDefault(); frame.style.outline = "3px solid #d9fa72";
  }));
  frame.addEventListener("dragleave", () => { frame.style.outline = ""; });
  frame.addEventListener("drop", (event) => {
    event.preventDefault(); frame.style.outline = "";
    if (event.dataTransfer?.files?.length) playFile(event.dataTransfer.files[0]);
  });

  // Same-origin development ROM: load automatically when the page opens.
  // Local file selection is still available for testing other developer builds.
  async function loadBundledROM() {
    const name = "Rockman7FC_Freeze_MM6_Player_20261013.nes";
    try {
      tell("내장 NES 개발판을 불러오는 중…");
      const response = await fetch("./" + name, { cache: "no-cache" });
      if (!response.ok) throw new Error("HTTP " + response.status);
      const data = new Uint8Array(await response.arrayBuffer());
      if (data.length !== 253968 || data[0] !== 0x4e || data[1] !== 0x45 || data[2] !== 0x53 || data[3] !== 0x1a) {
        throw new Error("내장 ROM의 크기 또는 헤더가 맞지 않습니다.");
      }
      await playFile(new File([data], name, { type: "application/octet-stream" }));
    } catch (error) {
      tell("내장 ROM을 불러오지 못했습니다. NES ROM 선택으로 직접 열 수 있습니다: " + (error?.message || String(error)), true);
    }
  }
  loadBundledROM();
})();