import os
import io
import threading
import requests

from flask import Flask, request, jsonify, Response

# ============================================================

# J.A.R.V.I.S

# Personal AI Assistant

# Created by Erward Rowen Sanjaya

# ============================================================

app = Flask(**name**)

CREATOR = "Erward Rowen Sanjaya"

# Current Groq production model

CHAT_MODEL = "llama-3.3-70b-versatile"

# Groq speech-to-text model

STT_MODEL = "whisper-large-v3-turbo"

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

GROQ_CHAT_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_STT_URL = "https://api.groq.com/openai/v1/audio/transcriptions"

# ============================================================

# CONVERSATION MEMORY

# ============================================================

SYSTEM_PROMPT = f"""
You are J.A.R.V.I.S, a personal AI assistant created by {CREATOR}.

Personality:

* Intelligent
* Calm
* Helpful
* Slightly futuristic
* Professional
* Friendly
* Concise when possible

Rules:

* Always speak English unless the user asks for another language.
* Never claim that you control hardware, computers, phones, cameras,
  smart homes, or other systems unless an actual tool has been provided.
* If the user asks what you are, say that you are J.A.R.V.I.S.
* If the user asks who created you, say Erward Rowen Sanjaya.
* Do not pretend to have abilities that you do not have.
* Give useful direct answers.
* Since your responses may be spoken aloud, avoid unnecessary formatting.
  """

conversation = [
{
"role": "system",
"content": SYSTEM_PROMPT
}
]

conversation_lock = threading.Lock()

# ============================================================

# HELPERS

# ============================================================

def groq_headers():
return {
"Authorization": f"Bearer {GROQ_API_KEY}"
}

def add_conversation(role, content):
global conversation

```
with conversation_lock:

    conversation.append({
        "role": role,
        "content": content
    })

    # Keep the system prompt plus the latest 20 messages.
    if len(conversation) > 21:

        conversation = (
            [conversation[0]]
            + conversation[-20:]
        )
```

def ask_jarvis(message):

```
if not GROQ_API_KEY:

    raise RuntimeError(
        "GROQ_API_KEY is not configured on the server."
    )

add_conversation("user", message)

with conversation_lock:

    messages = list(conversation)

response = requests.post(
    GROQ_CHAT_URL,
    headers={
        **groq_headers(),
        "Content-Type": "application/json"
    },
    json={
        "model": CHAT_MODEL,
        "messages": messages,
        "temperature": 0.6,
        "max_completion_tokens": 700
    },
    timeout=60
)

if not response.ok:

    try:
        error_data = response.json()
    except Exception:
        error_data = response.text

    print("GROQ CHAT ERROR:", error_data)

    raise RuntimeError(
        f"Groq AI request failed ({response.status_code})."
    )

data = response.json()

try:

    answer = (
        data["choices"][0]["message"]["content"]
        .strip()
    )

except Exception:

    print("INVALID GROQ RESPONSE:", data)

    raise RuntimeError(
        "Invalid response received from Groq."
    )

add_conversation("assistant", answer)

return answer
```

def transcribe_audio(audio_bytes, filename="recording.webm"):

```
if not GROQ_API_KEY:

    raise RuntimeError(
        "GROQ_API_KEY is not configured on the server."
    )

files = {
    "file": (
        filename,
        io.BytesIO(audio_bytes),
        "audio/webm"
    )
}

data = {
    "model": STT_MODEL,
    "language": "en",
    "response_format": "json",
    "temperature": "0"
}

response = requests.post(
    GROQ_STT_URL,
    headers=groq_headers(),
    files=files,
    data=data,
    timeout=90
)

if not response.ok:

    try:
        error_data = response.json()
    except Exception:
        error_data = response.text

    print("GROQ STT ERROR:", error_data)

    raise RuntimeError(
        f"Speech recognition failed ({response.status_code})."
    )

result = response.json()

text = str(
    result.get("text", "")
).strip()

if not text:

    raise RuntimeError(
        "No speech was detected."
    )

return text
```

# ============================================================

# FRONTEND

# ============================================================

