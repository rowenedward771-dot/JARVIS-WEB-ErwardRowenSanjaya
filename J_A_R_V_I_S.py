import os
import requests
from flask import Flask, request, jsonify, Response

app = Flask(__name__)

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

MODEL = "llama-3.1-8b-instant"
CREATOR = "Erward Rowen Sanjaya"

conversation = [
    {
        "role": "system",
        "content": f"""
You are J.A.R.V.I.S, a personal AI assistant created by {CREATOR}.

Always speak English unless the user asks for another language.
Be intelligent, calm, helpful and slightly futuristic.
Keep answers reasonably concise because they may be spoken aloud.
Do not claim to control devices or systems that you cannot actually access.
"""
    }
]


HTML = r"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<meta name="theme-color" content="#02060d">

<title>J.A.R.V.I.S</title>

<style>

*{
    box-sizing:border-box;
}

html,body{
    margin:0;
    width:100%;
    min-height:100%;
    font-family:Arial,Helvetica,sans-serif;
    background:#02060d;
    color:#e8faff;
}

body{
    overflow-x:hidden;
    position:relative;
}

/* BACKGROUND */

.background{
    position:fixed;
    inset:0;
    overflow:hidden;
    z-index:-5;
    background:
        radial-gradient(circle at 50% 45%,#06334b 0%,#020913 35%,#01040a 75%);
}

.grid{
    position:absolute;
    inset:-50%;
    background-image:
        linear-gradient(rgba(0,220,255,.08) 1px,transparent 1px),
        linear-gradient(90deg,rgba(0,220,255,.08) 1px,transparent 1px);
    background-size:55px 55px;
    transform:perspective(500px) rotateX(60deg);
    animation:gridMove 12s linear infinite;
}

@keyframes gridMove{
    from{transform:perspective(500px) rotateX(60deg) translateY(0);}
    to{transform:perspective(500px) rotateX(60deg) translateY(55px);}
}

.scan{
    position:absolute;
    width:100%;
    height:2px;
    background:linear-gradient(
        90deg,
        transparent,
        #00eaff,
        transparent
    );
    box-shadow:0 0 20px #00eaff;
    opacity:.5;
    animation:scan 5s linear infinite;
}

@keyframes scan{
    0%{top:-5%;}
    100%{top:105%;}
}

.particle{
    position:absolute;
    width:3px;
    height:3px;
    background:#00eaff;
    border-radius:50%;
    box-shadow:0 0 10px #00eaff;
    animation:float 6s infinite ease-in-out;
}

@keyframes float{
    0%,100%{transform:translateY(0);opacity:.3;}
    50%{transform:translateY(-35px);opacity:1;}
}

/* HEADER */

header{
    height:82px;
    display:flex;
    align-items:center;
    justify-content:space-between;
    padding:0 5%;
    border-bottom:1px solid rgba(0,220,255,.2);
    background:rgba(2,8,15,.75);
    backdrop-filter:blur(15px);
}

.brand{
    display:flex;
    align-items:center;
    gap:14px;
}

.logo{
    width:48px;
    height:48px;
    border:2px solid #00eaff;
    border-radius:50%;
    display:flex;
    align-items:center;
    justify-content:center;
    font-size:25px;
    font-weight:bold;
    color:#00eaff;
    box-shadow:
        0 0 10px #00eaff,
        inset 0 0 15px rgba(0,234,255,.25);
    animation:pulse 2s infinite;
}

@keyframes pulse{
    0%,100%{box-shadow:0 0 10px #00eaff,inset 0 0 15px rgba(0,234,255,.25);}
    50%{box-shadow:0 0 30px #00eaff,inset 0 0 25px rgba(0,234,255,.4);}
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
    box-shadow:0 0 15px #00ff9d;
}

/* MAIN */

main{
    width:min(1250px,94%);
    margin:30px auto;
    display:grid;
    grid-template-columns:380px 1fr;
    gap:25px;
}

/* CORE */

.core-panel{
    min-height:650px;
    border:1px solid rgba(0,234,255,.25);
    background:rgba(3,13,23,.7);
    border-radius:22px;
    display:flex;
    flex-direction:column;
    align-items:center;
    justify-content:center;
    position:relative;
    overflow:hidden;
    box-shadow:0 0 50px rgba(0,180,255,.08);
}

.core-panel:before{
    content:"";
    position:absolute;
    inset:0;
    background:radial-gradient(circle,#00eaff12,transparent 65%);
}

.core{
    width:210px;
    height:210px;
    border-radius:50%;
    border:2px solid #00eaff;
    display:flex;
    align-items:center;
    justify-content:center;
    position:relative;
    box-shadow:
        0 0 30px #00eaff,
        inset 0 0 45px #00eaff44;
    animation:corePulse 3s infinite;
}

@keyframes corePulse{
    0%,100%{transform:scale(1);}
    50%{transform:scale(1.05);}
}

.core:before,
.core:after{
    content:"";
    position:absolute;
    border-radius:50%;
    border:1px solid #00eaff;
}

.core:before{
    inset:-25px;
    border-left-color:transparent;
    border-right-color:transparent;
    animation:spin 5s linear infinite;
}

.core:after{
    inset:-45px;
    border-top-color:transparent;
    border-bottom-color:transparent;
    animation:spinReverse 8s linear infinite;
}

@keyframes spin{
    to{transform:rotate(360deg);}
}

@keyframes spinReverse{
    to{transform:rotate(-360deg);}
}

.core-inner{
    width:125px;
    height:125px;
    border-radius:50%;
    background:radial-gradient(circle,#1de8ff,#006c8b 45%,#02131d 75%);
    display:flex;
    align-items:center;
    justify-content:center;
    font-size:55px;
    font-weight:bold;
    color:white;
    text-shadow:0 0 20px white;
    box-shadow:0 0 40px #00eaff;
}

.core-status{
    margin-top:75px;
    font-size:12px;
    letter-spacing:3px;
    color:#00eaff;
}

.talk{
    margin-top:30px;
    border:1px solid #00eaff;
    color:#00eaff;
    background:#03131c;
    padding:14px 22px;
    border-radius:30px;
    cursor:pointer;
    letter-spacing:1px;
    transition:.25s;
    box-shadow:0 0 15px #00eaff33;
}

.talk:hover{
    background:#00eaff;
    color:#001018;
    box-shadow:0 0 30px #00eaff;
}

.talk.listening{
    background:#ff1744;
    border-color:#ff1744;
    color:white;
    box-shadow:0 0 30px #ff1744;
}

/* CHAT */

.chat{
    min-height:650px;
    border:1px solid rgba(0,234,255,.25);
    background:rgba(3,13,23,.7);
    border-radius:22px;
    display:flex;
    flex-direction:column;
    overflow:hidden;
}

.chat-header{
    padding:22px 25px;
    border-bottom:1px solid rgba(0,234,255,.18);
    display:flex;
    justify-content:space-between;
}

.chat-header h2{
    margin:0 0 5px;
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
    border:1px solid #24515d;
    color:#7da7b0;
    padding:7px 13px;
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
    animation:messageIn .3s ease;
}

@keyframes messageIn{
    from{opacity:0;transform:translateY(10px);}
    to{opacity:1;transform:translateY(0);}
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
    padding:13px 16px;
    border-radius:12px;
    background:#061522;
    border:1px solid rgba(0,234,255,.12);
    line-height:1.5;
    font-size:14px;
}

.user .text{
    background:#073343;
}

.system .text{
    color:#7597a0;
}

.input{
    padding:18px;
    display:flex;
    gap:10px;
    border-top:1px solid rgba(0,234,255,.18);
}

.input input{
    flex:1;
    background:#020b13;
    border:1px solid #17434f;
    border-radius:10px;
    color:white;
    padding:14px;
    outline:none;
}

.input input:focus{
    border-color:#00eaff;
    box-shadow:0 0 15px #00eaff22;
}

.send{
    background:#00eaff;
    color:#001018;
    border:0;
    border-radius:10px;
    padding:0 25px;
    font-weight:bold;
    cursor:pointer;
}

footer{
    text-align:center;
    padding:20px;
    border-top:1px solid rgba(0,234,255,.15);
    color:#55747d;
    font-size:10px;
    letter-spacing:2px;
}

@media(max-width:850px){
    main{
        grid-template-columns:1fr;
    }

    .core-panel{
        min-height:400px;
    }

    .core{
        width:150px;
        height:150px;
    }

    .core-inner{
        width:90px;
        height:90px;
        font-size:40px;
    }
}

</style>
</head>

<body>

<div class="background">
    <div class="grid"></div>
    <div class="scan"></div>

    <div class="particle" style="left:10%;top:30%;"></div>
    <div class="particle" style="left:25%;top:70%;animation-delay:1s;"></div>
    <div class="particle" style="left:60%;top:20%;animation-delay:2s;"></div>
    <div class="particle" style="left:80%;top:60%;animation-delay:3s;"></div>
    <div class="particle" style="left:90%;top:25%;animation-delay:4s;"></div>
</div>

<header>

<div class="brand">

<div class="logo">J</div>

<div>
<h1>J.A.R.V.I.S</h1>
<span>PERSONAL AI SYSTEM</span>
</div>

</div>

<div class="status">
<div class="dot"></div>
<span id="status">ONLINE</span>
</div>

</header>

<main>

<section class="core-panel">

<div class="core">
<div class="core-inner">J</div>
</div>

<div class="core-status" id="coreStatus">
AI CORE ONLINE
</div>

<button class="talk" id="talk">
🎙️ TALK TO JARVIS
</button>

</section>

<section class="chat">

<div class="chat-header">

<div>
<h2>CONVERSATION</h2>
<span>CLOUD AI • J.A.R.V.I.S</span>
</div>

<button class="clear" id="clear">CLEAR</button>

</div>

<div class="messages" id="messages">

<div class="message system">
<div class="sender">SYSTEM</div>
<div class="text">
J.A.R.V.I.S initialized.<br><br>
Cloud AI core connected.<br><br>
Voice system ready.
</div>
</div>

<div class="message jarvis">
<div class="sender">JARVIS</div>
<div class="text">
Welcome back, Owen. How may I assist you?
</div>
</div>

</div>

<div class="input">

<input
id="input"
placeholder="Speak or type your command..."
autocomplete="off"
>

<button class="send" id="send">
SEND
</button>

</div>

</section>

</main>

<footer>
<span>J.A.R.V.I.S SYSTEM</span>
&nbsp;&nbsp;|&nbsp;&nbsp;
<span>Created by Erward Rowen Sanjaya</span>
</footer>

<script>

const messages=document.getElementById("messages");
const input=document.getElementById("input");
const send=document.getElementById("send");
const talk=document.getElementById("talk");
const clear=document.getElementById("clear");
const status=document.getElementById("status");
const coreStatus=document.getElementById("coreStatus");

function setStatus(value){
    status.textContent=value;
    coreStatus.textContent="AI CORE "+value;
}

function addMessage(sender,text,type){

    const box=document.createElement("div");
    box.className="message "+type;

    const senderEl=document.createElement("div");
    senderEl.className="sender";
    senderEl.textContent=sender;

    const textEl=document.createElement("div");
    textEl.className="text";
    textEl.textContent=text;

    box.appendChild(senderEl);
    box.appendChild(textEl);

    messages.appendChild(box);

    messages.scrollTop=messages.scrollHeight;
}

function speak(text){

    if(!("speechSynthesis" in window)){
        return;
    }

    speechSynthesis.cancel();

    const voice=new SpeechSynthesisUtterance(text);

    voice.lang="en-US";
    voice.rate=.95;
    voice.pitch=.85;
    voice.volume=1;

    voice.onstart=()=>{
        setStatus("SPEAKING");
    };

    voice.onend=()=>{
        setStatus("ONLINE");
    };

    speechSynthesis.speak(voice);
}

async function sendMessage(){

    const text=input.value.trim();

    if(!text){
        return;
    }

    addMessage("YOU",text,"user");

    input.value="";

    setStatus("THINKING");

    try{

        const response=await fetch("/chat",{
            method:"POST",
            headers:{
                "Content-Type":"application/json"
            },
            body:JSON.stringify({
                message:text
            })
        });

        const data=await response.json();

        if(data.answer){

            addMessage(
                "JARVIS",
                data.answer,
                "jarvis"
            );

            speak(data.answer);

        }else{

            addMessage(
                "SYSTEM",
                data.error || "Unknown error.",
                "system"
            );

        }

    }catch(error){

        addMessage(
            "SYSTEM",
            "Connection error.",
            "system"
        );

    }

    setStatus("ONLINE");
}

send.onclick=sendMessage;

input.addEventListener("keydown",function(e){

    if(e.key==="Enter"){
        sendMessage();
    }

});

clear.onclick=function(){

    messages.innerHTML="";

    addMessage(
        "SYSTEM",
        "Conversation cleared.",
        "system"
    );

};

/* VOICE */

let recognition=null;

const SpeechRecognition=
    window.SpeechRecognition ||
    window.webkitSpeechRecognition;

if(SpeechRecognition){

    recognition=new SpeechRecognition();

    recognition.lang="en-US";
    recognition.continuous=false;
    recognition.interimResults=false;

    recognition.onstart=function(){

        setStatus("LISTENING");

        talk.classList.add("listening");

        talk.textContent="🎙️ LISTENING...";

    };

    recognition.onresult=function(event){

        const text=
            event.results[0][0].transcript;

        input.value=text;

        sendMessage();

    };

    recognition.onerror=function(){

        setStatus("ONLINE");

        talk.classList.remove("listening");

        talk.textContent="🎙️ TALK TO JARVIS";

    };

    recognition.onend=function(){

        setStatus("ONLINE");

        talk.classList.remove("listening");

        talk.textContent="🎙️ TALK TO JARVIS";

    };

}

talk.onclick=function(){

    if(!recognition){

        alert(
            "Voice recognition is not supported by this browser. Try Chrome or Edge."
        );

        return;

    }

    recognition.start();

};

</script>

</body>
</html>
"""


@app.route("/")
def home():
    return Response(HTML, mimetype="text/html")


@app.route("/chat", methods=["POST"])
def chat():

    global conversation

    data = request.get_json(silent=True) or {}

    message = str(data.get("message", "")).strip()

    if not message:
        return jsonify({
            "error": "Empty message."
        }), 400

    if not GROQ_API_KEY:
        return jsonify({
            "error": "GROQ_API_KEY is not configured."
        }), 500

    conversation.append({
        "role": "user",
        "content": message
    })

    try:

        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": MODEL,
                "messages": conversation,
                "temperature": 0.7,
                "max_tokens": 500
            },
            timeout=60
        )

        response.raise_for_status()

        result = response.json()

        answer = (
            result["choices"][0]["message"]["content"]
            .strip()
        )

        conversation.append({
            "role": "assistant",
            "content": answer
        })

        # Keep memory from growing forever
        if len(conversation) > 21:

            conversation = (
                [conversation[0]]
                + conversation[-20:]
            )

        return jsonify({
            "answer": answer
        })

    except Exception as error:

        print("GROQ ERROR:", error)

        return jsonify({
            "error": "J.A.R.V.I.S could not connect to the cloud AI."
        }), 500


@app.route("/health")
def health():

    return jsonify({
        "status": "online",
        "creator": CREATOR,
        "ai": MODEL
    })


if __name__ == "__main__":

    port = int(
        os.environ.get(
            "PORT",
            5000
        )
    )

    print()
    print("======================================")
    print("          J.A.R.V.I.S WEB")
    print("======================================")
    print("Creator  :", CREATOR)
    print("AI Model :", MODEL)
    print("Status   : ONLINE")
    print("Voice    : BROWSER")
    print("Memory   : ENABLED")
    print("UI       : FUTURISTIC")
    print("Port     :", port)
    print("======================================")
    print()

    app.run(
        host="0.0.0.0",
        port=port
    )
