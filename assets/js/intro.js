const root = document.querySelector('.codec-intro');
const answer = document.getElementById('answer');
const callAudio = document.getElementById('codec-call-audio');
const answerAudio = document.getElementById('codec-answer-audio');
const audioToggle = document.getElementById('audio-toggle');
const pushSelect = document.querySelector('.push-select');

const muteKey = 'mgsCodecMuted';
let muted = false;
let navigating = false;

try {
  muted = localStorage.getItem(muteKey) === '1';
} catch (_) {}

function updateAudioButton() {
  if (!audioToggle) return;
  audioToggle.textContent = muted ? '소리 켜기 / UNMUTE' : '음소거 / MUTE';
  audioToggle.setAttribute('aria-pressed', muted ? 'true' : 'false');
}

function applyMuteState() {
  if (callAudio) callAudio.muted = muted;
  if (answerAudio) answerAudio.muted = muted;
  updateAudioButton();
}

async function startCallAudio() {
  if (!callAudio || muted || root?.classList.contains('connecting')) return;
  try {
    await callAudio.play();
    root?.classList.remove('audio-blocked');
  } catch (_) {
    root?.classList.add('audio-blocked');
  }
}

function unlockCallAudio() {
  if (!muted && callAudio?.paused && !root?.classList.contains('connecting')) {
    startCallAudio();
  }
}

function goHome() {
  if (navigating) return;
  navigating = true;
  window.location.href = 'patch.html';
}

async function playAnswerThenGoHome() {
  if (!answerAudio || muted) {
    setTimeout(goHome, 650);
    return;
  }

  answerAudio.currentTime = 0;
  answerAudio.addEventListener('ended', goHome, { once: true });
  answerAudio.addEventListener('error', () => setTimeout(goHome, 1000), { once: true });

  try {
    await answerAudio.play();
  } catch (_) {
    setTimeout(goHome, 1000);
  }
}

function connect() {
  if (!root || !answer || root.classList.contains('connecting')) return;

  root.classList.add('connecting');
  answer.setAttribute('aria-label', 'CONNECTING');
  if (pushSelect) pushSelect.textContent = 'CONNECTING...';

  if (callAudio) {
    callAudio.pause();
    callAudio.currentTime = 0;
  }

  playAnswerThenGoHome();
}

applyMuteState();
startCallAudio();

audioToggle?.addEventListener('click', (event) => {
  event.stopPropagation();
  muted = !muted;
  try {
    localStorage.setItem(muteKey, muted ? '1' : '0');
  } catch (_) {}
  applyMuteState();
  if (!muted) startCallAudio();
});

document.addEventListener('pointerdown', unlockCallAudio, { once: true });
document.addEventListener('keydown', unlockCallAudio, { once: true });

answer?.addEventListener('click', connect);
document.addEventListener('keydown', (event) => {
  if (event.key === 'Enter' || event.key === ' ') {
    event.preventDefault();
    connect();
  }
});
