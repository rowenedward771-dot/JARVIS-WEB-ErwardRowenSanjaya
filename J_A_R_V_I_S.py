from flask import Flask, request, jsonify, render_template_string
import ollama
import threading
import time

# ============================================================
# J.A.R.V.I.S - SINGLE FILE WEB AI
# Creator: Erward Rowen Sanjaya
# ============================================================

app = Flask(__name__)

MODEL = "llama3.2:3b"
PORT = 5000

conversation = [
    {
        "role": "system",
        "content": """
You are J.A.R.V.I.S, a personal AI assistant created by Erward Rowen Sanjaya.

Your personality:
- Intelligent
- Calm
- Helpful
- Futuristic
- Professional
- Slightly like a sophisticated movie AI assistant

Always address the user as Owen when appropriate.

Speak English unless the user speaks Indonesian.
Keep normal answers reasonably concise because they may be spoken aloud.

You are running locally through Ollama.
Do not claim to have internet access unless it is actually provided.
Do not claim to control physical devices unless a tool is actually connected.
"""
    }
]


# ============================================================
# HTML + CSS + JAVASCRIPT
# Everything is inside this Python file.
# ============================================================

HTML = r"""
<!DOCTYPE html>
<html lang="en">

<head>

<meta charset="UTF-8">

<meta name="viewport"
      content="width=device-width, initial-scale=1.0">

<meta name="theme-color"
      content="#02050a">

<title>J.A.R.V.I.S</title>

<style>

/* ============================================================
   RESET
============================================================ */

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

html,
body {
    width: 100%;
    min-height: 100%;
}

body {

    background:
        radial-gradient(
            circle at 50% 20%,
            rgba(0, 180, 255, 0.12),
            transparent 35%
        ),
        radial-gradient(
            circle at 80% 80%,
            rgba(0, 80, 255, 0.08),
            transparent 30%
        ),
        #02050a;

    color: #dff8ff;

    font-family:
        "Segoe UI",
        Arial,
        sans-serif;

    overflow-x: hidden;
}


/* ============================================================
   BACKGROUND
============================================================ */

.background {

    position: fixed;

    inset: 0;

    pointer-events: none;

    overflow: hidden;

    z-index: 0;
}

.grid {

    position: absolute;

    inset: -50%;

    background-image:
        linear-gradient(
            rgba(0, 180, 255, 0.045) 1px,
            transparent 1px
        ),
        linear-gradient(
            90deg,
            rgba(0, 180, 255, 0.045) 1px,
            transparent 1px
        );

    background-size: 45px 45px;

    transform:
        perspective(600px)
        rotateX(60deg);

    animation:
        gridMove 12s linear infinite;
}

@keyframes gridMove {

    from {
        transform:
            perspective(600px)
            rotateX(60deg)
            translateY(0);
    }

    to {
        transform:
            perspective(600px)
            rotateX(60deg)
            translateY(45px);
    }
}


.scanline {

    position: absolute;

    width: 100%;

    height: 2px;

    background:
        linear-gradient(
            90deg,
            transparent,
            rgba(0,220,255,.7),
            transparent
        );

    box-shadow:
        0 0 20px #00cfff;

    animation:
        scan 5s linear infinite;
}

@keyframes scan {

    0% {
        top: -5%;
        opacity: 0;
    }

    10% {
        opacity: 1;
    }

    90% {
        opacity: 1;
    }

    100% {
        top: 105%;
        opacity: 0;
    }
}


.particle {

    position: absolute;

    width: 3px;
    height: 3px;

    background: #66eaff;

    border-radius: 50%;

    box-shadow:
        0 0 10px #00d9ff;

    animation:
        floatParticle linear infinite;
}

@keyframes floatParticle {

    from {
        transform:
            translateY(110vh)
            translateX(0);
        opacity: 0;
    }

    15% {
        opacity: 1;
    }

    85% {
        opacity: 1;
    }

    to {
        transform:
            translateY(-20vh)
            translateX(80px);
        opacity: 0;
    }
}


/* ============================================================
   HEADER
============================================================ */

header {

    position: relative;

    z-index: 2;

    display: flex;

    justify-content: space-between;

    align-items: center;

    padding: 22px 35px;

    border-bottom:
        1px solid rgba(0,210,255,.15);

    background:
        rgba(2,8,15,.65);

    backdrop-filter:
        blur(15px);

    box-shadow:
        0 10px 40px rgba(0,0,0,.25);
}

.brand {

    display: flex;

    align-items: center;

    gap: 15px;
}

.logo {

    width: 52px;
    height: 52px;

    display: flex;

    justify-content: center;
    align-items: center;

    border-radius: 14px;

    border:
        1px solid #00d9ff;

    color: #7ff3ff;

    font-size: 27px;

    font-weight: 700;

    box-shadow:
        0 0 20px rgba(0,217,255,.3),
        inset 0 0 20px rgba(0,217,255,.08);

    animation:
        logoPulse 2s ease-in-out infinite;
}

@keyframes logoPulse {

    0%,100% {
        box-shadow:
            0 0 15px rgba(0,217,255,.2);
    }

    50% {
        box-shadow:
            0 0 35px rgba(0,217,255,.65);
    }
}

.brand h1 {

    font-size: 24px;

    letter-spacing: 5px;
}

.brand span {

    display: block;

    margin-top: 3px;

    font-size: 10px;

    letter-spacing: 3px;

    color: #4f8e9c;
}


.status {

    display: flex;

    align-items: center;

    gap: 9px;

    font-size: 11px;

    letter-spacing: 2px;

    color: #6fffd2;
}

.status-dot {

    width: 9px;
    height: 9px;

    border-radius: 50%;

    background: #00ff9d;

    box-shadow:
        0 0 10px #00ff9d,
        0 0 25px #00ff9d;

    animation:
        statusPulse 1.2s infinite;
}

@keyframes statusPulse {

    0%,100% {
        transform: scale(1);
        opacity: .7;
    }

    50% {
        transform: scale(1.4);
        opacity: 1;
    }
}


/* ============================================================
   MAIN
============================================================ */

main {

    position: relative;

    z-index: 1;

    max-width: 1400px;

    margin: auto;

    padding: 35px;

    display: grid;

    grid-template-columns:
        minmax(320px, .9fr)
        minmax(400px, 1.5fr);

    gap: 30px;
}


/* ============================================================
   CORE PANEL
============================================================ */

.core-panel {

    min-height: 620px;

    display: flex;

    flex-direction: column;

    justify-content: center;

    align-items: center;

    position: relative;

    border:
        1px solid rgba(0,210,255,.15);

    border-radius: 25px;

    background:
        linear-gradient(
            145deg,
            rgba(4,20,30,.8),
            rgba(2,7,14,.8)
        );

    box-shadow:
        0 0 60px rgba(0,160,255,.06);

    overflow: hidden;
}

.core-panel::before {

    content: "";

    position: absolute;

    inset: 0;

    background:
        radial-gradient(
            circle,
            rgba(0,200,255,.08),
            transparent 50%
        );

    animation:
        coreBackground 4s ease-in-out infinite;
}

@keyframes coreBackground {

    0%,100% {
        opacity: .5;
    }

    50% {
        opacity: 1;
    }
}


/* ============================================================
   ARC REACTOR
============================================================ */

.core-container {

    width: 360px;
    height: 360px;

    position: relative;

    display: flex;

    justify-content: center;
    align-items: center;
}

.ring {

    position: absolute;

    border-radius: 50%;

    border: 1px solid rgba(0,210,255,.4);

    box-shadow:
        0 0 20px rgba(0,200,255,.15),
        inset 0 0 20px rgba(0,200,255,.08);
}

.ring1 {

    width: 330px;
    height: 330px;

    border-top-color: #00e5ff;

    animation:
        rotate 8s linear infinite;
}

.ring2 {

    width: 280px;
    height: 280px;

    border-right-color: #00aaff;

    animation:
        rotateReverse 6s linear infinite;
}

.ring3 {

    width: 220px;
    height: 220px;

    border-bottom-color: #00ffff;

    animation:
        rotate 4s linear infinite;
}

.ring4 {

    width: 170px;
    height: 170px;

    border-left-color: #80f6ff;

    animation:
        rotateReverse 3s linear infinite;
}

@keyframes rotate {

    from {
        transform: rotate(0deg);
    }

    to {
        transform: rotate(360deg);
    }
}

@keyframes rotateReverse {

    from {
        transform: rotate(360deg);
    }

    to {
        transform: rotate(0deg);
    }
}

.core {

    width: 125px;
    height: 125px;

    border-radius: 50%;

    display: flex;

    justify-content: center;
    align-items: center;

    position: relative;

    z-index: 3;

    background:
        radial-gradient(
            circle,
            #c9fbff 0%,
            #29dcff 18%,
            #0088bb 45%,
            #003044 70%,
            #020a10 100%
        );

    border:
        3px solid #a8f8ff;

    box-shadow:
        0 0 25px #00d9ff,
        0 0 60px rgba(0,210,255,.8),
        0 0 120px rgba(0,130,255,.45);

    animation:
        corePulse 2s ease-in-out infinite;
}

@keyframes corePulse {

    0%,100% {
        transform: scale(.95);

        box-shadow:
            0 0 20px #00d9ff,
            0 0 50px rgba(0,210,255,.7);
    }

    50% {
        transform: scale(1.05);

        box-shadow:
            0 0 35px #00eaff,
            0 0 90px rgba(0,210,255,.9);
    }
}

.core-text {

    font-size: 45px;

    font-weight: 800;

    color: white;

    text-shadow:
        0 0 20px #00eaff;
}


.core-info {

    position: relative;

    z-index: 2;

    text-align: center;

    margin-top: 10px;
}

.core-info h2 {

    font-size: 13px;

    letter-spacing: 4px;

    color: #6fefff;
}

.core-info p {

    margin-top: 8px;

    font-size: 10px;

    color: #4f7f8c;

    letter-spacing: 2px;
}


/* ============================================================
   TALK BUTTON
============================================================ */

.talk {

    position: relative;

    z-index: 5;

    margin-top: 30px;

    padding: 15px 28px;

    border-radius: 50px;

    border:
        1px solid #00d9ff;

    background:
        rgba(0,190,255,.08);

    color: #b9f7ff;

    font-weight: 700;

    letter-spacing: 1px;

    cursor: pointer;

    transition: .25s;

    box-shadow:
        0 0 20px rgba(0,200,255,.15);
}

.talk:hover {

    transform:
        translateY(-3px)
        scale(1.03);

    background:
        rgba(0,200,255,.2);

    box-shadow:
        0 0 35px rgba(0,220,255,.5);
}

.talk.listening {

    background:
        rgba(255,60,80,.15);

    border-color:
        #ff5368;

    box-shadow:
        0 0 30px rgba(255,60,80,.5);

    animation:
        listeningPulse 1s infinite;
}

@keyframes listeningPulse {

    0%,100% {
        transform: scale(1);
    }

    50% {
        transform: scale(1.05);
    }
}


/* ============================================================
   CHAT
============================================================ */

.chat-panel {

    min-height: 620px;

    display: flex;

    flex-direction: column;

    border:
        1px solid rgba(0,210,255,.15);

    border-radius: 25px;

    overflow: hidden;

    background:
        rgba(3,11,18,.78);

    backdrop-filter:
        blur(15px);

    box-shadow:
        0 20px 80px rgba(0,0,0,.35);
}

.chat-header {

    display: flex;

    justify-content: space-between;

    align-items: center;

    padding: 20px 24px;

    border-bottom:
        1px solid rgba(0,210,255,.12);
}

.chat-header h2 {

    font-size: 13px;

    letter-spacing: 3px;
}

.chat-header span {

    display: block;

    margin-top: 5px;

    font-size: 9px;

    color: #4f8290;

    letter-spacing: 2px;
}

.clear {

    padding: 8px 13px;

    border:
        1px solid rgba(0,200,255,.25);

    border-radius: 8px;

    background:
        transparent;

    color: #6397a3;

    cursor: pointer;
}

.clear:hover {

    color: #fff;

    border-color:
        #00d9ff;
}


/* ============================================================
   MESSAGES
============================================================ */

.messages {

    flex: 1;

    overflow-y: auto;

    padding: 25px;

    scroll-behavior: smooth;
}

.messages::-webkit-scrollbar {

    width: 5px;
}

.messages::-webkit-scrollbar-thumb {

    background: #087c9c;

    border-radius: 10px;
}

.message {

    margin-bottom: 20px;

    padding: 15px 17px;

    border-radius: 14px;

    animation:
        messageIn .35s ease;
}

@keyframes messageIn {

    from {
        opacity: 0;
        transform:
            translateY(12px)
            scale(.98);
    }

    to {
        opacity: 1;
        transform:
            translateY(0)
            scale(1);
    }
}

.message .sender {

    font-size: 9px;

    letter-spacing: 2px;

    margin-bottom: 7px;
}

.message .text {

    line-height: 1.6;

    font-size: 14px;

    white-space: pre-wrap;
}

.message.system {

    background:
        rgba(0,150,190,.04);

    border-left:
        2px solid #17677b;

    color: #6c9ca8;
}

.message.jarvis {

    background:
        linear-gradient(
            90deg,
            rgba(0,170,220,.1),
            rgba(0,170,220,.025)
        );

    border-left:
        2px solid #00d9ff;

    box-shadow:
        0 0 25px rgba(0,200,255,.04);
}

.message.jarvis .sender {

    color: #00e5ff;
}

.message.user {

    background:
        rgba(80,100,130,.1);

    border-right:
        2px solid #657c8c;

    text-align: right;
}

.message.user .sender {

    color: #9eabb5;
}


/* ============================================================
   INPUT
============================================================ */

.input-area {

    display: flex;

    gap: 10px;

    padding: 18px;

    border-top:
        1px solid rgba(0,210,255,.12);
}

.input {

    flex: 1;

    min-width: 0;

    padding: 14px 17px;

    border-radius: 12px;

    border:
        1px solid rgba(0,210,255,.2);

    background:
        rgba(0,0,0,.35);

    color: white;

    outline: none;

    font-size: 14px;
}

.input:focus {

    border-color:
        #00d9ff;

    box-shadow:
        0 0 20px rgba(0,200,255,.1);
}

.send {

    padding: 0 20px;

    border: none;

    border-radius: 12px;

    background:
        linear-gradient(
            135deg,
            #00b7df,
            #006caa
        );

    color: white;

    font-weight: 700;

    cursor: pointer;

    transition: .2s;
}

.send:hover {

    transform: scale(1.04);

    box-shadow:
        0 0 25px rgba(0,200,255,.35);
}

.send:disabled {

    opacity: .5;

    cursor: not-allowed;
}


/* ============================================================
   FOOTER
============================================================ */

footer {

    position: relative;

    z-index: 2;

    padding: 20px 30px;

    display: flex;

    justify-content: space-between;

    gap: 20px;

    border-top:
        1px solid rgba(0,210,255,.12);

    color: #426b76;

    font-size: 10px;

    letter-spacing: 1.5px;

    background:
        rgba(2,7,12,.6);
}


/* ============================================================
   RESPONSIVE
============================================================ */

@media (max-width: 900px) {

    main {

        grid-template-columns: 1fr;

        padding: 18px;
    }

    .core-panel,
    .chat-panel {

        min-height: 550px;
    }

    .core-container {

        transform: scale(.8);
    }

}

@media (max-width: 550px) {

    header {

        padding: 17px;
    }

    .brand h1 {

        font-size: 18px;
    }

    .brand span {

        font-size: 8px;
    }

    .core-container {

        transform: scale(.65);
    }

    footer {

        flex-direction: column;

        text-align: center;
    }
}

</style>

</head>


<body>

<!-- ============================================================
     BACKGROUND
============================================================ -->

<div class="background">

    <div class="grid"></div>

    <div class="scanline"></div>

    <div class="particle"
         style="left:8%;animation-duration:9s;"></div>

    <div class="particle"
         style="left:18%;animation-duration:12s;animation-delay:2s;"></div>

    <div class="particle"
         style="left:35%;animation-duration:8s;animation-delay:4s;"></div>

    <div class="particle"
         style="left:55%;animation-duration:14s;animation-delay:1s;"></div>

    <div class="particle"
         style="left:73%;animation-duration:10s;animation-delay:3s;"></div>

    <div class="particle"
         style="left:90%;animation-duration:13s;animation-delay:5s;"></div>

</div>


<!-- ============================================================
     HEADER
============================================================ -->

<header>

    <div class="brand">

        <div class="logo">J</div>

        <div>

            <h1>J.A.R.V.I.S</h1>

            <span>PERSONAL AI SYSTEM</span>

        </div>

    </div>


    <div class="status">

        <span class="status-dot"></span>

        <span id="status">
            ONLINE
        </span>

    </div>

</header>


<!-- ============================================================
     MAIN
============================================================ -->

<main>


    <!-- CORE -->

    <section class="core-panel">

        <div class="core-container">

            <div class="ring ring1"></div>

            <div class="ring ring2"></div>

            <div class="ring ring3"></div>

            <div class="ring ring4"></div>

            <div class="core">

                <div class="core-text">
                    J
                </div>

            </div>

        </div>


        <div class="core-info">

            <h2 id="coreStatus">
                AI CORE ONLINE
            </h2>

            <p>
                LLAMA 3.2 3B • LOCAL INTELLIGENCE
            </p>

        </div>


        <button
            id="talkButton"
            class="talk">

            🎙️ TALK TO JARVIS

        </button>

    </section>


    <!-- CHAT -->

    <section class="chat-panel">

        <div class="chat-header">

            <div>

                <h2>
                    CONVERSATION
                </h2>

                <span>
                    LOCAL AI • LLAMA 3.2 3B
                </span>

            </div>


            <button
                id="clearButton"
                class="clear">

                CLEAR

            </button>

        </div>


        <div
            id="messages"
            class="messages">

            <div class="message system">

                <div class="sender">
                    SYSTEM
                </div>

                <div class="text">
                    J.A.R.V.I.S initialized.

                    Local AI core connected.

                    Voice system ready.
                </div>

            </div>


            <div class="message jarvis">

                <div class="sender">
                    JARVIS
                </div>

                <div class="text">
                    Welcome back, Owen.
                    How may I assist you?
                </div>

            </div>

        </div>


        <div class="input-area">

            <input
                id="messageInput"
                class="input"
                type="text"
                placeholder="Speak or type your command..."
                autocomplete="off"
            >

            <button
                id="sendButton"
                class="send">

                SEND

            </button>

        </div>

    </section>

</main>


<!-- ============================================================
     FOOTER
============================================================ -->

<footer>

    <span>
        J.A.R.V.I.S SYSTEM
    </span>

    <span>
        Created by Erward Rowen Sanjaya
    </span>

</footer>


<script>

/* ============================================================
   ELEMENTS
============================================================ */

const messages =
    document.getElementById("messages");

const input =
    document.getElementById("messageInput");

const sendButton =
    document.getElementById("sendButton");

const talkButton =
    document.getElementById("talkButton");

const clearButton =
    document.getElementById("clearButton");

const status =
    document.getElementById("status");

const coreStatus =
    document.getElementById("coreStatus");


/* ============================================================
   STATUS
============================================================ */

function setStatus(text) {

    status.textContent = text;

    coreStatus.textContent =
        "AI CORE " + text;
}


/* ============================================================
   ADD MESSAGE
============================================================ */

function addMessage(sender, text, type) {

    const message =
        document.createElement("div");

    message.className =
        "message " + type;


    const senderElement =
        document.createElement("div");

    senderElement.className =
        "sender";

    senderElement.textContent =
        sender;


    const textElement =
        document.createElement("div");

    textElement.className =
        "text";

    textElement.textContent =
        text;


    message.appendChild(senderElement);

    message.appendChild(textElement);

    messages.appendChild(message);


    messages.scrollTop =
        messages.scrollHeight;
}


/* ============================================================
   SPEAK
============================================================ */

function speak(text) {

    if (!("speechSynthesis" in window)) {
        return;
    }


    window.speechSynthesis.cancel();


    const utterance =
        new SpeechSynthesisUtterance(text);


    utterance.lang = "en-US";

    utterance.rate = 0.92;

    utterance.pitch = 0.82;

    utterance.volume = 1;


    utterance.onstart = function() {

        setStatus("SPEAKING");

    };


    utterance.onend = function() {

        setStatus("ONLINE");

    };


    window.speechSynthesis.speak(
        utterance
    );
}


/* ============================================================
   SEND MESSAGE
============================================================ */

async function sendMessage() {

    const message =
        input.value.trim();


    if (!message) {
        return;
    }


    addMessage(
        "YOU",
        message,
        "user"
    );


    input.value = "";


    sendButton.disabled = true;

    setStatus("THINKING");


    try {

        const response =
            await fetch(
                "/chat",
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({
                        message: message
                    })
                }
            );


        const data =
            await response.json();


        if (data.answer) {

            addMessage(
                "JARVIS",
                data.answer,
                "jarvis"
            );

            speak(data.answer);

        } else {

            addMessage(
                "SYSTEM",
                "JARVIS returned no response.",
                "system"
            );

        }

    }

    catch (error) {

        console.error(error);


        addMessage(
            "SYSTEM",
            "Cannot connect to JARVIS AI core. Make sure Ollama is running.",
            "system"
        );

        setStatus("ERROR");

    }


    sendButton.disabled = false;

    if (status.textContent !== "SPEAKING") {
        setStatus("ONLINE");
    }
}


/* ============================================================
   VOICE RECOGNITION
============================================================ */

let recognition = null;

function startListening() {

    const SpeechRecognition =
        window.SpeechRecognition ||
        window.webkitSpeechRecognition;


    if (!SpeechRecognition) {

        alert(
            "Voice recognition is not supported by this browser. Please use Google Chrome."
        );

        return;
    }


    if (recognition) {

        try {
            recognition.stop();
        } catch(e) {}

    }


    recognition =
        new SpeechRecognition();


    recognition.lang =
        "en-US";

    recognition.continuous =
        false;

    recognition.interimResults =
        false;


    recognition.onstart =
        function() {

            setStatus("LISTENING");

            talkButton.classList.add(
                "listening"
            );

            talkButton.textContent =
                "🎙️ LISTENING...";

        };


    recognition.onresult =
        function(event) {

            const text =
                event.results[0][0]
                .transcript;


            input.value = text;


            talkButton.classList.remove(
                "listening"
            );

            talkButton.textContent =
                "🎙️ TALK TO JARVIS";


            sendMessage();

        };


    recognition.onerror =
        function(event) {

            console.log(
                "Voice recognition error:",
                event.error
            );


            setStatus("ONLINE");


            talkButton.classList.remove(
                "listening"
            );


            talkButton.textContent =
                "🎙️ TALK TO JARVIS";

        };


    recognition.onend =
        function() {

            talkButton.classList.remove(
                "listening"
            );


            talkButton.textContent =
                "🎙️ TALK TO JARVIS";

        };


    try {

        recognition.start();

    }

    catch(error) {

        console.log(error);

    }
}


/* ============================================================
   BUTTONS
============================================================ */

sendButton.addEventListener(
    "click",
    sendMessage
);


talkButton.addEventListener(
    "click",
    startListening
);


clearButton.addEventListener(
    "click",
    function() {

        messages.innerHTML = "";

        addMessage(
            "SYSTEM",
            "Conversation cleared.",
            "system"
        );

    }
);


input.addEventListener(
    "keydown",
    function(event) {

        if (event.key === "Enter") {

            sendMessage();

        }

    }
);


/* ============================================================
   STARTUP
============================================================ */

console.log(
    "J.A.R.V.I.S Web Interface initialized."
);

</script>

</body>

</html>
"""


