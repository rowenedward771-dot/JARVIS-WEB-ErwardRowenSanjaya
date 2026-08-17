import os
import io
import requests
from flask import Flask, request, jsonify, Response

app = Flask(__name__)

# ============================================================
# CONFIGURATION
# ============================================================

GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")

CHAT_MODEL = "llama-3.3-70b-versatile"
WHISPER_MODEL = "whisper-large-v3-turbo"
CREATOR = "Erward Rowen Sanjaya"

# ============================================================
# HTML, STYLES & JAVASCRIPT DASHBOARD
# ============================================================

HTML_TEMPLATE = r"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<title>STARK AI SYSTEM // J.A.R.V.I.S & F.R.I.D.A.Y</title>
<style>
:root {
    --primary: #00eaff;
    --primary-glow: rgba(0, 234, 255, 0.4);
    --bg-dark: #02060d;
    --panel-bg: rgba(3, 15, 28, 0.75);
    --border-color: rgba(0, 234, 255, 0.3);
    --text-color: #e8faff;
    --accent-red: #ff3154;
}

[data-theme="female"] {
    --primary: #ff007f;
    --primary-glow: rgba(255, 0, 127, 0.4);
    --panel-bg: rgba(25, 3, 18, 0.75);
    --border-color: rgba(255, 0, 127, 0.3);
}

* { box-sizing: border-box; transition: color 0.3s, border-color 0.3s, box-shadow 0.3s; }
html, body { margin: 0; padding: 0; min-height: 100vh; background: var(--bg-dark); color: var(--text-color); font-family: 'Segoe UI', system-ui, -apple-system, sans-serif; overflow-x: hidden; }

/* BACKGROUND HUD GRID */
.bg-grid { position: fixed; inset: 0; z-index: -10; overflow: hidden; background: radial-gradient(circle at 50% 50%, #07263b 0%, #020813 60%, #010408 100%); }
.grid-lines { position: absolute; width: 200%; height: 200%; left: -50%; top: -50%; background-image: linear-gradient(var(--border-color) 1px, transparent 1px), linear-gradient(90deg, var(--border-color) 1px, transparent 1px); background-size: 60px 60px; transform: perspective(600px) rotateX(60deg); animation: gridMove 15s linear infinite; opacity: 0.15; }
@keyframes gridMove { 0% { transform: perspective(600px) rotateX(60deg) translateY(0); } 100% { transform: perspective(600px) rotateX(60deg) translateY(60px); } }

.scanline { position: fixed; inset: 0; pointer-events: none; background: linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.25) 50%); background-size: 100% 4px; z-index: 999; opacity: 0.6; }

