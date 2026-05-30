from flask import Flask, request, jsonify, render_template_string, session, redirect
import requests
import functools

app = Flask(__name__)
app.secret_key = 'bronx-king'

# ============================================
# 👥 30 USERS WITH PERMISSIONS
# ============================================
USERS = {
    "bronx": {"pass": "ultra2026", "perms": ["number", "vehicle", "telegram", "aadhar", "mail"], "name": "👑 BRONX"},
    "admin": {"pass": "admin123", "perms": ["number", "vehicle", "telegram", "aadhar", "mail"], "name": "Admin"},
    "john": {"pass": "john123", "perms": ["number", "vehicle"], "name": "John"},
    "mike": {"pass": "mike123", "perms": ["number", "mail"], "name": "Mike"},
    "sarah": {"pass": "sarah123", "perms": ["number", "telegram"], "name": "Sarah"},
    "david": {"pass": "david123", "perms": ["number"], "name": "David"},
    "emma": {"pass": "emma123", "perms": ["vehicle", "mail"], "name": "Emma"},
    "alex": {"pass": "alex123", "perms": ["number", "aadhar"], "name": "Alex"},
    "lisa": {"pass": "lisa123", "perms": ["telegram", "mail"], "name": "Lisa"},
    "tom": {"pass": "tom123", "perms": ["number", "vehicle", "mail"], "name": "Tom"},
    "jerry": {"pass": "jerry123", "perms": ["number"], "name": "Jerry"},
    "anna": {"pass": "anna123", "perms": ["vehicle", "aadhar"], "name": "Anna"},
    "peter": {"pass": "peter123", "perms": ["number", "telegram"], "name": "Peter"},
    "rose": {"pass": "rose123", "perms": ["mail"], "name": "Rose"},
    "jack": {"pass": "jack123", "perms": ["number", "vehicle", "aadhar"], "name": "Jack"},
    "lucy": {"pass": "lucy123", "perms": ["telegram"], "name": "Lucy"},
    "mark": {"pass": "mark123", "perms": ["number", "mail", "aadhar"], "name": "Mark"},
    "nina": {"pass": "nina123", "perms": ["vehicle"], "name": "Nina"},
    "paul": {"pass": "paul123", "perms": ["number", "telegram", "mail"], "name": "Paul"},
    "jane": {"pass": "jane123", "perms": ["number"], "name": "Jane"},
    "bob": {"pass": "bob123", "perms": ["vehicle", "mail"], "name": "Bob"},
    "lily": {"pass": "lily123", "perms": ["telegram", "aadhar"], "name": "Lily"},
    "sam": {"pass": "sam123", "perms": ["number", "vehicle"], "name": "Sam"},
    "mia": {"pass": "mia123", "perms": ["mail", "aadhar"], "name": "Mia"},
    "joe": {"pass": "joe123", "perms": ["number"], "name": "Joe"},
    "ava": {"pass": "ava123", "perms": ["telegram"], "name": "Ava"},
    "ben": {"pass": "ben123", "perms": ["vehicle", "aadhar", "mail"], "name": "Ben"},
    "zoe": {"pass": "zoe123", "perms": ["number", "telegram"], "name": "Zoe"},
    "max": {"pass": "max123", "perms": ["number", "vehicle", "telegram", "mail"], "name": "Max"},
    "kia": {"pass": "kia123", "perms": ["aadhar"], "name": "Kia"},
}

# ============================================
# API ENDPOINTS (Tumhari APIs yahan daalna)
# ============================================
API_ENDPOINTS = {
    "number": "https://osint-api-website-bronx.vercel.app/api/key-bronx/number?key=op&num=",      # 👈 APNI API DAALO
    "vehicle": "https://osint-api-website-bronx.vercel.app/api/key-bronx/rc?key=op&owner=",     # 👈 APNI API DAALO
    "telegram": "https://your-telegram-api.com/api?user=", # 👈 APNI API DAALO
    "aadhar": "https://osint-api-website-bronx.vercel.app/api/key-bronx/aadhar?key=op&num=",      # 👈 APNI API DAALO
    "mail": "https://osint-api-website-bronx.vercel.app/api/custom/email-lookup?key=op&mail=",        # 👈 APNI API DAALO
}

