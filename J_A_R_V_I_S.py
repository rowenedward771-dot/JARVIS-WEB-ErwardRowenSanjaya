import os
import requests
from flask import Flask, request, jsonify, Response

app = Flask(__name__)

# ============================================================
# CONFIGURATION
# ============================================================

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

CHAT_MODEL = "llama-3.3-70b-versatile"
WHISPER_MODEL = "whisper-large-v3-turbo"

CREATOR = "Erward Rowen Sanjaya"

# ============================================================
# HTML & JAVASCRIPT LENGKAP
# ============================================================

HTML = r"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<meta name="theme-color" content="#02060d">
<title>J.A.R.V.I.S 2.0</title>
<style>
* { box-sizing: border-box; }
html, body { margin: 0; min-height: 100%; background: #02060d; color: #e8faff; font-family: Arial, Helvetica, sans-serif; }
body { overflow-x: hidden; }

/* BACKGROUND */
.background { position: fixed; inset: 0; z-index: -10; overflow: hidden; background: radial-gradient(circle at 50% 40%, #07384f 0%, #020b13 38%, #01040a 78%); }
.grid { position: absolute; width: 200%; height: 200%; left: -50%; top: -20%; background-image: linear-gradient(rgba(0,234,255,.07) 1px, transparent 1px), linear-gradient(90deg, rgba(0,234,255,.07) 1px, transparent 1px); background-size: 50px 50px; transform: perspective(500px) rotateX(60deg); animation: gridMove 12s linear infinite; }
@keyframes gridMove { from { transform: perspective(500px) rotateX(60deg) translateY(0); } to { transform: perspective(500px) rotateX(60deg) translateY(50px); } }
.scanline { position: absolute; width: 100%; height: 2px; background: linear-gradient(90deg, transparent, #00eaff, transparent); box-shadow: 0 0 20px #00eaff; opacity: .35; animation: scan 6s linear infinite; }
@keyframes scan { 0% { top: -5%; } 100% { top: 105%; } }

/* LOGIN */
#loginScreen { position: fixed; inset: 0; z-index: 1000; display: flex; align-items: center; justify-content: center; padding: 25px; background: radial-gradient(circle at center, #07384f, #02060d 65%); }
.loginBox { width: min(440px, 100%); padding: 40px 30px; border: 1px solid rgba(0,234,255,.35); border-radius: 24px; background: rgba(3,13,23,.88); backdrop-filter: blur(20px); box-shadow: 0 0 60px rgba(0,234,255,.12); text-align: center; }
.loginLogo { width: 100px; height: 100px; margin: 0 auto 25px; border: 2px solid #00eaff; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 50px; font-weight: bold; color: #00eaff; box-shadow: 0 0 35px #00eaff, inset 0 0 30px rgba(0,234,255,.25); animation: corePulse 2s infinite; }
.loginBox h1 { margin: 0; letter-spacing: 5px; }
.loginBox p { color: #7098a3; font-size: 13px; line-height: 1.6; }
.nameInput { width: 100%; padding: 15px; margin-top: 15px; border: 1px solid #17434f; border-radius: 10px; background: #020b13; color: white; outline: none; font-size: 16px; text-align: center; }
.nameInput:focus { border-color: #00eaff; box-shadow: 0 0 20px rgba(0,234,255,.15); }
.startButton { width: 100%; margin-top: 15px; padding: 15px; border: 0; border-radius: 10px; background: #00eaff; color: #001018; font-weight: bold; cursor: pointer; font-size: 15px; }
.startButton:active { transform: scale(.98); }

/* HEADER */
header { min-height: 78px; padding: env(safe-area-inset-top) 5% 0 5%; display: flex; align-items: center; justify-content: space-between; border-bottom: 1px solid rgba(0,234,255,.2); background: rgba(2,8,15,.75); backdrop-filter: blur(18px); }
.brand { display: flex; align-items: center; gap: 13px; }
.logo { width: 45px; height: 45px; border: 2px solid #00eaff; border-radius: 50%; display: flex; align-items: center; justify-content: center; color: #00eaff; font-weight: bold; box-shadow: 0 0 20px #00eaff; }
.brand h1 { margin: 0; letter-spacing: 4px; font-size: 21px; }
.brand small { color: #638c96; letter-spacing: 2px; font-size: 9px; }
.status { display: flex; align-items: center; gap: 8px; color: #8cb6c0; font-size: 10px; letter-spacing: 2px; }
.statusDot { width: 8px; height: 8px; border-radius: 50%; background: #00ff9d; box-shadow: 0 0 15px #00ff9d; }

/* MAIN & CORE */
main { width: min(1300px, 94%); margin: 25px auto; display: grid; grid-template-columns: 360px 1fr; gap: 22px; }
.corePanel { min-height: 680px; border: 1px solid rgba(0,234,255,.25); border-radius: 22px; background: rgba(3,13,23,.72); display: flex; flex-direction: column; align-items: center; justify-content: center; position: relative; overflow: hidden; }
.core { width: 190px; height: 190px; border: 2px solid #00eaff; border-radius: 50%; display: flex; align-items: center; justify-content: center; position: relative; box-shadow: 0 0 35px #00eaff, inset 0 0 45px rgba(0,234,255,.25); animation: corePulse 3s infinite; }
@keyframes corePulse { 0%,100% { transform: scale(1); } 50% { transform: scale(1.05); } }
.core::before { content: ""; position: absolute; inset: -25px; border: 1px solid #00eaff; border-left-color: transparent; border-right-color: transparent; border-radius: 50%; animation: spin 5s linear infinite; }
.core::after { content: ""; position: absolute; inset: -45px; border: 1px solid #00eaff; border-top-color: transparent; border-bottom-color: transparent; border-radius: 50%; animation: spinReverse 8s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }
@keyframes spinReverse { to { transform: rotate(-360deg); } }
.coreInner { width: 115px; height: 115px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 50px; font-weight: bold; background: radial-gradient(circle, #27efff, #006d8b 45%, #02131d 75%); box-shadow: 0 0 45px #00eaff; }
.coreStatus { margin-top: 65px; color: #00eaff; letter-spacing: 3px; font-size: 11px; }
.userWelcome { margin-top: 12px; color: #7597a0; font-size: 12px; }

/* VOICE BUTTONS */
.voiceButtons { display: flex; gap: 10px; margin-top: 25px; }
.talkButton, .stopButton { padding: 13px 17px; border-radius: 25px; cursor: pointer; font-weight: bold; font-size: 12px; user-select: none; }
.talkButton { border: 1px solid #00eaff; color: #00eaff; background: #03131c; }
.stopButton { border: 1px solid #ff3154; color: #ff3154; background: #17040a; }
.talkButton.listening { background: #ff1744; color: white; border-color: #ff1744; box-shadow: 0 0 30px #ff1744; }

/* CAMERA */
.cameraBox { margin-top: 25px; width: 250px; border: 1px solid rgba(0,234,255,.25); border-radius: 14px; padding: 10px; background: rgba(0,0,0,.3); }
.cameraFrame { position: relative; overflow: hidden; border-radius: 10px; background: #000; aspect-ratio: 16 / 10; }
#camera { width: 100%; height: 100%; object-fit: cover; transform: scaleX(-1); display: none; }
.faceBox { position: absolute; width: 90px; height: 90px; border: 2px solid #00ff9d; border-radius: 50%; display: none; transform: translate(-50%,-50%); box-shadow: 0 0 20px #00ff9d; transition: all 0.1s ease; }
.cameraStatus { margin-top: 8px; text-align: center; color: #638c96; font-size: 9px; letter-spacing: 2px; }
.cameraButton { width: 100%; margin-top: 8px; padding: 9px; border: 1px solid #24515d; border-radius: 8px; background: transparent; color: #8cb6c0; cursor: pointer; }

/* CHAT */
.chat { min-height: 680px; border: 1px solid rgba(0,234,255,.25); border-radius: 22px; background: rgba(3,13,23,.72); display: flex; flex-direction: column; overflow: hidden; }
.chatHeader { padding: 20px; border-bottom: 1px solid rgba(0,234,255,.18); display: flex; justify-content: space-between; }
.chatHeader h2 { margin: 0; font-size: 15px; letter-spacing: 3px; }
.chatHeader span { display: block; margin-top: 5px; color: #638c96; font-size: 9px; letter-spacing: 2px; }
.clearButton { border: 1px solid #24515d; background: transparent; color: #8cb6c0; border-radius: 6px; padding: 7px 12px; cursor: pointer; }
.messages { flex: 1; overflow-y: auto; padding: 22px; }
.message { margin-bottom: 18px; max-width: 85%; animation: messageIn .25s ease; }
@keyframes messageIn { from { opacity: 0; transform: translateY(8px); } to { opacity: 1; transform: translateY(0); } }
.message.user { margin-left: auto; text-align: right; }
.sender { margin-bottom: 5px; color: #00eaff; font-size: 9px; letter-spacing: 2px; }
.text { padding: 13px 15px; border: 1px solid rgba(0,234,255,.12); border-radius: 12px; background: #061522; line-height: 1.55; font-size: 14px; white-space: pre-wrap; }
.user .text { background: #073343; }
.system .text { color: #71919a; }

/* INPUT */
.inputArea { padding: 15px; display: flex; gap: 8px; border-top: 1px solid rgba(0,234,255,.18); }
.inputArea input { flex: 1; min-width: 0; background: #020b13; border: 1px solid #17434f; border-radius: 10px; color: white; padding: 13px; outline: none; }
.inputArea input:focus { border-color: #00eaff; }
.sendButton { border: 0; border-radius: 10px; background: #00eaff; color: #001018; padding: 0 20px; font-weight: bold; cursor: pointer; }
footer { text-align: center; padding: 20px; color: #55747d; font-size: 9px; letter-spacing: 2px; }

@media(max-width: 850px) {
    header { padding-left: 18px; padding-right: 18px; }
    main { width: 94%; grid-template-columns: 1fr; }
    .corePanel { min-height: auto; padding: 40px 15px; }
    .core { width: 150px; height: 150px; }
    .coreInner { width: 90px; height: 90px; font-size: 38px; }
    .cameraBox { width: min(280px, 90%); }
    .chat { min-height: 600px; }
}
</style>
</head>
<body>

<div class="background"><div class="grid"></div><div class="scanline"></div></div>

<section id="loginScreen">
    <div class="loginBox">
        <div class="loginLogo">J</div>
        <h1>J.A.R.V.I.S</h1>
        <p>Personal Artificial Intelligence System<br>Please identify yourself before activation.</p>
        <input id="nameInput" class="nameInput" type="text" maxlength="30" autocomplete="name" placeholder="Enter your name...">
        <button id="startButton" class="startButton">INITIALIZE J.A.R.V.I.S</button>
    </div>
</section>

<header>
    <div class="brand">
        <div class="logo">J</div>
        <div><h1>J.A.R.V.I.S</h1><small>PERSONAL AI SYSTEM</small></div>
    </div>
    <div class="status">
        <div class="statusDot"></div><span id="status">ONLINE</span>
    </div>
</header>

<main>
<section class="corePanel">
    <div class="core"><div class="coreInner">J</div></div>
    <div id="coreStatus" class="coreStatus">AI CORE ONLINE</div>
    <div id="userWelcome" class="userWelcome">Welcome.</div>
    <div class="voiceButtons">
        <button id="talkButton" class="talkButton">🎙️ HOLD TO TALK</button>
        <button id="stopButton" class="stopButton">⏹ STOP AI</button>
    </div>
    <div class="cameraBox">
        <div class="cameraFrame">
            <video id="camera" autoplay playsinline muted></video>
            <div id="faceBox" class="faceBox"></div>
        </div>
        <div id="cameraStatus" class="cameraStatus">CAMERA OFF</div>
        <button id="cameraButton" class="cameraButton">📷 ACTIVATE CAMERA</button>
    </div>
</section>

<section class="chat">
    <div class="chatHeader">
        <div><h2>CONVERSATION</h2><span>CLOUD AI • VOICE • VISION</span></div>
        <button id="clearButton" class="clearButton">CLEAR</button>
    </div>
    <div id="messages" class="messages">
        <div class="message system">
            <div class="sender">SYSTEM</div>
            <div class="text">J.A.R.V.I.S initialized. Awaiting user identification.</div>
        </div>
    </div>
    <div class="inputArea">
        <input id="textInput" type="text" placeholder="Type a command..." autocomplete="off">
        <button id="sendButton" class="sendButton">SEND</button>
    </div>
</section>
</main>
<footer>J.A.R.V.I.S 2.0 &nbsp;|&nbsp; Created by Erward Rowen Sanjaya</footer>

<script>
const loginScreen = document.getElementById("loginScreen");
const nameInput = document.getElementById("nameInput");
const startButton = document.getElementById("startButton");
const messages = document.getElementById("messages");
const textInput = document.getElementById("textInput");
const sendButton = document.getElementById("sendButton");
const talkButton = document.getElementById("talkButton");
const stopButton = document.getElementById("stopButton");
const clearButton = document.getElementById("clearButton");
const statusEl = document.getElementById("status");
const coreStatus = document.getElementById("coreStatus");
const userWelcome = document.getElementById("userWelcome");
const camera = document.getElementById("camera");
const cameraButton = document.getElementById("cameraButton");
const cameraStatus = document.getElementById("cameraStatus");
const faceBox = document.getElementById("faceBox");

let userName = localStorage.getItem("jarvis_user_name") || "";
if (userName) {
    loginScreen.style.display = "none";
    userWelcome.textContent = "Welcome back, " + userName + ".";
}

function initializeJarvis() {
    const name = nameInput.value.trim();
    if (!name) { nameInput.focus(); return; }
    userName = name;
    localStorage.setItem("jarvis_user_name", userName);
    loginScreen.style.display = "none";
    userWelcome.textContent = "Welcome, " + userName + ".";
    addMessage("JARVIS", "Good to see you, " + userName + ". My systems are online. How may I assist you?", "jarvis");
    speak("Good to see you, " + userName + ". My systems are online.");
}
startButton.onclick = initializeJarvis;
nameInput.addEventListener("keydown", e => { if (e.key === "Enter") initializeJarvis(); });

function setStatus(value) {
    statusEl.textContent = value;
    coreStatus.textContent = "AI CORE " + value;
}

function addMessage(sender, text, type) {
    const box = document.createElement("div");
    box.className = "message " + type;
    box.innerHTML = `<div class="sender">${sender}</div><div class="text">${text}</div>`;
    messages.appendChild(box);
    messages.scrollTop = messages.scrollHeight;
}

let voices = [];
function loadVoices() { if ("speechSynthesis" in window) voices = speechSynthesis.getVoices(); }
if ("speechSynthesis" in window) { loadVoices(); speechSynthesis.onvoiceschanged = loadVoices; }

function speak(text) {
    if (!("speechSynthesis" in window)) return;
    speechSynthesis.cancel();
    
    // Cleaning text (remove asterisks from markdown)
    const cleanText = text.replace(/\*/g, '');
    const parts = cleanText.match(/[^.!?]+[.!?]+|[^.!?]+$/g) || [cleanText];
    let index = 0;

    function speakNext() {
        if (index >= parts.length) { setStatus("ONLINE"); return; }
        const utterance = new SpeechSynthesisUtterance(parts[index].trim());
        utterance.lang = "id-ID"; // Try Indonesian by default, fallback to default OS voice
        utterance.rate = 0.95;
        utterance.pitch = 0.85;
        
        const preferred = voices.find(v => v.lang.toLowerCase().includes("id") || v.name.includes("Indonesian"));
        if (preferred) utterance.voice = preferred;

        utterance.onstart = () => setStatus("SPEAKING");
        utterance.onend = () => { index++; setTimeout(speakNext, 80); };
        utterance.onerror = () => { index++; speakNext(); };
        speechSynthesis.speak(utterance);
    }
    speakNext();
}

stopButton.onclick = () => { speechSynthesis.cancel(); setStatus("ONLINE"); };
clearButton.onclick = () => { messages.innerHTML = ''; addMessage("SYSTEM", "Conversation cleared.", "system"); };

let sending = false;
async function sendMessage(suppliedText = null) {
    if (sending) return;
    const text = (suppliedText !== null ? suppliedText : textInput.value).trim();
    if (!text) return;
    if (!userName) { addMessage("SYSTEM", "Please enter your name first.", "system"); return; }

    sending = true;
    addMessage(userName.toUpperCase(), text, "user");
    textInput.value = "";
    setStatus("THINKING");

    try {
        const response = await fetch("/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message: text, name: userName })
        });
        const data = await response.json();
        if (!response.ok) throw new Error(data.error || "Server error");
        addMessage("JARVIS", data.answer, "jarvis");
        speak(data.answer);
    } catch (error) {
        addMessage("SYSTEM", "Connection error: " + error.message, "system");
        setStatus("ERROR");
        setTimeout(() => setStatus("ONLINE"), 1500);
    } finally { sending = false; }
}

sendButton.onclick = () => sendMessage();
textInput.addEventListener("keydown", e => { if (e.key === "Enter") sendMessage(); });

/* ============================================================
   MICROPHONE / AUDIO RECORDING
============================================================ */
let mediaStream = null;
let mediaRecorder = null;
let audioChunks = [];
let recordingStartedAt = 0;

function chooseMimeType() {
    if (typeof MediaRecorder === "undefined") return "";
    const types = ["audio/webm", "audio/mp4", "audio/ogg"];
    for (const type of types) {
        try { if (MediaRecorder.isTypeSupported(type)) return type; } catch (error) {}
    }
    return "";
}

async function startRecording() {
    if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
        addMessage("SYSTEM", "Microphone not supported.", "system"); return;
    }
    try {
        mediaStream = await navigator.mediaDevices.getUserMedia({ audio: { echoCancellation: true, noiseSuppression: true } });
        const mimeType = chooseMimeType();
        mediaRecorder = new MediaRecorder(mediaStream, mimeType ? { mimeType } : {});
        audioChunks = [];
        recordingStartedAt = Date.now();

        mediaRecorder.ondataavailable = e => { if (e.data && e.data.size > 0) audioChunks.push(e.data); };
        mediaRecorder.onstop = processRecording;
        mediaRecorder.start(250);

        talkButton.classList.add("listening");
        talkButton.textContent = "🔴 RECORDING...";
        setStatus("LISTENING");
    } catch (error) {
        addMessage("SYSTEM", "Microphone error: " + error.message, "system");
    }
}

function stopRecording() {
    if (mediaRecorder && mediaRecorder.state === "recording") {
        mediaRecorder.stop();
        setStatus("PROCESSING");
    }
}

function cleanupMicrophone() {
    if (mediaStream) mediaStream.getTracks().forEach(track => track.stop());
    mediaStream = null; mediaRecorder = null;
    talkButton.classList.remove("listening");
    talkButton.textContent = "🎙️ HOLD TO TALK";
}

async function processRecording() {
    const duration = Date.now() - recordingStartedAt;
    cleanupMicrophone();

    if (duration < 500) {
        addMessage("SYSTEM", "Recording too short.", "system");
        setStatus("ONLINE"); return;
    }

    const mimeType = mediaRecorder && mediaRecorder.mimeType ? mediaRecorder.mimeType : "audio/webm";
    const blob = new Blob(audioChunks, { type: mimeType });
    
    if (blob.size < 1000) {
        addMessage("SYSTEM", "Recording empty.", "system");
        setStatus("ONLINE"); return;
    }

    const formData = new FormData();
    formData.append("audio", blob, "voice.webm");
    formData.append("name", userName);

    setStatus("TRANSCRIBING");

    try {
        const response = await fetch("/transcribe", { method: "POST", body: formData });
        const data = await response.json();
        if (!response.ok) throw new Error(data.error || "Transcription failed");
        
        const transcript = (data.text || "").trim();
        if (!transcript) {
            addMessage("SYSTEM", "Could not hear anything clearly.", "system");
            setStatus("ONLINE"); return;
        }
        sendMessage(transcript);
    } catch (error) {
        addMessage("SYSTEM", "Audio Error: " + error.message, "system");
        setStatus("ONLINE");
    }
}

// Push to talk listeners
talkButton.addEventListener("mousedown", startRecording);
talkButton.addEventListener("mouseup", stopRecording);
talkButton.addEventListener("touchstart", e => { e.preventDefault(); startRecording(); });
talkButton.addEventListener("touchend", e => { e.preventDefault(); stopRecording(); });

/* ============================================================
   CAMERA & FACE DETECTION
============================================================ */
let videoStream = null;
let faceInterval = null;

async function toggleCamera() {
    if (videoStream) {
        // Matikan Kamera
        videoStream.getTracks().forEach(t => t.stop());
        videoStream = null;
        camera.style.display = "none";
        faceBox.style.display = "none";
        cameraStatus.textContent = "CAMERA OFF";
        cameraButton.textContent = "📷 ACTIVATE CAMERA";
        if (faceInterval) clearInterval(faceInterval);
        return;
    }
    
    try {
        videoStream = await navigator.mediaDevices.getUserMedia({ video: true });
        camera.srcObject = videoStream;
        camera.style.display = "block";
        cameraStatus.textContent = "CAMERA ON (SCANNING...)";
        cameraButton.textContent = "📷 DEACTIVATE CAMERA";

        // Fitur Deteksi Muka (Native / Mock jika tidak disupport)
        if (window.FaceDetector) {
            const detector = new window.FaceDetector();
            faceInterval = setInterval(async () => {
                try {
                    const faces = await detector.detect(camera);
                    if (faces.length > 0) {
                        const face = faces[0].boundingBox;
                        const rect = camera.getBoundingClientRect();
                        const scaleX = rect.width / camera.videoWidth;
                        const scaleY = rect.height / camera.videoHeight;
                        
                        // Menyesuaikan posisi karena kamera ter-flip (scaleX(-1))
                        faceBox.style.width = (face.width * scaleX) + "px";
                        faceBox.style.height = (face.height * scaleY) + "px";
                        faceBox.style.left = (rect.width - (face.left * scaleX) - (face.width * scaleX)/2) + "px";
                        faceBox.style.top = (face.top * scaleY + (face.height * scaleY)/2) + "px";
                        faceBox.style.display = "block";
                        cameraStatus.textContent = "TARGET ACQUIRED";
                    } else {
                        faceBox.style.display = "none";
                        cameraStatus.textContent = "SCANNING FOR FACES...";
                    }
                } catch (e) { console.error(e); }
            }, 150);
        } else {
            // Mock Tracking Keren Jika Browser Tidak Support FaceDetector
            faceBox.style.display = "block";
            faceBox.style.left = "50%";
            faceBox.style.top = "50%";
            cameraStatus.textContent = "CAMERA ON (MOCK TRACKING)";
            
            let angle = 0;
            faceInterval = setInterval(() => {
                angle += 0.1;
                const offsetX = Math.sin(angle) * 15;
                const offsetY = Math.cos(angle) * 15;
                faceBox.style.transform = `translate(calc(-50% + ${offsetX}px), calc(-50% + ${offsetY}px)) scale(${1 + Math.sin(angle*2)*0.1})`;
            }, 50);
        }
    } catch (error) {
        addMessage("SYSTEM", "Camera access denied or unavailable.", "system");
    }
}
cameraButton.onclick = toggleCamera;

</script>
</body>
</html>
"""

# ============================================================
# FLASK ROUTES
# ============================================================

@app.route("/")
def index():
    return Response(HTML, mimetype="text/html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_msg = data.get("message", "")
    user_name = data.get("name", "User")

    if not GROQ_API_KEY:
        return jsonify({"answer": f"System Error: API Key missing. Please inform {CREATOR} or set your GROQ_API_KEY."}), 500

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    # Prompt System untuk JARVIS. Meminta agar ia merespon dengan bahasa Indonesia/campur agar sesuai dengan pengguna.
    system_prompt = (
        f"You are J.A.R.V.I.S, an advanced and highly intelligent personal AI assistant created by {CREATOR}. "
        f"The user's name is '{user_name}'. You must ALWAYS address the user by their name in your responses. "
        "Keep your answers brief, intelligent, and helpful. You can speak Indonesian or English depending on what the user uses."
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
        resp = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=payload)
        resp.raise_for_status()
        answer = resp.json()["choices"][0]["message"]["content"]
        return jsonify({"answer": answer})
    except Exception as e:
        return jsonify({"error": f"Groq API Error: {str(e)}"}), 500

@app.route("/transcribe", methods=["POST"])
def transcribe():
    if 'audio' not in request.files:
        return jsonify({"error": "No audio file provided."}), 400

    audio_file = request.files['audio']

    if not GROQ_API_KEY:
        return jsonify({"error": "API Key missing."}), 500

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}"
    }

    files = {
        'file': (audio_file.filename, audio_file.read(), audio_file.content_type),
        'model': (None, WHISPER_MODEL)
    }

    try:
        resp = requests.post("https://api.groq.com/openai/v1/audio/transcriptions", headers=headers, files=files)
        resp.raise_for_status()
        text = resp.json().get("text", "")
        return jsonify({"text": text})
    except Exception as e:
        return jsonify({"error": f"Transcription Error: {str(e)}"}), 500

if __name__ == "__main__":
    # Menjalankan server lokal
    app.run(host="0.0.0.0", port=5000, debug=True)