/* LOGIN OVERLAY */
#loginOverlay { position: fixed; inset: 0; z-index: 2000; background: rgba(1, 4, 10, 0.95); backdrop-filter: blur(25px); display: flex; align-items: center; justify-content: center; padding: 20px; }
.loginCard { width: min(480px, 100%); padding: 40px; border: 1px solid var(--primary); border-radius: 20px; background: rgba(5, 18, 32, 0.9); box-shadow: 0 0 50px var(--primary-glow); text-align: center; position: relative; overflow: hidden; }
.loginCard h1 { margin: 0 0 10px; font-size: 28px; letter-spacing: 6px; color: var(--primary); text-shadow: 0 0 15px var(--primary); }
.loginCard p { color: #81a4b0; font-size: 13px; margin-bottom: 25px; }

.gender-select { display: flex; gap: 15px; margin-bottom: 25px; }
.gender-btn { flex: 1; padding: 14px; border: 1px solid var(--border-color); border-radius: 12px; background: rgba(2, 12, 22, 0.8); color: #81a4b0; cursor: pointer; font-weight: bold; letter-spacing: 2px; font-size: 12px; }
.gender-btn.active { border-color: var(--primary); color: var(--primary); box-shadow: 0 0 20px var(--primary-glow); background: rgba(0, 234, 255, 0.1); }

.input-field { width: 100%; padding: 16px; border: 1px solid var(--border-color); border-radius: 12px; background: rgba(2, 10, 20, 0.9); color: #fff; font-size: 15px; text-align: center; outline: none; margin-bottom: 20px; }
.input-field:focus { border-color: var(--primary); box-shadow: 0 0 20px var(--primary-glow); }

.btn-primary { width: 100%; padding: 16px; border: none; border-radius: 12px; background: var(--primary); color: #000; font-weight: 900; font-size: 14px; letter-spacing: 3px; cursor: pointer; box-shadow: 0 0 25px var(--primary-glow); }
.btn-primary:hover { transform: translateY(-2px); filter: brightness(1.2); }

/* MAIN HUD LAYOUT */
header { height: 75px; padding: 0 4%; display: flex; align-items: center; justify-content: space-between; border-bottom: 1px solid var(--border-color); background: rgba(2, 8, 16, 0.85); backdrop-filter: blur(15px); }
.brand { display: flex; align-items: center; gap: 15px; }
.brand-logo { width: 42px; height: 42px; border: 2px solid var(--primary); border-radius: 50%; display: flex; align-items: center; justify-content: center; color: var(--primary); font-weight: bold; font-size: 18px; box-shadow: 0 0 15px var(--primary-glow); }
.brand-text h2 { margin: 0; font-size: 18px; letter-spacing: 4px; color: var(--primary); }
.brand-text span { font-size: 9px; color: #6a8d9a; letter-spacing: 2px; }

.status-badge { display: flex; align-items: center; gap: 10px; padding: 8px 16px; border: 1px solid var(--border-color); border-radius: 30px; background: rgba(0,0,0,0.4); font-size: 11px; letter-spacing: 2px; }
.status-dot { width: 10px; height: 10px; border-radius: 50%; background: #00ff9d; box-shadow: 0 0 12px #00ff9d; animation: pulseDot 1.5s infinite; }
@keyframes pulseDot { 0%, 100% { opacity: 1; } 50% { opacity: 0.3; } }

main { max-width: 1400px; margin: 25px auto; padding: 0 20px; display: grid; grid-template-columns: 380px 1fr; gap: 25px; }

/* LEFT PANEL - ARC REACTOR & CAMERA */
.left-panel { display: flex; flex-direction: column; gap: 20px; }
.panel-card { border: 1px solid var(--border-color); border-radius: 20px; background: var(--panel-bg); backdrop-filter: blur(15px); padding: 25px; position: relative; overflow: hidden; box-shadow: 0 8px 32px rgba(0,0,0,0.5); }

/* ARC REACTOR CORE */
.core-container { display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 20px 0; }
.arc-reactor { width: 180px; height: 180px; border-radius: 50%; border: 2px solid var(--primary); position: relative; display: flex; align-items: center; justify-content: center; box-shadow: 0 0 40px var(--primary-glow), inset 0 0 30px var(--primary-glow); animation: reactorGlow 4s ease-in-out infinite alternate; }
@keyframes reactorGlow { from { box-shadow: 0 0 25px var(--primary-glow), inset 0 0 15px var(--primary-glow); } to { box-shadow: 0 0 50px var(--primary-glow), inset 0 0 35px var(--primary-glow); } }

.ring-1 { position: absolute; inset: -15px; border: 2px dashed var(--primary); border-radius: 50%; animation: rotateClockwise 12s linear infinite; opacity: 0.7; }
.ring-2 { position: absolute; inset: -28px; border: 1px solid var(--primary); border-top-color: transparent; border-bottom-color: transparent; border-radius: 50%; animation: rotateCounter 8s linear infinite; opacity: 0.5; }
@keyframes rotateClockwise { to { transform: rotate(360deg); } }
@keyframes rotateCounter { to { transform: rotate(-360deg); } }

.core-center { width: 90px; height: 90px; border-radius: 50%; background: radial-gradient(circle, #fff 0%, var(--primary) 60%, transparent 100%); display: flex; align-items: center; justify-content: center; color: #000; font-weight: 900; font-size: 28px; box-shadow: 0 0 30px #fff; }

.core-info { margin-top: 25px; text-align: center; }
.core-info h3 { margin: 0; font-size: 14px; letter-spacing: 3px; color: var(--primary); }
.core-info p { margin: 5px 0 0; font-size: 11px; color: #6a8d9a; letter-spacing: 1px; }

/* AUDIO SPECTRUM CANVAS */
#spectrumCanvas { width: 100%; height: 50px; margin-top: 15px; border-radius: 8px; }

/* SCI-FI HUD CAMERA */
.camera-card { padding: 15px; }
.camera-frame { position: relative; width: 100%; aspect-ratio: 16/10; border-radius: 12px; overflow: hidden; background: #000; border: 1px solid var(--border-color); }
#cameraVideo { width: 100%; height: 100%; object-fit: cover; transform: scaleX(-1); display: block; }
#hudCanvas { position: absolute; inset: 0; width: 100%; height: 100%; pointer-events: none; }

/* CONTROLS */
.controls-group { display: flex; flex-direction: column; gap: 10px; margin-top: 15px; }
.hud-btn { padding: 12px 18px; border: 1px solid var(--border-color); border-radius: 10px; background: rgba(0,0,0,0.5); color: var(--text-color); font-size: 11px; letter-spacing: 2px; font-weight: bold; cursor: pointer; display: flex; align-items: center; justify-content: center; gap: 10px; }
.hud-btn:hover { border-color: var(--primary); color: var(--primary); box-shadow: 0 0 15px var(--primary-glow); }
.hud-btn.active { background: var(--primary); color: #000; border-color: var(--primary); box-shadow: 0 0 20px var(--primary-glow); }

/* RIGHT PANEL - CHAT TERMINAL */
.chat-panel { height: calc(100vh - 150px); display: flex; flex-direction: column; padding: 0; overflow: hidden; }
.chat-header { padding: 20px 25px; border-bottom: 1px solid var(--border-color); display: flex; align-items: center; justify-content: space-between; background: rgba(0,0,0,0.2); }
.chat-header h3 { margin: 0; font-size: 14px; letter-spacing: 3px; color: var(--primary); }

.chat-logs { flex: 1; padding: 25px; overflow-y: auto; display: flex; flex-direction: column; gap: 20px; scroll-behavior: smooth; }
.chat-msg { max-width: 80%; display: flex; flex-direction: column; gap: 6px; animation: msgFadeIn 0.3s ease; }
@keyframes msgFadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }

.chat-msg.user { align-self: flex-end; }
.chat-msg.ai { align-self: flex-start; }

.msg-sender { font-size: 10px; letter-spacing: 2px; color: var(--primary); font-weight: bold; }
.msg-bubble { padding: 16px 20px; border-radius: 16px; font-size: 14px; line-height: 1.6; border: 1px solid var(--border-color); background: rgba(4, 18, 33, 0.8); backdrop-filter: blur(10px); white-space: pre-wrap; }
.user .msg-bubble { background: rgba(0, 234, 255, 0.12); border-color: var(--primary); border-bottom-right-radius: 2px; }
.ai .msg-bubble { border-bottom-left-radius: 2px; box-shadow: 0 4px 20px rgba(0,0,0,0.3); }

/* INPUT BAR */
.chat-input-bar { padding: 20px; border-top: 1px solid var(--border-color); display: flex; gap: 12px; background: rgba(2, 8, 16, 0.9); }
.chat-input-bar input { flex: 1; padding: 16px 20px; border: 1px solid var(--border-color); border-radius: 12px; background: rgba(0,0,0,0.6); color: #fff; font-size: 14px; outline: none; }
.chat-input-bar input:focus { border-color: var(--primary); box-shadow: 0 0 15px var(--primary-glow); }

/* VAD VOICE INDICATOR */
.vad-status { display: flex; align-items: center; gap: 8px; font-size: 11px; letter-spacing: 1px; color: #6a8d9a; margin-top: 8px; justify-content: center; }
.vad-wave { display: inline-flex; gap: 3px; align-items: center; height: 12px; }
.vad-wave span { width: 3px; height: 100%; background: var(--primary); border-radius: 3px; animation: vadPulse 1s infinite ease-in-out; }
.vad-wave span:nth-child(2) { animation-delay: 0.2s; }
.vad-wave span:nth-child(3) { animation-delay: 0.4s; }
@keyframes vadPulse { 0%, 100% { transform: scaleY(0.3); } 50% { transform: scaleY(1); } }

@media (max-width: 950px) {
    main { grid-template-columns: 1fr; }
    .chat-panel { height: 600px; }
}
</style>
</head>
<body data-theme="male">

<div class="bg-grid"><div class="grid-lines"></div></div>
<div class="scanline"></div>

<!-- LOGIN / PERSONA SELECTOR OVERLAY -->
<div id="loginOverlay">
    <div class="loginCard">
        <h1 id="aiTitleHeader">STARK AI SYSTEM</h1>
        <p>IDENTIFICATION REQUIRED TO ACCESS SYSTEM</p>
        
        <div class="gender-select">
            <button class="gender-btn active" id="btnJarvis" onclick="selectPersona('male')">J.A.R.V.I.S<br><small style="font-size: 8px;">(MALE PERSONA)</small></button>
            <button class="gender-btn" id="btnFriday" onclick="selectPersona('female')">F.R.I.D.A.Y<br><small style="font-size: 8px;">(FEMALE PERSONA)</small></button>
        </div>

        <input type="text" id="userNameInput" class="input-field" placeholder="Enter Operator Name..." autocomplete="off">
        <button class="btn-primary" onclick="initializeSystem()">INITIALIZE SYSTEM</button>
    </div>
</div>

<header>
    <div class="brand">
        <div class="brand-logo" id="brandLogo">J</div>
        <div class="brand-text">
            <h2 id="aiBrandName">J.A.R.V.I.S 3.0</h2>
            <span>STARK INDUSTRIES AI SYSTEM</span>
        </div>
    </div>
    <div class="status-badge">
        <div class="status-dot"></div>
        <span id="systemStatus">SYSTEM ONLINE</span>
    </div>
</header>

<main>
    <!-- LEFT PANEL: ARC REACTOR & FACE TRACKING -->
    <div class="left-panel">
        <div class="panel-card core-container">
            <div class="arc-reactor">
                <div class="ring-1"></div>
                <div class="ring-2"></div>
                <div class="core-center" id="coreBadge">J</div>
            </div>
            <div class="core-info">
                <h3 id="corePersonaName">J.A.R.V.I.S CORE</h3>
                <p id="operatorGreeting">Operator: Unidentified</p>
            </div>
            <canvas id="spectrumCanvas"></canvas>
            
            <div class="vad-status">
                <div class="vad-wave" id="vadWave" style="display:none;">
                    <span></span><span></span><span></span>
                </div>
                <span id="vadStatusText">MIC: HANDS-FREE ACTIVE</span>
            </div>
        </div>

        <div class="panel-card camera-card">
            <div class="camera-frame">
                <video id="cameraVideo" autoplay playsinline muted></video>
                <canvas id="hudCanvas"></canvas>
            </div>
            <div class="controls-group">
                <button class="hud-btn" id="btnCameraToggle" onclick="toggleCamera()">📷 TOGGLE HUD FACE TRACKER</button>
                <button class="hud-btn" id="btnMicToggle" onclick="toggleHandsFreeMic()">🎙️ HANDS-FREE MIC: ON</button>
            </div>
        </div>
    </div>

    <!-- RIGHT PANEL: CHAT INTERFACE -->
    <div class="panel-card chat-panel">
        <div class="chat-header">
            <h3 id="chatTerminalTitle">TERMINAL LOGS // J.A.R.V.I.S</h3>
            <button class="hud-btn" style="padding: 6px 12px;" onclick="clearLogs()">CLEAR</button>
        </div>
        
        <div class="chat-logs" id="chatLogs">
            <div class="chat-msg ai">
                <span class="msg-sender" id="initialSender">SYSTEM</span>
                <div class="msg-bubble">Awaiting user identity verification...</div>
            </div>
        </div>

        <div class="chat-input-bar">
            <input type="text" id="userInput" placeholder="Speak hands-free or type command..." onkeydown="if(event.key==='Enter') sendTextMessage()">
            <button class="hud-btn active" onclick="sendTextMessage()">TRANSMIT</button>
        </div>
    </div>
</main>

<script>
/* ============================================================
   SYNTHESIZED SCI-FI SOUND EFFECTS (WEB AUDIO API)
============================================================ */
const AudioFX = {
    ctx: null,
    init() { if (!this.ctx) this.ctx = new (window.AudioContext || window.webkitAudioContext)(); },
    
    playChime(type = 'response') {
        try {
            this.init();
            const now = this.ctx.currentTime;
            const osc = this.ctx.createOscillator();
            const gain = this.ctx.createGain();
            osc.connect(gain);
            gain.connect(this.ctx.destination);

            if (type === 'response') {
                osc.type = 'sine';
                osc.frequency.setValueAtTime(520, now);
                osc.frequency.exponentialRampToValueAtTime(1040, now + 0.12);
                gain.gain.setValueAtTime(0.15, now);
                gain.gain.exponentialRampToValueAtTime(0.01, now + 0.12);
                osc.start(now); osc.stop(now + 0.12);
            } else if (type === 'listen') {
                osc.type = 'triangle';
                osc.frequency.setValueAtTime(880, now);
                osc.frequency.exponentialRampToValueAtTime(440, now + 0.15);
                gain.gain.setValueAtTime(0.1, now);
                gain.gain.exponentialRampToValueAtTime(0.01, now + 0.15);
                osc.start(now); osc.stop(now + 0.15);
            } else if (type === 'error') {
                osc.type = 'sawtooth';
                osc.frequency.setValueAtTime(180, now);
                gain.gain.setValueAtTime(0.2, now);
                gain.gain.exponentialRampToValueAtTime(0.01, now + 0.25);
                osc.start(now); osc.stop(now + 0.25);
            }
        } catch (e) { console.error("AudioFX error", e); }
    }
};

/* ============================================================
   GLOBAL STATE & PERSONAS
============================================================ */
let persona = 'male'; // 'male' (JARVIS) or 'female' (FRIDAY)
let userName = '';
let isHandsFreeActive = true;
let isSpeaking = false;
let recognition = null;

function selectPersona(selected) {
    persona = selected;
    document.body.setAttribute('data-theme', selected);
    document.getElementById('btnJarvis').classList.toggle('active', selected === 'male');
    document.getElementById('btnFriday').classList.toggle('active', selected === 'female');
    document.getElementById('aiTitleHeader').textContent = selected === 'male' ? 'STARK AI // J.A.R.V.I.S' : 'STARK AI // F.R.I.D.A.Y';
    AudioFX.playChime('response');
}

function initializeSystem() {
    const nameInput = document.getElementById('userNameInput').value.trim();
    if (!nameInput) { alert("Please enter your name, Operator."); return; }
    
    userName = nameInput;
    document.getElementById('loginOverlay').style.display = 'none';
    
    // Update Persona UI
    const isMale = persona === 'male';
    const aiName = isMale ? 'J.A.R.V.I.S' : 'F.R.I.D.A.Y';
    
    document.getElementById('brandLogo').textContent = isMale ? 'J' : 'F';
    document.getElementById('coreBadge').textContent = isMale ? 'J' : 'F';
    document.getElementById('aiBrandName').textContent = aiName + ' 3.0';
    document.getElementById('corePersonaName').textContent = aiName + ' CORE';
    document.getElementById('operatorGreeting').textContent = 'Operator: ' + userName;
    document.getElementById('chatTerminalTitle').textContent = 'TERMINAL LOGS // ' + aiName;
    
    addLogMessage(aiName, `Welcome online, ${userName}. All primary subroutines are nominal. How can I assist you today?`, 'ai');
    speakText(`Welcome online, ${userName}. How can I assist you today?`);
    
    initHandsFreeSpeech();
    initAudioSpectrum();
}

/* ============================================================
   TEXT TO SPEECH (MALE vs FEMALE VOICE SELECTION)
============================================================ */
let availableVoices = [];
function updateVoices() {
    if ('speechSynthesis' in window) availableVoices = speechSynthesis.getVoices();
}
if ('speechSynthesis' in window) {
    updateVoices();
    speechSynthesis.onvoiceschanged = updateVoices;
}

function speakText(text) {
    if (!('speechSynthesis' in window)) return;
    speechSynthesis.cancel();

    // Clean Markdown
    const cleanText = text.replace(/[\*\_]/g, '');
    const utterance = new SpeechSynthesisUtterance(cleanText);
    
    // Find ideal voice based on gender
    let chosenVoice = null;
    const isMale = persona === 'male';
    
    if (isMale) {
        utterance.pitch = 0.85; // Lower pitch for male/JARVIS
        utterance.rate = 0.98;
        chosenVoice = availableVoices.find(v => v.name.includes("David") || v.name.includes("Male") || v.name.includes("George") || v.name.includes("UK English Male"));
    } else {
        utterance.pitch = 1.15; // Higher pitch for female/FRIDAY
        utterance.rate = 1.0;
        chosenVoice = availableVoices.find(v => v.name.includes("Zira") || v.name.includes("Female") || v.name.includes("Hazel") || v.name.includes("Google US English"));
    }

    if (chosenVoice) utterance.voice = chosenVoice;

    utterance.onstart = () => {
        isSpeaking = true;
        document.getElementById('systemStatus').textContent = 'AI TRANSMITTING...';
        if (recognition) try { recognition.stop(); } catch(e){}
    };

    utterance.onend = () => {
        isSpeaking = false;
        document.getElementById('systemStatus').textContent = 'SYSTEM ONLINE';
        if (isHandsFreeActive) startListeningLoop();
    };

    speechSynthesis.speak(utterance);
}

/* ============================================================
   CONTINUOUS HANDS-FREE SPEECH RECOGNITION (VAD)
============================================================ */
function initHandsFreeSpeech() {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) {
        console.warn("Web Speech API not supported in this browser. Falling back to manual text input.");
        document.getElementById('vadStatusText').textContent = "VOICE RECOGNITION UNSUPPORTED";
        return;
    }

    recognition = new SpeechRecognition();
    recognition.continuous = true;
    recognition.interimResults = true;
    recognition.lang = 'en-US';

    let finalTranscript = '';

    recognition.onstart = () => {
        document.getElementById('vadWave').style.display = 'inline-flex';
        document.getElementById('vadStatusText').textContent = "MIC: LISTENING...";
    };

    recognition.onresult = (event) => {
        if (isSpeaking) return; // Ignore input while AI is speaking

        let interimTranscript = '';
        for (let i = event.resultIndex; i < event.results.length; ++i) {
            if (event.results[i].isFinal) {
                finalTranscript += event.results[i][0].transcript;
            } else {
                interimTranscript += event.results[i][0].transcript;
            }
        }

        if (finalTranscript.trim().length > 0) {
            const query = finalTranscript.trim();
            finalTranscript = '';
            AudioFX.playChime('listen');
            processUserQuery(query);
        }
    };

    recognition.onerror = (e) => {
        console.log("Speech Rec error:", e.error);
        if (e.error !== 'no-speech' && e.error !== 'aborted') {
            document.getElementById('vadStatusText').textContent = "MIC RECONNECTING...";
        }
    };

    recognition.onend = () => {
        document.getElementById('vadWave').style.display = 'none';
        if (isHandsFreeActive && !isSpeaking) {
            setTimeout(startListeningLoop, 300);
        } else {
            document.getElementById('vadStatusText').textContent = "MIC: PAUSED";
        }
    };

    startListeningLoop();
}

function startListeningLoop() {
    if (recognition && isHandsFreeActive && !isSpeaking) {
        try { recognition.start(); } catch(e) {}
    }
}

function toggleHandsFreeMic() {
    isHandsFreeActive = !isHandsFreeActive;
    const btn = document.getElementById('btnMicToggle');
    if (isHandsFreeActive) {
        btn.textContent = "🎙️ HANDS-FREE MIC: ON";
        btn.classList.add('active');
        startListeningLoop();
    } else {
        btn.textContent = "🎙️ HANDS-FREE MIC: OFF";
        btn.classList.remove('active');
        if (recognition) try { recognition.stop(); } catch(e){}
    }
}

/* ============================================================
   COMMUNICATION BACKEND (CHAT ROUTE)
============================================================ */
async function processUserQuery(text) {
    if (!text) return;
    
    addLogMessage(userName.toUpperCase(), text, 'user');
    document.getElementById('systemStatus').textContent = 'PROCESSING QUERY...';

    try {
        const response = await fetch('/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: text, name: userName, persona: persona })
        });

        const data = await response.json();
        if (!response.ok) throw new Error(data.error || "Backend query failure");

        const aiName = persona === 'male' ? 'J.A.R.V.I.S' : 'F.R.I.D.A.Y';
        addLogMessage(aiName, data.answer, 'ai');
        AudioFX.playChime('response');
        speakText(data.answer);

    } catch (err) {
        AudioFX.playChime('error');
        addLogMessage('SYSTEM ERROR', "Failed to connect to AI server: " + err.message, 'ai');
        document.getElementById('systemStatus').textContent = 'SYSTEM ERROR';
    }
}

function sendTextMessage() {
    const input = document.getElementById('userInput');
    const text = input.value.trim();
    if (text) {
        input.value = '';
        processUserQuery(text);
    }
}

function addLogMessage(sender, text, type) {
    const chatLogs = document.getElementById('chatLogs');
    const msgDiv = document.createElement('div');
    msgDiv.className = `chat-msg ${type}`;
    msgDiv.innerHTML = `<span class="msg-sender">${sender}</span><div class="msg-bubble">${text}</div>`;
    chatLogs.appendChild(msgDiv);
    chatLogs.scrollTop = chatLogs.scrollHeight;
}

function clearLogs() {
    document.getElementById('chatLogs').innerHTML = '';
}

/* ============================================================
   AUDIO SPECTRUM VISUALIZER
============================================================ */
function initAudioSpectrum() {
    const canvas = document.getElementById('spectrumCanvas');
    const ctx = canvas.getContext('2d');
    canvas.width = canvas.offsetWidth;
    canvas.height = canvas.offsetHeight;

    let step = 0;
    function renderSpectrum() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        const bars = 24;
        const barWidth = canvas.width / bars - 4;
        const color = persona === 'male' ? '#00eaff' : '#ff007f';

        for (let i = 0; i < bars; i++) {
            let height = 4;
            if (isSpeaking) {
                height = Math.sin(step + i * 0.5) * 18 + 22;
            } else if (isHandsFreeActive) {
                height = Math.cos(step + i * 0.3) * 6 + 10;
            }
            
            ctx.fillStyle = color;
            ctx.shadowBlur = 10;
            ctx.shadowColor = color;
            ctx.fillRect(i * (barWidth + 4), canvas.height - height, barWidth, height);
        }
        step += 0.15;
        requestAnimationFrame(renderSpectrum);
    }
    renderSpectrum();
}

/* ============================================================
   SCI-FI HUD CAMERA & FACE TRACKER OVERLAY
============================================================ */
let cameraStream = null;
let hudAnimFrame = null;

async function toggleCamera() {
    const video = document.getElementById('cameraVideo');
    const btn = document.getElementById('btnCameraToggle');

    if (cameraStream) {
        cameraStream.getTracks().forEach(t => t.stop());
        cameraStream = null;
        video.srcObject = null;
        cancelAnimationFrame(hudAnimFrame);
        btn.classList.remove('active');
        return;
    }

    try {
        cameraStream = await navigator.mediaDevices.getUserMedia({ video: { width: 640, height: 480 } });
        video.srcObject = cameraStream;
        btn.classList.add('active');
        startHudOverlay();
    } catch (e) {
        alert("Camera Access Denied or Unavailable: " + e.message);
    }
}

function startHudOverlay() {
    const canvas = document.getElementById('hudCanvas');
    const ctx = canvas.getContext('2d');
    let angle = 0;

    function drawHUD() {
        canvas.width = canvas.offsetWidth;
        canvas.height = canvas.offsetHeight;
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        const cx = canvas.width / 2;
        const cy = canvas.height / 2;
        const color = persona === 'male' ? '#00eaff' : '#ff007f';

        // Target Lock Reticle
        ctx.strokeStyle = color;
        ctx.lineWidth = 2;
        ctx.shadowColor = color;
        ctx.shadowBlur = 12;

        // Dynamic Rotational HUD Ring
        ctx.save();
        ctx.translate(cx, cy);
        ctx.rotate(angle);
        ctx.beginPath();
        ctx.arc(0, 0, 55, 0, Math.PI * 1.5);
        ctx.stroke();
        ctx.restore();

        // Corner Target Brackets (Simulated Face Tracking Box)
        const boxSize = 120 + Math.sin(angle * 2) * 10;
        const left = cx - boxSize / 2;
        const top = cy - boxSize / 2;
        const bracket = 20;

        ctx.beginPath();
        // Top Left
        ctx.moveTo(left, top + bracket); ctx.lineTo(left, top); ctx.lineTo(left + bracket, top);
        // Top Right
        ctx.moveTo(left + boxSize - bracket, top); ctx.lineTo(left + boxSize, top); ctx.lineTo(left + boxSize, top + bracket);
        // Bottom Right
        ctx.moveTo(left + boxSize, top + boxSize - bracket); ctx.lineTo(left + boxSize, top + boxSize); ctx.lineTo(left + boxSize - bracket, top + boxSize);
        // Bottom Left
        ctx.moveTo(left + bracket, top + boxSize); ctx.lineTo(left, top + boxSize); ctx.lineTo(left, top + boxSize - bracket);
        ctx.stroke();

        // HUD Telemetry Text
        ctx.fillStyle = color;
        ctx.font = '10px monospace';
        ctx.fillText(`TARGET: SUBJECT_01`, left, top - 12);
        ctx.fillText(`LOC: [${Math.round(cx)}, ${Math.round(cy)}]`, left, top + boxSize + 18);
        ctx.fillText(`STATUS: LOCKED`, left + boxSize - 70, top + boxSize + 18);

        angle += 0.03;
        hudAnimFrame = requestAnimationFrame(drawHUD);
    }
    drawHUD();
}
</script>
</body>
</html>
"""

# ============================================================
# FLASK BACKEND ROUTES
# ============================================================

@app.route("/")
def index():
    return Response(HTML_TEMPLATE, mimetype="text/html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json or {}
    user_msg = data.get("message", "")
    user_name = data.get("name", "Operator")
    persona = data.get("persona", "male")

    if not GROQ_API_KEY:
        return jsonify({"answer": f"System Alert: GROQ_API_KEY is not set on the server. Please configure your API key."}), 200

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    if persona == "female":
        system_prompt = (
            f"You are F.R.I.D.A.Y, an advanced female tactical AI assistant created by {CREATOR}. "
            f"You are addressing user '{user_name}'. Be brilliant, highly efficient, supportive, and direct. "
            "Address the user by name frequently."
        )
    else:
        system_prompt = (
            f"You are J.A.R.V.I.S, an extraordinarily intelligent, polite male AI assistant created by {CREATOR}. "
            f"You are addressing user '{user_name}'. Provide sharp, articulate, witty, and concise responses. "
            "Address the user by name frequently."
        )

    payload = {
        "model": CHAT_MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_msg}
        ],
        "temperature": 0.7,
        "max_tokens": 1024
    }

    try:
        resp = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=payload, timeout=15)
        resp.raise_for_status()
        answer = resp.json()["choices"][0]["message"]["content"]
        return jsonify({"answer": answer})
    except Exception as e:
        return jsonify({"error": f"Groq LLM Error: {str(e)}"}), 500

@app.route("/transcribe", methods=["POST"])
def transcribe():
    """Fixed robust Whisper endpoint supporting multipart file uploads."""
    if 'audio' not in request.files:
        return jsonify({"error": "No audio file provided."}), 400

    audio_file = request.files['audio']
    audio_bytes = audio_file.read()

    if not GROQ_API_KEY:
        return jsonify({"error": "GROQ_API_KEY is missing."}), 500

    headers = { "Authorization": f"Bearer {GROQ_API_KEY}" }

    # Fixed multipart tuple structure to avoid Bad Request 400 errors
    files = {
        'file': ('speech.webm', audio_bytes, 'audio/webm'),
        'model': (None, WHISPER_MODEL)
    }

    try:
        resp = requests.post("https://api.groq.com/openai/v1/audio/transcriptions", headers=headers, files=files, timeout=20)
        if not resp.ok:
            return jsonify({"error": f"Groq Whisper Error ({resp.status_code}): {resp.text}"}), resp.status_code
        
        return jsonify({"text": resp.json().get("text", "")})
    except Exception as e:
        return jsonify({"error": f"Transcription Exception: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
