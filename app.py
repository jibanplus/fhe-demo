from flask import Flask, request
import hashlib

app = Flask(__name__)

# --- Simulated Encryption ---
def encrypt(value):
    return hashlib.sha256(str(value).encode()).hexdigest()

@app.route("/", methods=["GET", "POST"])
def home():
    result_html = ""

    if request.method == "POST":
        a = request.form.get("a")
        b = request.form.get("b")

        if a and b:
            a = int(a)
            b = int(b)

            enc_a = encrypt(a)
            enc_b = encrypt(b)
            result = a + b  # simulated final output

            result_html = f"""
            <div class="result">
                <p><b>Encrypted A:</b> {enc_a[:20]}...</p>
                <p><b>Encrypted B:</b> {enc_b[:20]}...</p>
                <h3>Final Result (after decryption): {result}</h3>
            </div>
            """

    return f"""
    <html>
    <head>
        <title>FHE Concept Demo</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background: #0f0f0f;
                color: #ffffff;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
            }}
            .box {{
                background: #1c1c1c;
                padding: 30px;
                border-radius: 10px;
                width: 350px;
                text-align: center;
            }}
            input {{
                width: 90%;
                padding: 10px;
                margin: 8px 0;
                border-radius: 5px;
                border: none;
            }}
            button {{
                padding: 10px 20px;
                border: none;
                border-radius: 5px;
                background: #6c63ff;
                color: white;
                font-size: 16px;
                cursor: pointer;
            }}
            button:hover {{
                background: #5848e5;
            }}
            .result {{
                margin-top: 20px;
                background: #111;
                padding: 15px;
                border-radius: 8px;
            }}
            .footer {{
                margin-top: 15px;
                font-size: 12px;
                opacity: 0.7;
            }}
        </style>
    </head>

    <body>
        <div class="box">
            <h2>FHE Concept Demo</h2>
            <p>Compute on encrypted data (simulated)</p>

            <form method="POST">
                <input type="number" name="a" placeholder="Enter first number" required />
                <input type="number" name="b" placeholder="Enter second number" required />
                <br><br>
                <button type="submit">Run Encrypted Compute</button>
            </form>

            {result_html}

            <div class="footer">
                Powered by <b>Jiban</b>
            </div>
        </div>
    </body>
    </html>
    """