# ============================================
# LOGIN REQUIRED DECORATOR
# ============================================
def login_required(f):
    @functools.wraps(f)
    def decorated(*args, **kwargs):
        if 'user' not in session:
            return redirect('/')
        return f(*args, **kwargs)
    return decorated

# ============================================
# CLEAN RESPONSE - Hide Developer Names
# ============================================
def clean_response(data):
    """Remove unwanted fields and add BRONX branding"""
    if isinstance(data, dict):
        # Remove competitor branding
        for key in ['developer', 'by', 'credit', 'owner', 'channel', 'api_by', 'API BY', 
                     'powered_by', 'api_developer', 'API DEVELOPER', 'source']:
            data.pop(key, None)
        # Add BRONX branding
        data['developer'] = '@BRONX_ULTRA'
        data['powered_by'] = 'BRONX OSINT'
    return data

# ============================================
# CALL API
# ============================================
def call_api(api_type, query):
    """Call external API and return cleaned response"""
    url = API_ENDPOINTS.get(api_type, '')
    if not url:
        return {"error": "API not configured", "developer": "@BRONX_ULTRA"}
    
    try:
        resp = requests.get(f"{url}{query}", timeout=15, headers={
            'User-Agent': 'Mozilla/5.0'
        })
        data = resp.json()
        return clean_response(data)
    except Exception as e:
        return {"error": str(e), "developer": "@BRONX_ULTRA"}

# ============================================
# HTML TEMPLATES
# ============================================
LOGIN_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>BRONX ULTRA OSINT</title>
    <style>
        :root {
            --primary: #0066ff;
            --primary-dark: #0044cc;
            --bg: #f0f4ff;
            --card: #ffffff;
            --text: #1a1a2e;
            --sub: #666;
            --glow: rgba(0,102,255,0.3);
        }
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            background: linear-gradient(135deg, #f0f4ff 0%, #e8f0ff 50%, #dce8ff 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            font-family: 'Segoe UI', system-ui, sans-serif;
        }
        .login-box {
            background: var(--card);
            padding: 45px 40px;
            border-radius: 20px;
            width: 400px;
            box-shadow: 0 10px 50px rgba(0,102,255,0.15), 0 0 80px var(--glow);
            text-align: center;
            animation: fadeIn 0.5s ease;
        }
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(-20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .logo {
            width: 70px;
            height: 70px;
            background: linear-gradient(135deg, var(--primary), var(--primary-dark));
            border-radius: 20px;
            margin: 0 auto 20px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 35px;
            color: #fff;
            box-shadow: 0 5px 30px var(--glow);
        }
        h1 {
            color: var(--text);
            font-size: 1.6em;
            margin-bottom: 5px;
            font-weight: 700;
        }
        .subtitle {
            color: var(--sub);
            font-size: 0.8em;
            margin-bottom: 25px;
            letter-spacing: 1px;
        }
        .input-group {
            margin-bottom: 15px;
            text-align: left;
        }
        .input-group label {
            display: block;
            color: var(--sub);
            font-size: 0.7em;
            text-transform: uppercase;
            letter-spacing: 2px;
            margin-bottom: 6px;
            font-weight: 600;
        }
        .input-group input {
            width: 100%;
            padding: 14px 16px;
            border: 2px solid #e0e8ff;
            border-radius: 12px;
            font-size: 15px;
            transition: 0.3s;
            background: #f8faff;
            color: var(--text);
        }
        .input-group input:focus {
            border-color: var(--primary);
            box-shadow: 0 0 20px var(--glow);
            outline: none;
            background: #fff;
        }
        .btn {
            width: 100%;
            padding: 15px;
            background: linear-gradient(135deg, var(--primary), var(--primary-dark));
            color: #fff;
            border: none;
            border-radius: 12px;
            font-size: 16px;
            font-weight: 700;
            cursor: pointer;
            letter-spacing: 1px;
            margin-top: 10px;
            transition: 0.3s;
            box-shadow: 0 5px 25px var(--glow);
        }
        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 40px rgba(0,102,255,0.4);
        }
        .error {
            color: #ff4444;
            font-size: 0.8em;
            margin-top: 10px;
        }
    </style>
