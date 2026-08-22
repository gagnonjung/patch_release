const release = {
  status: "BUGFIX RELEASE",
  title: "MGS_TTS_KO_v1.11_xdelta_windows.zip",
  version: "1.11",
  date: "2026-08-23",
  size: "133.49 MiB / 139,977,986 bytes",
  provider: "GOOGLE DRIVE",
  url: "https://drive.google.com/file/d/1dI9TfL_eiRmlsL2ldWLu5zeGzXoQHkyO/view?usp=sharing",
  patchSha256: "36dba5eb935a7a8f6f5b9f5a95a5af3af6760bb0ec940e780e273b589c10a7da"
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
setText("patch-hash", release.patchSha256);

const link = document.getElementById("release-link");
if (link && release.url) {
  link.href = release.url;
  const label = link.querySelector("span:last-child");
  if (label) label.textContent = `DOWNLOAD — ${release.provider}`;
  else link.textContent = `DOWNLOAD — ${release.provider}`;
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