# ============================================================
# ROUTES
# ============================================================

@app.route("/")
def home():

    return render_template_string(HTML)


@app.route("/chat", methods=["POST"])
def chat():

    try:

        data = request.get_json(silent=True)

        if not data:
            return jsonify({
                "answer": "I did not receive your message."
            }), 400


        message = data.get("message", "")

        if not isinstance(message, str):
            return jsonify({
                "answer": "Invalid message."
            }), 400


        message = message.strip()


        if not message:

            return jsonify({
                "answer": "Please say something, Owen."
            }), 400


        conversation.append({
            "role": "user",
            "content": message
        })


        response = ollama.chat(
            model=MODEL,
            messages=conversation
        )


        answer = response["message"]["content"].strip()


        conversation.append({
            "role": "assistant",
            "content": answer
        })


        return jsonify({
            "answer": answer
        })


    except Exception as error:

        print()
        print("======================================")
        print("OLLAMA ERROR")
        print("======================================")
        print(error)
        print("======================================")
        print()


        return jsonify({
            "answer":
            "Sorry Owen, my local AI core is unavailable. Please make sure Ollama is running."
        })


# ============================================================
# START SERVER
# ============================================================

if __name__ == "__main__":

    print()
    print("======================================")
    print("          J.A.R.V.I.S WEB")
    print("======================================")
    print("Creator  : Erward Rowen Sanjaya")
    print("AI Model : " + MODEL)
    print("Status   : ONLINE")
    print("Voice    : BROWSER")
    print("Memory   : ENABLED")
    print("UI       : FUTURISTIC")
    print("Port     : " + str(PORT))
    print("======================================")
    print()
    print("Open your browser:")
    print("http://127.0.0.1:5000")
    print()
    print("J.A.R.V.I.S is ready.")
    print()


    app.run(
        host="0.0.0.0",
        port=PORT,
        debug=False,
        threaded=True
    )