</head>
<body>
    <div class="login-box">
        <div class="logo">🔍</div>
        <h1>BRONX ULTRA OSINT</h1>
        <p class="subtitle">Professional Intelligence Platform</p>
        <form method="post">
            <div class="input-group">
                <label>Username</label>
                <input type="text" name="user" placeholder="Enter username" required>
            </div>
            <div class="input-group">
                <label>Password</label>
                <input type="password" name="pass" placeholder="Enter password" required>
            </div>
            <button class="btn" type="submit">🔐 ACCESS SYSTEM</button>
        </form>
        {% if error %}<p class="error">{{ error }}</p>{% endif %}
    </div>
</body>
</html>
"""

DASHBOARD = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>BRONX OSINT Dashboard</title>
    <style>
        :root {
            --primary: #0066ff;
            --primary-dark: #0044cc;
            --bg: #f0f4ff;
            --card: #ffffff;
            --text: #1a1a2e;
            --sub: #666;
            --glow: rgba(0,102,255,0.3);
            --success: #00cc66;
            --danger: #ff4444;
        }
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            background: linear-gradient(135deg, #f0f4ff 0%, #e8f0ff 50%, #dce8ff 100%);
            min-height: 100vh;
            font-family: 'Segoe UI', system-ui, sans-serif;
            padding: 20px;
        }
        .container { max-width: 1200px; margin: 0 auto; }
        
        /* Header */
        .header {
            background: var(--card);
            border-radius: 20px;
            padding: 25px 30px;
            margin-bottom: 25px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            box-shadow: 0 5px 30px rgba(0,102,255,0.1);
            flex-wrap: wrap;
            gap: 15px;
        }
        .header h1 {
            color: var(--primary);
            font-size: 1.6em;
            font-weight: 700;
        }
        .header .user-info {
            display: flex;
            align-items: center;
            gap: 15px;
        }
        .header .badge {
            background: var(--primary);
            color: #fff;
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 0.8em;
            font-weight: 600;
        }
        .header .btn-logout {
            background: var(--danger);
            color: #fff;
            padding: 8px 20px;
            border-radius: 10px;
            text-decoration: none;
            font-size: 0.8em;
            font-weight: 600;
            transition: 0.3s;
        }
        .header .btn-logout:hover {
            box-shadow: 0 5px 20px rgba(255,68,68,0.3);
        }
        
        /* Stats */
        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-bottom: 25px;
        }
        .stat-card {
            background: var(--card);
            border-radius: 15px;
            padding: 20px;
            text-align: center;
            box-shadow: 0 3px 20px rgba(0,102,255,0.08);
            transition: 0.3s;
        }
        .stat-card:hover {
            transform: translateY(-3px);
            box-shadow: 0 10px 40px rgba(0,102,255,0.15);
        }
        .stat-card .icon {
            font-size: 2em;
            margin-bottom: 8px;
        }
        .stat-card .label {
            color: var(--sub);
            font-size: 0.75em;
            text-transform: uppercase;
            letter-spacing: 2px;
        }
        .stat-card .value {
            color: var(--primary);
            font-size: 1.8em;
            font-weight: 700;
        }
        
        /* Tools Grid */
        .tools-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
        }
        .tool-card {
            background: var(--card);
            border-radius: 18px;
            padding: 25px;
            box-shadow: 0 5px 25px rgba(0,102,255,0.08);
            transition: 0.3s;
        }
        .tool-card:hover {
            box-shadow: 0 10px 50px rgba(0,102,255,0.2);
            transform: translateY(-2px);
        }
        .tool-card.locked {
            opacity: 0.5;
            pointer-events: none;
            position: relative;
        }
        .tool-card.locked::after {
            content: '🔒 NO ACCESS';
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: rgba(0,0,0,0.8);
            color: #fff;
            padding: 10px 25px;
            border-radius: 25px;
            font-weight: 700;
            font-size: 0.9em;
        }
        .tool-icon {
            font-size: 2.5em;
            margin-bottom: 10px;
        }
        .tool-card h3 {
            color: var(--text);
            margin-bottom: 5px;
            font-size: 1.1em;
        }
        .tool-card p {
            color: var(--sub);
            font-size: 0.8em;
            margin-bottom: 15px;
        }
        .tool-card input {
            width: 100%;
            padding: 12px 15px;
            border: 2px solid #e0e8ff;
            border-radius: 10px;
            font-size: 14px;
            margin-bottom: 10px;
            background: #f8faff;
            transition: 0.3s;
        }
        .tool-card input:focus {
            border-color: var(--primary);
            box-shadow: 0 0 15px var(--glow);
            outline: none;
        }
        .btn-search {
            width: 100%;
            padding: 12px;
            background: linear-gradient(135deg, var(--primary), var(--primary-dark));
            color: #fff;
            border: none;
            border-radius: 10px;
            font-weight: 600;
            cursor: pointer;
            font-size: 0.85em;
            letter-spacing: 1px;
            transition: 0.3s;
            box-shadow: 0 5px 20px var(--glow);
        }
        .btn-search:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 35px rgba(0,102,255,0.4);
        }
        
        /* Result */
        .result {
            background: #f8faff;
            border: 1px solid #e0e8ff;
            border-radius: 10px;
            padding: 15px;
            margin-top: 12px;
            max-height: 300px;
            overflow: auto;
            font-size: 0.8em;
            display: none;
            color: var(--text);
            font-family: 'SF Mono', monospace;
            white-space: pre-wrap;
            word-break: break-all;
        }
        
        .footer {
            text-align: center;
            margin-top: 30px;
            color: var(--sub);
            font-size: 0.75em;
            letter-spacing: 2px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div>
                <h1>🔍 BRONX ULTRA OSINT</h1>
                <span style="color: var(--sub); font-size: 0.7em; letter-spacing: 2px;">PROFESSIONAL INTELLIGENCE PLATFORM</span>
            </div>
            <div class="user-info">
                <span class="badge">👤 {{ user_name }}</span>
                <a href="/logout" class="btn-logout">LOGOUT</a>
            </div>
        </div>
        
        <div class="stats">
            <div class="stat-card">
                <div class="icon">📱</div>
                <div class="label">Number Info</div>
                <div class="value">{{ '✅' if 'number' in perms else '❌' }}</div>
            </div>
            <div class="stat-card">
                <div class="icon">🚗</div>
                <div class="label">Vehicle Info</div>
                <div class="value">{{ '✅' if 'vehicle' in perms else '❌' }}</div>
            </div>
            <div class="stat-card">
                <div class="icon">📲</div>
                <div class="label">Telegram Info</div>
                <div class="value">{{ '✅' if 'telegram' in perms else '❌' }}</div>
            </div>
            <div class="stat-card">
                <div class="icon">🆔</div>
                <div class="label">Aadhar Info</div>
                <div class="value">{{ '✅' if 'aadhar' in perms else '❌' }}</div>
            </div>
            <div class="stat-card">
                <div class="icon">📧</div>
                <div class="label">Mail Info</div>
                <div class="value">{{ '✅' if 'mail' in perms else '❌' }}</div>
            </div>
        </div>
        
        <div class="tools-grid">
            <!-- Number Info -->
            <div class="tool-card {{ 'locked' if 'number' not in perms else '' }}">
                <div class="tool-icon">📱</div>
                <h3>Number Lookup</h3>
                <p>Get complete mobile number details</p>
                <input type="text" id="numberInput" placeholder="Enter phone number">
                <button class="btn-search" onclick="lookup('number')">🔍 SEARCH</button>
                <pre class="result" id="numberResult"></pre>
            </div>
            
            <!-- Vehicle Info -->
            <div class="tool-card {{ 'locked' if 'vehicle' not in perms else '' }}">
                <div class="tool-icon">🚗</div>
                <h3>Vehicle RC Lookup</h3>
                <p>Get vehicle registration details</p>
                <input type="text" id="vehicleInput" placeholder="Enter RC number">
                <button class="btn-search" onclick="lookup('vehicle')">🔍 SEARCH</button>
                <pre class="result" id="vehicleResult"></pre>
            </div>
            
            <!-- Telegram Info -->
            <div class="tool-card {{ 'locked' if 'telegram' not in perms else '' }}">
                <div class="tool-icon">📲</div>
                <h3>Telegram Lookup</h3>
                <p>Get Telegram user info from username</p>
                <input type="text" id="telegramInput" placeholder="Enter @username or ID">
                <button class="btn-search" onclick="lookup('telegram')">🔍 SEARCH</button>
                <pre class="result" id="telegramResult"></pre>
            </div>
            
            <!-- Aadhar Info -->
            <div class="tool-card {{ 'locked' if 'aadhar' not in perms else '' }}">
                <div class="tool-icon">🆔</div>
                <h3>Aadhar Lookup</h3>
                <p>Get Aadhar card information</p>
                <input type="text" id="aadharInput" placeholder="Enter Aadhar number">
                <button class="btn-search" onclick="lookup('aadhar')">🔍 SEARCH</button>
                <pre class="result" id="aadharResult"></pre>
            </div>
            
            <!-- Mail Info -->
            <div class="tool-card {{ 'locked' if 'mail' not in perms else '' }}">
                <div class="tool-icon">📧</div>
                <h3>Email Lookup</h3>
                <p>Get email address information</p>
                <input type="text" id="mailInput" placeholder="Enter email address">
                <button class="btn-search" onclick="lookup('mail')">🔍 SEARCH</button>
                <pre class="result" id="mailResult"></pre>
            </div>
        </div>
        
        <div class="footer">🔒 @BRONX_ULTRA | Professional OSINT Platform</div>
    </div>
    
    <script>
        async function lookup(type) {
            const inputMap = {
                'number': 'numberInput',
                'vehicle': 'vehicleInput',
                'telegram': 'telegramInput',
                'aadhar': 'aadharInput',
                'mail': 'mailInput'
            };
            
            const resultMap = {
                'number': 'numberResult',
                'vehicle': 'vehicleResult',
                'telegram': 'telegramResult',
                'aadhar': 'aadharResult',
                'mail': 'mailResult'
            };
            
            const query = document.getElementById(inputMap[type]).value.trim();
            const resultDiv = document.getElementById(resultMap[type]);
            
            if (!query) {
                resultDiv.style.display = 'block';
                resultDiv.textContent = '❌ Please enter a value';
                resultDiv.style.color = '#ff4444';
                return;
            }
            
            resultDiv.style.display = 'block';
            resultDiv.textContent = '⏳ Searching...';
            resultDiv.style.color = '#0066ff';
            
            try {
                const resp = await fetch(`/api/${type}?q=${encodeURIComponent(query)}`);
                const data = await resp.json();
                resultDiv.textContent = JSON.stringify(data, null, 2);
                resultDiv.style.color = '#1a1a2e';
            } catch (e) {
                resultDiv.textContent = '❌ Error: ' + e.message;
                resultDiv.style.color = '#ff4444';
            }
        }
    </script>
</body>
</html>
"""