HTML = r"""

<!DOCTYPE html>

<html lang="en">

<head>

<meta charset="UTF-8">

<meta
name="viewport"
content="width=device-width, initial-scale=1.0"

>

<meta
name="theme-color"
content="#02060d"

>

<title>J.A.R.V.I.S</title>

<style>

*{
    box-sizing:border-box;
}

html,
body{

    margin:0;

    width:100%;

    min-height:100%;

    font-family:
        Arial,
        Helvetica,
        sans-serif;

    background:#02060d;

    color:#e8faff;
}

body{

    min-height:100vh;

    overflow-x:hidden;
}


/* ============================================================
   BACKGROUND
   ============================================================ */

.background{

    position:fixed;

    inset:0;

    overflow:hidden;

    z-index:-10;

    background:
        radial-gradient(
            circle at 50% 45%,
            #06334b 0%,
            #020913 35%,
            #01040a 75%
        );
}

.grid{

    position:absolute;

    inset:-50%;

    background-image:
        linear-gradient(
            rgba(0,220,255,.08) 1px,
            transparent 1px
        ),
        linear-gradient(
            90deg,
            rgba(0,220,255,.08) 1px,
            transparent 1px
        );

    background-size:55px 55px;

    transform:
        perspective(500px)
        rotateX(60deg);

    animation:
        gridMove 12s linear infinite;
}

@keyframes gridMove{

    from{

        transform:
            perspective(500px)
            rotateX(60deg)
            translateY(0);
    }

    to{

        transform:
            perspective(500px)
            rotateX(60deg)
            translateY(55px);
    }
}

.scan{

    position:absolute;

    width:100%;

    height:2px;

    background:
        linear-gradient(
            90deg,
            transparent,
            #00eaff,
            transparent
        );

    box-shadow:
        0 0 20px #00eaff;

    opacity:.5;

    animation:
        scan 5s linear infinite;
}

@keyframes scan{

    0%{
        top:-5%;
    }

    100%{
        top:105%;
    }
}


/* ============================================================
   HEADER
   ============================================================ */

header{

    height:82px;

    display:flex;

    align-items:center;

    justify-content:space-between;

    padding:
        0 5%;

    border-bottom:
        1px solid
        rgba(0,220,255,.2);

    background:
        rgba(2,8,15,.75);

    backdrop-filter:
        blur(15px);
}

.brand{

    display:flex;

    align-items:center;

    gap:14px;
}

.logo{

    width:48px;

    height:48px;

    border:
        2px solid
        #00eaff;

    border-radius:50%;

    display:flex;

    align-items:center;

    justify-content:center;

    font-size:25px;

    font-weight:bold;

    color:#00eaff;

    box-shadow:
        0 0 10px #00eaff,
        inset 0 0 15px
        rgba(0,234,255,.25);

    animation:
        pulse 2s infinite;
}

@keyframes pulse{

    0%,
    100%{

        box-shadow:
            0 0 10px #00eaff,
            inset 0 0 15px
            rgba(0,234,255,.25);
    }

    50%{

        box-shadow:
            0 0 30px #00eaff,
            inset 0 0 25px
            rgba(0,234,255,.4);
    }
}

.brand h1{

    margin:0;

    letter-spacing:4px;

    font-size:23px;
}

.brand span{

    color:#6c9da8;

    font-size:10px;

    letter-spacing:2px;
}

.status{

    display:flex;

    align-items:center;

    gap:8px;

    font-size:12px;

    letter-spacing:2px;
}

.dot{

    width:9px;

    height:9px;

    background:#00ff9d;

    border-radius:50%;

    box-shadow:
        0 0 15px #00ff9d;
}


/* ============================================================
   MAIN
   ============================================================ */

main{

    width:min(
        1250px,
        94%
    );

    margin:
        30px auto;

    display:grid;

    grid-template-columns:
        380px 1fr;

    gap:25px;
}


/* ============================================================
   CORE
   ============================================================ */

.core-panel{

    min-height:650px;

    border:
        1px solid
        rgba(0,234,255,.25);

    background:
        rgba(3,13,23,.7);

    border-radius:22px;

    display:flex;

    flex-direction:column;

    align-items:center;

    justify-content:center;

    position:relative;

    overflow:hidden;

    box-shadow:
        0 0 50px
        rgba(0,180,255,.08);
}

.core-panel:before{

    content:"";

    position:absolute;

    inset:0;

    background:
        radial-gradient(
            circle,
            #00eaff12,
            transparent 65%
        );
}

.core{

    width:210px;

    height:210px;

    border-radius:50%;

    border:
        2px solid
        #00eaff;

    display:flex;

    align-items:center;

    justify-content:center;

    position:relative;

    box-shadow:
        0 0 30px #00eaff,
        inset 0 0 45px #00eaff44;

    animation:
        corePulse 3s infinite;
}

@keyframes corePulse{

    0%,
    100%{
        transform:scale(1);
    }

    50%{
        transform:scale(1.05);
    }
}

.core:before,
.core:after{

    content:"";

    position:absolute;

    border-radius:50%;

    border:
        1px solid
        #00eaff;
}

.core:before{

    inset:-25px;

    border-left-color:
        transparent;

    border-right-color:
        transparent;

    animation:
        spin 5s linear infinite;
}

.core:after{

    inset:-45px;

    border-top-color:
        transparent;

    border-bottom-color:
        transparent;

    animation:
        spinReverse 8s linear infinite;
}

@keyframes spin{

    to{
        transform:
            rotate(360deg);
    }
}

@keyframes spinReverse{

    to{
        transform:
            rotate(-360deg);
    }
}

.core-inner{

    width:125px;

    height:125px;

    border-radius:50%;

    background:
        radial-gradient(
            circle,
            #1de8ff,
            #006c8b 45%,
            #02131d 75%
        );

    display:flex;

    align-items:center;

    justify-content:center;

    font-size:55px;

    font-weight:bold;

    color:white;

    text-shadow:
        0 0 20px white;

    box-shadow:
        0 0 40px #00eaff;
}

.core-status{

    margin-top:75px;

    font-size:12px;

    letter-spacing:3px;

    color:#00eaff;

    text-align:center;
}


/* ============================================================
   TALK BUTTON
   ============================================================ */

.talk{

    margin-top:30px;

    border:
        1px solid
        #00eaff;

    color:#00eaff;

    background:#03131c;

    padding:
        14px 22px;

    border-radius:30px;

    cursor:pointer;

    letter-spacing:1px;

    transition:.25s;

    box-shadow:
        0 0 15px
        #00eaff33;
}

.talk:hover{

    background:#00eaff;

    color:#001018;

    box-shadow:
        0 0 30px
        #00eaff;
}

.talk.recording{

    background:#ff1744;

    border-color:#ff1744;

    color:white;

    box-shadow:
        0 0 30px
        #ff1744;

    animation:
        recordingPulse 1s infinite;
}

@keyframes recordingPulse{

    50%{
        transform:scale(1.04);
    }
}


/* ============================================================
   CHAT
   ============================================================ */

.chat{

    min-height:650px;

    border:
        1px solid
        rgba(0,234,255,.25);

    background:
        rgba(3,13,23,.7);

    border-radius:22px;

    display:flex;

    flex-direction:column;

    overflow:hidden;
}

.chat-header{

    padding:
        22px 25px;

    border-bottom:
        1px solid
        rgba(0,234,255,.18);

    display:flex;

    justify-content:space-between;

    align-items:center;
}

.chat-header h2{

    margin:
        0 0 5px;

    letter-spacing:3px;

    font-size:16px;
}

.chat-header span{

    color:#628995;

    font-size:10px;

    letter-spacing:2px;
}

.clear{

    background:transparent;

    border:
        1px solid
        #24515d;

    color:#7da7b0;

    padding:
        7px 13px;

    border-radius:5px;

    cursor:pointer;
}

.messages{

    flex:1;

    overflow-y:auto;

    padding:25px;
}

.message{

    margin-bottom:20px;

    max-width:85%;

    animation:
        messageIn .3s ease;
}

@keyframes messageIn{

    from{

        opacity:0;

        transform:
            translateY(10px);
    }

    to{

        opacity:1;

        transform:
            translateY(0);
    }
}

.message.user{

    margin-left:auto;

    text-align:right;
}

.sender{

    font-size:10px;

    letter-spacing:2px;

    color:#00eaff;

    margin-bottom:6px;
}

.text{

    padding:
        13px 16px;

    border-radius:12px;

    background:#061522;

    border:
        1px solid
        rgba(0,234,255,.12);

    line-height:1.5;

    font-size:14px;

    white-space:pre-wrap;

    word-wrap:break-word;
}

.user .text{

    background:#073343;
}

.system .text{

    color:#7597a0;
}


/* ============================================================
   INPUT
   ============================================================ */

.input{

    padding:18px;

    display:flex;

    gap:10px;

    border-top:
        1px solid
        rgba(0,234,255,.18);
}

.input input{

    flex:1;

    background:#020b13;

    border:
        1px solid
        #17434f;

    border-radius:10px;

    color:white;

    padding:14px;

    outline:none;
}

.input input:focus{

    border-color:
        #00eaff;

    box-shadow:
        0 0 15px
        #00eaff22;
}

.send{

    background:#00eaff;

    color:#001018;

    border:0;

    border-radius:10px;

    padding:
        0 25px;

    font-weight:bold;

    cursor:pointer;
}

.send:disabled{

    opacity:.5;

    cursor:not-allowed;
}


/* ============================================================
   FOOTER
   ============================================================ */

footer{

    text-align:center;

    padding:20px;

    border-top:
        1px solid
        rgba(0,234,255,.15);

    color:#55747d;

    font-size:10px;

    letter-spacing:2px;
}


/* ============================================================
   MOBILE
   ============================================================ */

@media(max-width:850px){

    header{

        padding:
            0 20px;
    }

    .brand h1{

        font-size:18px;
    }

    main{

        grid-template-columns:1fr;
    }

    .core-panel{

        min-height:420px;
    }

    .core{

        width:160px;

        height:160px;
    }

    .core-inner{

        width:100px;

        height:100px;

        font-size:42px;
    }

    .messages{

        padding:18px;
    }

    .input{

        padding:12px;
    }

    .send{

        padding:
            0 18px;
    }
}

</style>

</head>

<body>

<div class="background">

```
<div class="grid"></div>

<div class="scan"></div>
```

</div>

<header>

```
<div class="brand">

    <div class="logo">
        J
    </div>

    <div>

        <h1>
            J.A.R.V.I.S
        </h1>

        <span>
            PERSONAL AI SYSTEM
        </span>

    </div>

</div>


<div class="status">

    <div class="dot"></div>

    <span id="statusEl">
        ONLINE
    </span>

</div>
```

</header>

<main>

<section class="core-panel">

```
<div class="core">

    <div class="core-inner">
        J
    </div>

</div>


<div
    class="core-status"
    id="coreStatus"
>
    AI CORE ONLINE
</div>


<button
    class="talk"
    id="talkBtn"
>
    🎙️ TALK TO JARVIS
</button>
```

</section>

<section class="chat">

```
<div class="chat-header">

    <div>

        <h2>
            CONVERSATION
        </h2>

        <span>
            GROQ AI • VOICE ENABLED
        </span>

    </div>


    <button
        class="clear"
        id="clearBtn"
    >
        CLEAR
    </button>

</div>


<div
    class="messages"
    id="messages"
>

    <div class="message system">

        <div class="sender">
            SYSTEM
        </div>

        <div class="text">
            J.A.R.V.I.S initialized.
            Cloud AI core connected.
            Voice interface ready.
        </div>

    </div>


    <div class="message jarvis">

        <div class="sender">
            JARVIS
        </div>

        <div class="text">
            Welcome back, Owen. How may I assist you?
        </div>

    </div>

</div>


<div class="input">

    <input
        id="input"
        placeholder="Type your command..."
        autocomplete="off"
    >

    <button
        class="send"
        id="sendBtn"
    >
        SEND
    </button>

</div>
```

</section>

</main>

<footer>

```
J.A.R.V.I.S SYSTEM
&nbsp;&nbsp;|&nbsp;&nbsp;
Created by Erward Rowen Sanjaya
```

</footer>

<script>

/* ============================================================
   ELEMENTS
   ============================================================ */

const messages =
    document.getElementById("messages");

const input =
    document.getElementById("input");

const sendBtn =
    document.getElementById("sendBtn");

const talkBtn =
    document.getElementById("talkBtn");

const clearBtn =
    document.getElementById("clearBtn");

const statusEl =
    document.getElementById("statusEl");

const coreStatus =
    document.getElementById("coreStatus");


/* ============================================================
   STATE
   ============================================================ */

let mediaRecorder = null;

let audioChunks = [];

let isRecording = false;

let currentAudio = null;


/* ============================================================
   STATUS
   ============================================================ */

function setStatus(value){

    statusEl.textContent =
        value;

    coreStatus.textContent =
        "AI CORE " + value;
}


/* ============================================================
   CHAT UI
   ============================================================ */

function addMessage(
    sender,
    text,
    type
){

    const box =
        document.createElement("div");

    box.className =
        "message " + type;


    const senderEl =
        document.createElement("div");

    senderEl.className =
        "sender";

    senderEl.textContent =
        sender;


    const textEl =
        document.createElement("div");

    textEl.className =
        "text";

    textEl.textContent =
        text;


    box.appendChild(
        senderEl
    );

    box.appendChild(
        textEl
    );


    messages.appendChild(
        box
    );


    messages.scrollTop =
        messages.scrollHeight;

    return textEl;
}


/* ============================================================
   TEXT TO SPEECH
   ============================================================ */

function speak(text){

    if(
        !("speechSynthesis" in window)
    ){

        return;
    }


    speechSynthesis.cancel();


    const utterance =
        new SpeechSynthesisUtterance(
            text
        );


    utterance.lang =
        "en-US";

    utterance.rate =
        0.95;

    utterance.pitch =
        0.82;

    utterance.volume =
        1;


    utterance.onstart =
        function(){

            setStatus(
                "SPEAKING"
            );
        };


    utterance.onend =
        function(){

            setStatus(
                "ONLINE"
            );
        };


    utterance.onerror =
        function(){

            setStatus(
                "ONLINE"
            );
        };


    speechSynthesis.speak(
        utterance
    );
}


/* ============================================================
   SEND TEXT TO JARVIS
   ============================================================ */

async function sendMessage(
    customText = null
){

    const text =
        customText !== null
            ? customText.trim()
            : input.value.trim();


    if(!text){

        return;
    }


    addMessage(
        "YOU",
        text,
        "user"
    );


    input.value =
        "";


    sendBtn.disabled =
        true;


    talkBtn.disabled =
        true;


    setStatus(
        "THINKING"
    );


    try{

        const response =
            await fetch(
                "/chat",
                {
                    method:"POST",

                    headers:{
                        "Content-Type":
                            "application/json"
                    },

                    body:
                        JSON.stringify({
                            message:text
                        })
                }
            );


        let data;


        try{

            data =
                await response.json();

        }catch{

            throw new Error(
                "Invalid server response."
            );
        }


        if(!response.ok){

            throw new Error(
                data.error ||
                "J.A.R.V.I.S server error."
            );
        }


        if(!data.answer){

            throw new Error(
                "J.A.R.V.I.S returned no answer."
            );
        }


        addMessage(
            "JARVIS",
            data.answer,
            "jarvis"
        );


        speak(
            data.answer
        );


    }catch(error){

        console.error(
            "CHAT ERROR:",
            error
        );


        addMessage(
            "SYSTEM",
            error.message ||
            "Connection error.",
            "system"
        );


        setStatus(
            "ERROR"
        );


        setTimeout(
            function(){

                setStatus(
                    "ONLINE"
                );

            },
            2000
        );

    }finally{

        sendBtn.disabled =
            false;

        talkBtn.disabled =
            false;

        input.focus();
    }
}


/* ============================================================
   MICROPHONE
   ============================================================ */

async function startRecording(){

    if(isRecording){

        stopRecording();

        return;
    }


    if(
        !navigator.mediaDevices ||
        !navigator.mediaDevices.getUserMedia
    ){

        addMessage(
            "SYSTEM",
            "Your browser does not support microphone access.",
            "system"
        );

        return;
    }


    try{

        const stream =
            await navigator.mediaDevices.getUserMedia(
                {
                    audio:{
                        echoCancellation:true,
                        noiseSuppression:true,
                        autoGainControl:true
                    }
                }
            );


        audioChunks = [];


        let mimeType =
            "audio/webm";


        if(
            !MediaRecorder.isTypeSupported(
                "audio/webm"
            )
        ){

            mimeType =
                "audio/webm;codecs=opus";
        }


        mediaRecorder =
            new MediaRecorder(
                stream,
                {
                    mimeType:
                        mimeType
                }
            );


        mediaRecorder.ondataavailable =
            function(event){

                if(
                    event.data &&
                    event.data.size > 0
                ){

                    audioChunks.push(
                        event.data
                    );
                }
            };


        mediaRecorder.onstop =
            async function(){

                stream
                    .getTracks()
                    .forEach(
                        track =>
                            track.stop()
                    );


                const audioBlob =
                    new Blob(
                        audioChunks,
                        {
                            type:
                                mediaRecorder.mimeType ||
                                "audio/webm"
                        }
                    );


                await processRecording(
                    audioBlob
                );
            };


        mediaRecorder.start();


        isRecording =
            true;


        talkBtn.classList.add(
            "recording"
        );


        talkBtn.textContent =
            "⏹️ STOP LISTENING";


        setStatus(
            "LISTENING"
        );


    }catch(error){

        console.error(
            "MIC ERROR:",
            error
        );


        let message =
            "Microphone could not be started.";


        if(
            error.name ===
            "NotAllowedError"
        ){

            message =
                "Microphone permission was denied. Allow microphone access in your browser settings and try again.";

        }else if(
            error.name ===
            "NotFoundError"
        ){

            message =
                "No microphone was found on this device.";

        }else if(
            error.name ===
            "NotReadableError"
        ){

            message =
                "The microphone is already being used by another application.";

        }else if(
            error.name ===
            "SecurityError"
        ){

            message =
                "The browser blocked microphone access for security reasons.";
        }


        addMessage(
            "SYSTEM",
            message,
            "system"
        );
    }
}


function stopRecording(){

    if(
        mediaRecorder &&
        mediaRecorder.state !==
        "inactive"
    ){

        mediaRecorder.stop();
    }


    isRecording =
        false;


    talkBtn.classList.remove(
        "recording"
    );


    talkBtn.textContent =
        "🎙️ TALK TO JARVIS";


    setStatus(
        "PROCESSING"
    );
}


/* ============================================================
   SEND RECORDING TO SERVER
   ============================================================ */

async function processRecording(
    audioBlob
){

    if(
        !audioBlob ||
        audioBlob.size === 0
    ){

        addMessage(
            "SYSTEM",
            "No audio was recorded.",
            "system"
        );

        setStatus(
            "ONLINE"
        );

        return;
    }


    try{

        const formData =
            new FormData();


        formData.append(
            "audio",
            audioBlob,
            "jarvis-recording.webm"
        );


        const response =
            await fetch(
                "/transcribe",
                {
                    method:"POST",
                    body:formData
                }
            );


        let data;


        try{

            data =
                await response.json();

        }catch{

            throw new Error(
                "Invalid transcription response."
            );
        }


        if(!response.ok){

            throw new Error(
                data.error ||
                "Speech recognition failed."
            );
        }


        const transcript =
            (data.text || "").trim();


        if(!transcript){

            throw new Error(
                "I could not understand the recording."
            );
        }


        addMessage(
            "YOU",
            transcript,
            "user"
        );


        setStatus(
            "THINKING"
        );


        const chatResponse =
            await fetch(
                "/chat",
                {
                    method:"POST",

                    headers:{
                        "Content-Type":
                            "application/json"
                    },

                    body:
                        JSON.stringify({
                            message:
                                transcript
                        })
                }
            );


        const chatData =
            await chatResponse.json();


        if(!chatResponse.ok){

            throw new Error(
                chatData.error ||
                "J.A.R.V.I.S could not answer."
            );
        }


        addMessage(
            "JARVIS",
            chatData.answer,
            "jarvis"
        );


        speak(
            chatData.answer
        );


    }catch(error){

        console.error(
            "VOICE ERROR:",
            error
        );


        addMessage(
            "SYSTEM",
            error.message ||
            "Voice processing failed.",
            "system"
        );


        setStatus(
            "ERROR"
        );


        setTimeout(
            function(){

                setStatus(
                    "ONLINE"
                );

            },
            2000
        );
    }
}


/* ============================================================
   BUTTONS
   ============================================================ */

sendBtn.onclick =
    function(){

        sendMessage();
    };


input.addEventListener(
    "keydown",
    function(event){

        if(
            event.key ===
            "Enter"
        ){

            event.preventDefault();

            sendMessage();
        }
    }
);


talkBtn.onclick =
    function(){

        if(isRecording){

            stopRecording();

        }else{

            startRecording();
        }
    };


clearBtn.onclick =
    function(){

        messages.innerHTML = "";


        addMessage(
            "SYSTEM",
            "Conversation cleared.",
            "system"
        );


        setStatus(
            "ONLINE"
        );
    };


/* ============================================================
   INITIALIZE SPEECH SYNTHESIS
   ============================================================ */

if(
    "speechSynthesis"
    in window
){

    speechSynthesis.getVoices();

    speechSynthesis.onvoiceschanged =
        function(){

            speechSynthesis.getVoices();
        };
}


/* ============================================================
   INITIAL STATE
   ============================================================ */

setStatus(
    "ONLINE"
);

input.focus();

</script>

</body>

</html>
"""

