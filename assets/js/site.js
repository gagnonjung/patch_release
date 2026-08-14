const release = {
  status: "FINAL RELEASE",
  title: "MGS_TTS_KO_v1.0_xdelta_windows.zip",
  version: "1.0",
  date: "2026-08-15",
  size: "133.02 MiB / 139,478,459 bytes",
  provider: "MEGA",
  url: "https://mega.nz/file/pm9T3ApS#X6fAnfwQplNY41qfABQKMZD_iLeW82BcrccT5gOjyGs",
  patchSha256: "9b9acbd1fbcd0196275d202217842339ae25a6420a5131f7d1b021a99ef01448",
  sourceSha256: "Disc 1: c514c3a672cf3587be87af9874629dfe31b21f92a46e760a9d7ba317f0399591 / Disc 2: e1fac2270a95eb40781af29db67d2c741931bc96e884931e42371c036e94a4e4"
};

const setText = (id, value) => {
  const el = document.getElementById(id);
  if (el) el.textContent = value;
};

setText("release-status", release.status);
setText("release-title", release.title);
setText("release-version", release.version);
setText("release-date", release.date);
setText("release-size", release.size);
setText("release-provider", release.provider);
setText("patch-hash", release.patchSha256);
setText("source-hash", release.sourceSha256);

const link = document.getElementById("release-link");
if (link && release.url) {
  link.href = release.url;
  link.textContent = `DOWNLOAD — ${release.provider}`;
  link.classList.remove("disabled");
  link.removeAttribute("aria-disabled");
  link.target = "_blank";
  link.rel = "noopener noreferrer";
}

const codecMeterBars = [...document.querySelectorAll(".codec-meter i")];
if (codecMeterBars.length) {
  let level = 3;
  let target = 5;

  const updateCodecMeter = () => {
    if (Math.random() < 0.38 || level === target) {
      target = Math.floor(Math.random() * (codecMeterBars.length + 1));
      if (Math.random() < 0.12) target = codecMeterBars.length;
    }

    const distance = target - level;
    if (distance !== 0) {
      const step = Math.min(Math.abs(distance), 1 + Math.floor(Math.random() * 3));
      level += Math.sign(distance) * step;
    }

    codecMeterBars.forEach((bar, index) => {
      bar.classList.toggle("active", index < level);
    });

    window.setTimeout(updateCodecMeter, 70 + Math.random() * 100);
  };

  updateCodecMeter();
}

const codecDialogue = document.querySelector(".codec-dialogue p");
if (codecDialogue) {
  const fullText = codecDialogue.textContent.trim();
  const characters = Array.from(fullText);
  let index = 0;

  codecDialogue.textContent = "";
  codecDialogue.classList.add("typing");

  const nextDelay = (char) => {
    if (char === "…") return 240;
    if (char === "," || char === "·") return 150;
    if (char === "." || char === "?" || char === "!") return 320;
    if (char === " ") return 35;
    return 48 + Math.random() * 42;
  };

  const typeNext = () => {
    if (index >= characters.length) {
      codecDialogue.classList.remove("typing");
      return;
    }

    const char = characters[index++];
    codecDialogue.textContent += char;
    window.setTimeout(typeNext, nextDelay(char));
  };

  window.setTimeout(typeNext, 380);
}

const pageBgm = document.getElementById("page-bgm");
const bgmToggle = document.getElementById("bgm-toggle");
const bgmMute = document.getElementById("bgm-mute");

if (pageBgm) {
  pageBgm.volume = 0.5;

  const syncBgmControls = () => {
    if (bgmToggle) {
      bgmToggle.textContent = pageBgm.paused ? "PLAY" : "STOP";
      bgmToggle.setAttribute("aria-pressed", String(!pageBgm.paused));
    }
    if (bgmMute) {
      bgmMute.textContent = pageBgm.muted ? "UNMUTE" : "MUTE";
      bgmMute.setAttribute("aria-pressed", String(pageBgm.muted));
    }
  };

  const playBgm = async () => {
    try {
      await pageBgm.play();
      syncBgmControls();
      return true;
    } catch (_) {
      syncBgmControls();
      return false;
    }
  };

  const startAfterInteraction = async (event) => {
    if (event?.target?.closest?.(".bgm-controls")) return;
    document.removeEventListener("pointerdown", startAfterInteraction, true);
    document.removeEventListener("keydown", startAfterInteraction, true);
    await playBgm();
  };

  playBgm().then((started) => {
    if (!started) {
      document.addEventListener("pointerdown", startAfterInteraction, true);
      document.addEventListener("keydown", startAfterInteraction, true);
    }
  });

  bgmToggle?.addEventListener("click", async () => {
    document.removeEventListener("pointerdown", startAfterInteraction, true);
    document.removeEventListener("keydown", startAfterInteraction, true);

    if (pageBgm.paused) {
      await playBgm();
    } else {
      pageBgm.pause();
      pageBgm.currentTime = 0;
      syncBgmControls();
    }
  });

  bgmMute?.addEventListener("click", () => {
    pageBgm.muted = !pageBgm.muted;
    syncBgmControls();
  });

  pageBgm.addEventListener("play", syncBgmControls);
  pageBgm.addEventListener("pause", syncBgmControls);
  pageBgm.addEventListener("volumechange", syncBgmControls);
  syncBgmControls();
}
