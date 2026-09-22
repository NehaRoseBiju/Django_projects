/**
 * PulseMind Hub - WebRTC Video Call & Realtime Consultation Script
 */

let localStream = null;
let remoteStream = null;
let peerConnection = null;
let isAudioMuted = false;
let isVideoOff = false;
let callDurationSeconds = 0;
let callTimerInterval = null;

const configuration = {
  iceServers: [
    { urls: 'stun:stun.l.google.com:19302' },
    { urls: 'stun:stun1.l.google.com:19302' }
  ]
};

document.addEventListener('DOMContentLoaded', () => {
  initLocalVideo();
  setupChat();
});


async function initLocalVideo() {
  const localVideo = document.getElementById('localVideo');
  const callStatus = document.getElementById('callStatus');

  try {
    localStream = await navigator.mediaDevices.getUserMedia({
      video: true,
      audio: true
    });
    if (localVideo) {
      localVideo.srcObject = localStream;
    }
    if (callStatus) {
      callStatus.innerHTML = "<span style='color: #34d399;'>●</span> Your Camera & Mic Active";
    }

    startTimer();
  } catch (err) {
    console.warn("Camera/Mic access not granted or unavailable, utilizing demo media stream for local PIP:", err);
    if (callStatus) {
      callStatus.innerText = "Camera Permission Needed (Local Preview)";
    }
    setupLocalDemoStream();
    startTimer();
  }
}

function setupLocalDemoStream() {
  const localVideo = document.getElementById('localVideo');
  const canvas = document.createElement('canvas');
  canvas.width = 320;
  canvas.height = 240;
  const ctx = canvas.getContext('2d');

  let frame = 0;
  function draw() {
    ctx.fillStyle = '#0f766e';
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    ctx.strokeStyle = '#2dd4bf';
    ctx.lineWidth = 4;
    ctx.beginPath();
    ctx.arc(160, 120, 40 + Math.sin(frame * 0.1) * 5, 0, Math.PI * 2);
    ctx.stroke();

    ctx.fillStyle = '#ffffff';
    ctx.font = '14px Outfit, sans-serif';
    ctx.fillText("Your Local Camera", 100, 180);

    frame++;
    requestAnimationFrame(draw);
  }
  draw();

  const canvasStream = canvas.captureStream(30);
  if (localVideo) localVideo.srcObject = canvasStream;
}


function startTimer() {
  const timerElem = document.getElementById('callTimer');
  if (!timerElem || callTimerInterval) return;

  callTimerInterval = setInterval(() => {
    callDurationSeconds++;
    const mins = String(Math.floor(callDurationSeconds / 60)).padStart(2, '0');
    const secs = String(callDurationSeconds % 60).padStart(2, '0');
    timerElem.innerText = `${mins}:${secs}`;
  }, 1000);
}

function toggleAudio() {
  if (!localStream) return;
  const audioTrack = localStream.getAudioTracks()[0];
  if (audioTrack) {
    isAudioMuted = !isAudioMuted;
    audioTrack.enabled = !isAudioMuted;
    const btn = document.getElementById('btnMuteAudio');
    if (btn) {
      btn.classList.toggle('muted', isAudioMuted);
      btn.innerHTML = isAudioMuted ? '🔇' : '🎙️';
    }
  }
}

function toggleVideo() {
  if (!localStream) return;
  const videoTrack = localStream.getVideoTracks()[0];
  if (videoTrack) {
    isVideoOff = !isVideoOff;
    videoTrack.enabled = !isVideoOff;
    const btn = document.getElementById('btnToggleVideo');
    if (btn) {
      btn.classList.toggle('muted', isVideoOff);
      btn.innerHTML = isVideoOff ? '📷❌' : '📹';
    }
  }
}

async function shareScreen() {
  try {
    const screenStream = await navigator.mediaDevices.getDisplayMedia({ video: true });
    const localVideo = document.getElementById('localVideo');
    if (localVideo) localVideo.srcObject = screenStream;
    alert("Screen sharing started.");
  } catch (err) {
    console.log("Screen share cancelled or failed:", err);
  }
}

function simulateParticipantJoin() {
  const remoteVideo = document.getElementById('remoteVideo');
  const waitingOverlay = document.getElementById('remoteWaitingOverlay');
  const callStatus = document.getElementById('callStatus');

  if (waitingOverlay) waitingOverlay.style.display = 'none';
  if (remoteVideo) remoteVideo.style.display = 'block';

  const canvas = document.createElement('canvas');
  canvas.width = 640;
  canvas.height = 480;
  const ctx = canvas.getContext('2d');

  let frame = 0;
  function draw() {
    ctx.fillStyle = '#064e3b';
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    // Waveform
    ctx.strokeStyle = '#34d399';
    ctx.lineWidth = 5;
    ctx.beginPath();
    ctx.moveTo(50, 240);
    ctx.lineTo(220, 240);
    ctx.lineTo(260, 240 - Math.sin(frame * 0.1) * 50);
    ctx.lineTo(300, 240 + Math.sin(frame * 0.1) * 70);
    ctx.lineTo(340, 240 - Math.sin(frame * 0.1) * 90);
    ctx.lineTo(380, 240);
    ctx.lineTo(590, 240);
    ctx.stroke();

    ctx.fillStyle = '#ffffff';
    ctx.font = '22px Outfit, sans-serif';
    ctx.fillText("Remote Doctor Consultation Feed", 160, 100);
    ctx.fillText("Connected via WebRTC Stream", 175, 400);

    frame++;
    requestAnimationFrame(draw);
  }
  draw();

  const remoteCanvasStream = canvas.captureStream(30);
  if (remoteVideo) remoteVideo.srcObject = remoteCanvasStream;

  if (callStatus) {
    callStatus.innerHTML = "<span style='color: #34d399;'>● Connected:</span> Remote Participant Live";
  }

  // Add notification message in chat
  const chatMessages = document.getElementById('chatMessages');
  if (chatMessages) {
    const sysDiv = document.createElement('div');
    sysDiv.className = 'chat-msg received';
    sysDiv.style.background = '#d1fae5';
    sysDiv.style.color = '#065f46';
    sysDiv.innerHTML = "<strong>System:</strong> Remote doctor has entered the video room.";
    chatMessages.appendChild(sysDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
  }
}

function endCall() {
  if (confirm("Are you sure you want to end this consultation call?")) {
    if (callTimerInterval) clearInterval(callTimerInterval);
    if (localStream) {
      localStream.getTracks().forEach(track => track.stop());
    }
    alert("Call ended. Thank you for using PulseMind Hub.");
    window.location.href = "/";
  }
}

function setupChat() {
  const chatForm = document.getElementById('chatForm');
  const chatInput = document.getElementById('chatInput');
  const chatMessages = document.getElementById('chatMessages');

  if (chatForm && chatInput && chatMessages) {
    chatForm.addEventListener('submit', (e) => {
      e.preventDefault();
      const text = chatInput.value.trim();
      if (!text) return;

      const msgDiv = document.createElement('div');
      msgDiv.className = 'chat-msg sent';
      msgDiv.innerText = text;
      chatMessages.appendChild(msgDiv);
      chatInput.value = '';
      chatMessages.scrollTop = chatMessages.scrollHeight;

      setTimeout(() => {
        const replyDiv = document.createElement('div');
        replyDiv.className = 'chat-msg received';
        replyDiv.innerText = "Thank you. I have received your message in the consultation session.";
        chatMessages.appendChild(replyDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
      }, 1500);
    });
  }
}