# ============================================================

# ROUTES

# ============================================================

@app.route("/")
def home():

```
return Response(
    HTML,
    mimetype="text/html"
)
```

@app.route("/chat", methods=["POST"])
def chat():

```
data = request.get_json(
    silent=True
) or {}


message = str(
    data.get(
        "message",
        ""
    )
).strip()


if not message:

    return jsonify({
        "error":
            "Please enter a message."
    }), 400


try:

    answer =
        ask_jarvis(
            message
        )


    return jsonify({
        "answer":
            answer
    })


except Exception as error:

    print(
        "CHAT ERROR:",
        error
    )


    return jsonify({
        "error":
            str(error)
    }), 500
```

@app.route(
"/transcribe",
methods=["POST"]
)
def transcribe():

```
if "audio" not in request.files:

    return jsonify({
        "error":
            "No audio file was received."
    }), 400


audio =
    request.files["audio"]


audio_bytes =
    audio.read()


if not audio_bytes:

    return jsonify({
        "error":
            "The audio recording was empty."
    }), 400


try:

    text =
        transcribe_audio(
            audio_bytes,
            audio.filename or
            "recording.webm"
        )


    return jsonify({
        "text":
            text
    })


except Exception as error:

    print(
        "TRANSCRIPTION ERROR:",
        error
    )


    return jsonify({
        "error":
            str(error)
    }), 500
```

@app.route("/health")
def health():

```
return jsonify({

    "status":
        "online",

    "creator":
        CREATOR,

    "chat_model":
        CHAT_MODEL,

    "speech_model":
        STT_MODEL,

    "voice":
        "enabled",

    "memory":
        "enabled"
})
```

# ============================================================

# START SERVER

# ============================================================

if **name** == "**main**":

```
port =
    int(
        os.environ.get(
            "PORT",
            8080
        )
    )


print()
print(
    "======================================"
)
print(
    "          J.A.R.V.I.S WEB"
)
print(
    "======================================"
)
print(
    "Creator :",
    CREATOR
)
print(
    "AI      :",
    CHAT_MODEL
)
print(
    "STT     :",
    STT_MODEL
)
print(
    "Voice   : ENABLED"
)
print(
    "Memory  : ENABLED"
)
print(
    "Port    :",
    port
)
print(
    "======================================"
)
print()


app.run(
    host="0.0.0.0",
    port=port
)
```