# ============================================
# ROUTES
# ============================================
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form.get('user', '').strip()
        pwd = request.form.get('pass', '').strip()
        
        if user in USERS and USERS[user]['pass'] == pwd:
            session['user'] = user
            return redirect('/dashboard')
        
        return render_template_string(LOGIN_PAGE, error='❌ Invalid username or password')
    
    return render_template_string(LOGIN_PAGE, error=None)

@app.route('/dashboard')
@login_required
def dashboard():
    user = session['user']
    user_data = USERS[user]
    return render_template_string(
        DASHBOARD,
        user_name=user_data['name'],
        perms=user_data['perms']
    )

@app.route('/api/<api_type>')
@login_required
def api_handler(api_type):
    user = session['user']
    user_perms = USERS[user]['perms']
    
    # Check permission
    if api_type not in user_perms:
        return jsonify({
            "error": "❌ Access Denied! You don't have permission for this tool.",
            "developer": "@BRONX_ULTRA"
        }), 403
    
    query = request.args.get('q', '').strip()
    if not query:
        return jsonify({"error": "Missing query parameter", "developer": "@BRONX_ULTRA"}), 400
    
    # Call external API
    result = call_api(api_type, query)
    return jsonify(result)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

# ============================================
# MAIN
# ============================================
if __name__ == "__main__":
    import os as _os
    port = int(_os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
