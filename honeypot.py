from flask import Flask, request, render_template_string
import sqlite3
import datetime

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('honeypot.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS attempts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            ip TEXT,
            username TEXT,
            password TEXT,
            user_agent TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

login_html = """
<!DOCTYPE html>
<html>
<head>
    <title>Fake Login - Honeypot</title>
    <style>
        body {
            height: 100vh;
            margin: 0;
            font-family: 'Segoe UI', Verdana, Geneva, Tahoma, sans-serif;
            background: linear-gradient(120deg, #a1c4fd 0%, #c2e9fb 100%);
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .login-box {
            background: linear-gradient(120deg, #fbc2eb 0%, #a6c1ee 100%);
            border-radius: 15px;
            box-shadow: 0 6px 18px rgba(0,0,0,0.15);
            padding: 40px 30px;
            width: 340px;
        }
        .login-box h2 {
            text-align: center;
            margin-bottom: 30px;
            color: #3963ab;
            letter-spacing: 1px;
        }
        .login-box input[type="text"],
        .login-box input[type="password"] {
            width: 100%;
            padding: 10px;
            margin: 10px 0 20px 0;
            border: none;
            border-radius: 8px;
            background: #e3eafc;
            font-size: 16px;
            box-sizing: border-box;
            outline: none;
        }
        .login-box input[type="submit"] {
            width: 100%;
            padding: 12px;
            border: none;
            border-radius: 8px;
            background: linear-gradient(120deg, #89f7fe 0%, #66a6ff 100%);
            color: #fff;
            font-size: 18px;
            font-weight: bold;
            cursor: pointer;
            transition: background 0.3s;
        }
        .login-box input[type="submit"]:hover {
            background: linear-gradient(120deg, #66a6ff 0%, #89f7fe 100%);
        }
        .footer {
            text-align: center;
            margin-top: 15px;
            font-size: 13px;
            color: #888;
        }
    </style>
</head>
<body>
    <div class="login-box">
        <h2>Member Login</h2>
        <form method="POST">
            <input name="username" type="text" placeholder="Username" required>
            <input name="password" type="password" placeholder="Password" required>
            <input type="submit" value="Sign In">
        </form>
        <div class="footer">© 2025 Secure Portal</div>
    </div>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        ip = request.remote_addr
        username = request.form.get('username', 'sbmp')
        password = request.form.get('password', 'pass123')
        user_agent = request.headers.get('User-Agent', '')
        timestamp = datetime.datetime.now().isoformat()

        conn = sqlite3.connect('honeypot.db')
        c = conn.cursor()
        c.execute('''
            INSERT INTO attempts (timestamp, ip, username, password, user_agent)
            VALUES (?, ?, ?, ?, ?)
        ''', (timestamp, ip, username, password, user_agent))
        conn.commit()
        conn.close()

        if username.lower() in ['admin', 'root', 'test'] or len(password) > 8:
            print(f"ALERT: Possible attack from {ip} with username '{username}'.")

        return render_template_string("""
        <html>
            <head>
                <title>Login Failed</title>
                <style>
                    body {
                        height: 100vh;
                        margin: 0;
                        font-family: 'Segoe UI', Verdana, Geneva, Tahoma, sans-serif;
                        background: linear-gradient(120deg, #f85032 0%, #e73827 100%);
                        display: flex;
                        align-items: center;
                        justify-content: center;
                    }
                    .result-box {
                        background: #fff;
                        color: #e73827;
                        padding: 30px;
                        border-radius: 15px;
                        box-shadow: 0 4px 12px rgba(0,0,0,0.10);
                        text-align: center;
                        font-size: 20px;
                    }
                    .back-link {
                        margin-top: 20px;
                        display: block;
                        color: #3963ab;
                        text-decoration: underline;
                        font-size: 15px;
                    }
                </style>
            </head>
            <body>
                <div class="result-box">
                    Invalid credentials.
                    <br>
                    <a href="/" class="back-link">← Back to login</a>
                </div>
            </body>
        </html>
        """)
    return render_template_string(login_html)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)