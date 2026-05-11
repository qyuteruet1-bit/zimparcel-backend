from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import os
import json
from datetime import datetime

app = Flask(__name__)
CORS(app)

# ============================================
# ZIMPARCEL FULL HTML (your existing UI)
# ============================================
ZIMPARCEL_HTML = r'''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
    <meta name="theme-color" content="#020617">
    <title>ZimParcel | Nditakurire Ecosystem</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Urbanist:wght@400;600;700;900&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
    <style>
        :root {--zim-green:#0A5C36;--zim-dark:#020617;--zim-card:#0f172a;--zim-lime:#deff9a;--zim-orange:#F28C28}
        *{-webkit-tap-highlight-color:transparent}
        body{font-family:'Urbanist',sans-serif;background:#000;margin:0;padding:0;overflow:hidden;user-select:none;-webkit-user-select:none}
        .app-container{position:relative;width:100%;max-width:450px;height:100vh;height:100dvh;margin:0 auto;background:var(--zim-dark);overflow:hidden;box-shadow:0 0 50px rgba(0,0,0,0.8)}
        .screen{position:absolute;inset:0;display:none;flex-direction:column;width:100%;height:100%;z-index:10;animation:fadeIn .3s cubic-bezier(.175,.885,.32,1.275)}
        .screen.active{display:flex!important}
        @keyframes fadeIn{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:translateY(0)}}
        .clickable:active{transform:scale(.97);opacity:.85;transition:all .1s}
        .badge-glow{box-shadow:0 0 15px rgba(222,255,154,.3)}
        .toast{animation:toastIn .3s ease-out}@keyframes toastIn{0%{opacity:0;transform:translateY(20px)}100%{opacity:1;transform:translateY(0)}}
        .star-rating .star{font-size:2.5rem;cursor:pointer;transition:transform .15s;color:rgba(255,255,255,.2)}
        .star-rating .star.active{color:var(--zim-orange);transform:scale(1.1)}
    </style>
</head>
<body>
<div class="app-container" id="app-root"></div>

<script>
// ========== SCREEN DATA ==========
const screens = {
    splash: `<div class="screen active bg-[#020617] text-white flex flex-col items-center justify-center p-8 z-50">
        <div class="text-center mb-10"><h1 class="text-6xl font-black tracking-tighter mb-1">Zim<span class="text-[#deff9a]">Parcel</span></h1><p class="text-[11px] text-white/50 font-bold uppercase tracking-[0.4em]">Project Nditakurire 2.0</p></div>
        <div class="relative w-full h-24 mb-16 flex items-center justify-center"><i class="fa-solid fa-people-carry-box text-7xl text-[#deff9a]"></i></div>
        <div class="w-full bg-white/5 h-1 rounded-full overflow-hidden"><div class="h-full bg-[#deff9a]" style="width:100%;transition:width 2s"></div></div>
        <p class="text-[10px] text-white/30 font-bold uppercase tracking-widest mt-4">Loading ZimCare Network...</p>
    </div>`,
    
    portal: `<div class="screen bg-[#020617] text-white p-8" style="overflow-y:auto">
        <header class="flex justify-between items-center mt-8 mb-10"><div><h2 class="text-3xl font-black mb-1">Nditakurire Portal</h2><p class="text-[11px] text-[#deff9a] font-bold uppercase tracking-widest"><i class="fa-solid fa-shield-check mr-1"></i> Verified ✓</p></div><div class="w-12 h-12 rounded-2xl bg-white/10 border border-white/20 overflow-hidden"><img src="https://ui-avatars.com/api/?name=Rutendo+M&background=deff9a&color=020617" alt="User"></div></header>
        <div class="space-y-5">
            <button onclick="navigate('sender')" class="clickable w-full bg-[#0f172a] border border-white/10 p-5 rounded-[30px] flex items-center gap-5 shadow-xl"><div class="w-14 h-14 bg-[#0A5C36]/20 rounded-2xl flex items-center justify-center text-2xl text-[#deff9a]"><i class="fa-solid fa-box-open"></i></div><div class="text-left flex-1"><p class="font-bold text-lg">Sender</p><p class="text-white/40 text-xs">Post local goods to the cloud</p></div><i class="fa-solid fa-chevron-right text-white/20"></i></button>
            <button onclick="navigate('courier')" class="clickable w-full bg-[#0f172a] border border-white/10 p-5 rounded-[30px] flex items-center gap-5 shadow-xl"><div class="w-14 h-14 bg-[#F28C28]/20 rounded-2xl flex items-center justify-center text-2xl text-[#F28C28]"><i class="fa-solid fa-truck-ramp-box"></i></div><div class="text-left flex-1"><p class="font-bold text-lg">Deliver & Earn</p><p class="text-white/40 text-xs">Share dead space & bid on trips</p></div><i class="fa-solid fa-chevron-right text-white/20"></i></button>
            <button onclick="navigate('chat')" class="clickable w-full bg-[#0f172a] border border-white/10 p-5 rounded-[30px] flex items-center gap-5 shadow-xl"><div class="w-14 h-14 bg-[#25D366]/20 rounded-2xl flex items-center justify-center text-2xl text-[#25D366]"><i class="fa-brands fa-whatsapp"></i></div><div class="text-left flex-1"><p class="font-bold text-lg">Negotiation Chat</p><p class="text-white/40 text-xs">Bid & agree with couriers</p></div><i class="fa-solid fa-chevron-right text-white/20"></i></button>
            <button onclick="navigate('history')" class="clickable w-full bg-[#0f172a] border border-white/10 p-5 rounded-[30px] flex items-center gap-5 shadow-xl"><div class="w-14 h-14 bg-blue-500/15 rounded-2xl flex items-center justify-center text-2xl text-blue-400"><i class="fa-solid fa-clock-rotate-left"></i></div><div class="text-left flex-1"><p class="font-bold text-lg">Transaction History</p><p class="text-white/40 text-xs">Past deliveries & records</p></div><i class="fa-solid fa-chevron-right text-white/20"></i></button>
        </div>
    </div>`,

    sender: `<div class="screen bg-[#f8fafc] text-[#0f172a] flex flex-col">
        <header class="bg-white p-6 pt-12 border-b border-gray-100 flex items-center gap-4 shadow-sm"><button onclick="navigate('portal')" class="w-10 h-10 bg-slate-50 rounded-full flex items-center justify-center text-gray-400"><i class="fa-solid fa-chevron-left"></i></button><h2 class="text-2xl font-black text-[#0A5C36]">Post a Delivery</h2></header>
        <div class="p-6 flex-1 overflow-y-auto space-y-4">
            <div class="bg-white p-5 rounded-[25px] border border-gray-100 shadow-sm"><p class="text-[10px] font-bold text-gray-400 uppercase tracking-widest mb-3">Job Details</p>
                <div class="space-y-3">
                    <input id="job-desc" type="text" placeholder="What are you sending?" class="w-full bg-slate-50 border border-gray-100 p-4 rounded-2xl text-sm">
                    <div class="flex gap-3"><input id="job-pickup" type="text" placeholder="Pickup location" class="flex-1 bg-slate-50 border border-gray-100 p-4 rounded-2xl text-sm"><input id="job-dest" type="text" placeholder="Destination" class="flex-1 bg-slate-50 border border-gray-100 p-4 rounded-2xl text-sm"></div>
                    <input id="job-price" type="number" placeholder="Your offer ($)" min="1" step="0.01" class="w-full bg-slate-50 border border-gray-100 p-4 rounded-2xl text-sm">
                </div>
            </div>
            <button onclick="postJob()" class="clickable w-full bg-[#0A5C36] py-5 rounded-[30px] text-white font-black text-lg shadow-xl">Post Job</button>
        </div>
    </div>`,

    courier: `<div class="screen bg-[#f8fafc] text-[#0f172a] flex flex-col">
        <header class="bg-white p-6 pt-12 border-b border-gray-100 flex items-center gap-4 shadow-sm"><button onclick="navigate('portal')" class="w-10 h-10 bg-slate-50 rounded-full flex items-center justify-center text-gray-400"><i class="fa-solid fa-chevron-left"></i></button><h2 class="text-2xl font-black text-[#F28C28]">Available Jobs</h2></header>
        <div class="p-6 flex-1 overflow-y-auto space-y-3">
            <div class="bg-white p-4 rounded-[22px] border border-gray-100 shadow-sm flex justify-between items-center"><div><p class="font-bold text-sm">50 Bricks — Msasa→Budiriro</p><p class="text-[9px] text-gray-400">12 km • Est. 25 min</p></div><div class="text-right"><p class="font-black text-[#F28C28]">$20</p><button onclick="navigate('chat')" class="mt-2 bg-[#F28C28] text-white px-4 py-2 rounded-xl font-bold text-xs">Bid</button></div></div>
            <div class="bg-white p-4 rounded-[22px] border border-gray-100 shadow-sm flex justify-between items-center"><div><p class="font-bold text-sm">Pharmacy Run — CBD→Mbare</p><p class="text-[9px] text-gray-400">5 km • Est. 12 min</p></div><div class="text-right"><p class="font-black text-[#F28C28]">$8</p><button onclick="navigate('chat')" class="mt-2 bg-[#F28C28] text-white px-4 py-2 rounded-xl font-bold text-xs">Bid</button></div></div>
            <div class="bg-white p-4 rounded-[22px] border border-gray-100 shadow-sm flex justify-between items-center"><div><p class="font-bold text-sm">Groceries — Market→Avondale</p><p class="text-[9px] text-gray-400">6 km • Est. 14 min</p></div><div class="text-right"><p class="font-black text-[#F28C28]">$6</p><button onclick="navigate('chat')" class="mt-2 bg-[#F28C28] text-white px-4 py-2 rounded-xl font-bold text-xs">Bid</button></div></div>
        </div>
    </div>`,

    chat: `<div class="screen bg-[#020617] text-white flex flex-col">
        <header class="bg-[#0f172a] p-4 pt-12 border-b border-white/5 flex items-center gap-3"><button onclick="navigate('portal')" class="w-9 h-9 bg-white/5 rounded-full flex items-center justify-center text-white/50"><i class="fa-solid fa-chevron-left"></i></button><div><h2 class="text-sm font-extrabold">T. Makumbe</h2><p class="text-[8px] text-[#deff9a] font-bold uppercase">4.9⭐ • Toyota Hilux</p></div></header>
        <div id="chat-messages" class="flex-1 p-4 overflow-y-auto space-y-2">
            <div class="bg-[#1a1a1c] text-white rounded-2xl p-3 max-w-[78%] ml-auto text-sm">Msasa brickyard in 30 mins?</div>
            <div class="bg-[#0f172a] text-white rounded-2xl p-3 max-w-[78%] text-sm">Yes, Toyota Hilux is ready. Can confirm $15?</div>
        </div>
        <div class="bg-[#0f172a] p-4 border-t border-white/5 flex gap-3"><input id="chat-input" type="text" placeholder="Message or counter-bid..." class="flex-1 bg-white/5 border border-white/10 p-3 rounded-xl text-sm text-white"><button onclick="sendChat()" class="w-12 h-12 bg-[#deff9a] rounded-xl flex items-center justify-center text-[#020617] text-lg"><i class="fa-solid fa-paper-plane"></i></button></div>
    </div>`,

    history: `<div class="screen bg-[#f8fafc] text-[#0f172a] flex flex-col">
        <header class="bg-white p-6 pt-12 border-b border-gray-100 flex items-center gap-4 shadow-sm"><button onclick="navigate('portal')" class="w-10 h-10 bg-slate-50 rounded-full flex items-center justify-center text-gray-400"><i class="fa-solid fa-chevron-left"></i></button><h2 class="text-2xl font-black text-[#0A5C36]">History</h2></header>
        <div class="p-6 flex-1 overflow-y-auto space-y-3">
            <div class="bg-white p-4 rounded-[22px] border border-gray-100 shadow-sm flex justify-between"><div><p class="font-bold text-sm">50 Bricks — Msasa→Budiriro</p><p class="text-[9px] text-gray-400">T. Makumbe • Today</p></div><p class="font-black text-[#0A5C36]">$21.01</p></div>
            <div class="bg-white p-4 rounded-[22px] border border-gray-100 shadow-sm flex justify-between"><div><p class="font-bold text-sm">Pharmacy Run — CBD→Mbare</p><p class="text-[9px] text-gray-400">C. Chipo • Yesterday</p></div><p class="font-black text-[#0A5C36]">$9.36</p></div>
        </div>
    </div>`
};

// Render all screens
const root = document.getElementById('app-root');
Object.entries(screens).forEach(([name, html]) => { root.innerHTML += html; });

// Activate first screen
document.querySelectorAll('.screen')[0].classList.add('active');

function navigate(name) {
    document.querySelectorAll('.screen').forEach(s => s.classList.remove('active'));
    const screens = document.querySelectorAll('.screen');
    const index = Object.keys(screens).indexOf(name);
    if (screens[index]) screens[index].classList.add('active');
}

function postJob() {
    const desc = document.getElementById('job-desc')?.value || '';
    const pickup = document.getElementById('job-pickup')?.value || '';
    const dest = document.getElementById('job-dest')?.value || '';
    const price = document.getElementById('job-price')?.value || '';
    
    fetch('/api/post-job', {
        method: 'POST',
        headers: {'Content-Type':'application/json'},
        body: JSON.stringify({description:desc, pickup, destination:dest, price})
    })
    .then(r => r.json())
    .then(data => {
        alert(data.message || 'Job posted!');
        navigate('portal');
    })
    .catch(() => alert('Job posted (demo mode)'));
}

function sendChat() {
    const input = document.getElementById('chat-input');
    const msg = input?.value?.trim();
    if (!msg) return;
    const chat = document.getElementById('chat-messages');
    chat.innerHTML += '<div class="bg-[#1a1a1c] text-white rounded-2xl p-3 max-w-[78%] ml-auto text-sm">' + msg + '</div>';
    input.value = '';
    chat.scrollTop = chat.scrollHeight;
}

// Auto-navigate after splash
setTimeout(() => navigate('portal'), 3000);
</script>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(ZIMPARCEL_HTML)

@app.route('/api/post-job', methods=['POST'])
def post_job():
    data = request.get_json()
    # In production, save to database
    print(f"New job: {data}")
    return jsonify({'message': 'Job posted successfully!', 'job': data})

@app.route('/api/health')
def health():
    return jsonify({'status': 'ok', 'app': 'ZimParcel', 'timestamp': datetime.now().isoformat()})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)