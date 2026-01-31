from flask import Flask, request
import hashlib, random, time

app = Flask(__name__)

# ---------- helpers ----------
def encrypt(val):
    return hashlib.sha256(str(val).encode()).hexdigest()

# ---------- main ----------
@app.route("/", methods=["GET", "POST"])
def home():
    mode = "calc"
    theme = "dark"
    show_steps = True

    a = b = ""
    result = ""
    steps = ""
    extra = ""

    if request.method == "POST":
        mode = request.form.get("mode", "calc")
        theme = request.form.get("theme", "dark")
        show_steps = request.form.get("show") == "on"

        # ---------- CALCULATOR ----------
        if mode == "calc":
            a = request.form.get("a", "")
            b = request.form.get("b", "")
            op = request.form.get("op")

            if a and b:
                a_i = int(a)
                b_i = int(b)

                enc_a = encrypt(a_i)
                enc_b = encrypt(b_i)

                if op == "add":
                    result = a_i + b_i
                    op_text = "Addition"
                elif op == "mul":
                    result = a_i * b_i
                    op_text = "Multiplication"
                else:
                    result = "A > B" if a_i > b_i else "A ≤ B"
                    op_text = "Comparison"

                if show_steps:
                    steps = f"""
                    <div class="steps">
                        <p><b>Encrypted A:</b> {enc_a[:18]}...</p>
                        <p><b>Encrypted B:</b> {enc_b[:18]}...</p>
                        <p><b>Operation:</b> {op_text}</p>
                    </div>
                    """

        # ---------- VOTING ----------
        if mode == "vote":
            votes = request.form.getlist("vote")
            encrypted_votes = [encrypt(v) for v in votes]
            yes = votes.count("yes")
            no = votes.count("no")

            result = f"YES: {yes} | NO: {no}"

            if show_steps:
                steps = "<div class='steps'>" + "".join(
                    f"<p>{v[:20]}...</p>" for v in encrypted_votes
                ) + "</div>"

        # ---------- AVERAGE ----------
        if mode == "avg":
            values = request.form.get("values", "")
            nums = [int(x) for x in values.split(",") if x.strip().isdigit()]

            if nums:
                enc_vals = [encrypt(x) for x in nums]
                result = round(sum(nums) / len(nums), 2)

                if show_steps:
                    steps = "<div class='steps'>" + "".join(
                        f"<p>{v[:20]}...</p>" for v in enc_vals
                    ) + "</div>"

    bg = "#0f0f0f" if theme == "dark" else "#f4f4f4"
    fg = "white" if theme == "dark" else "#111"
    box = "#1c1c1c" if theme == "dark" else "#ffffff"

    return f"""
    <html>
    <head>
        <title>FHE Concept Demo</title>
        <style>
            body {{
                background:{bg};
                color:{fg};
                font-family:Arial;
                display:flex;
                justify-content:center;
                align-items:center;
                height:100vh;
            }}
            .box {{
                background:{box};
                padding:30px;
                border-radius:12px;
                width:420px;
                text-align:center;
            }}
            input, select, textarea {{
                width:95%;
                padding:8px;
                margin:6px 0;
            }}
            button {{
                width:100%;
                padding:10px;
                margin-top:8px;
            }}
            .steps {{
                background:#111;
                padding:10px;
                margin-top:10px;
                font-size:13px;
            }}
            .footer {{
                margin-top:12px;
                font-size:12px;
                opacity:0.7;
            }}
        </style>
    </head>

    <body>
        <div class="box">
            <h2>FHE Concept Demo</h2>

            <form method="POST">

                <select name="mode">
                    <option value="calc">Calculator</option>
                    <option value="vote">Voting Demo</option>
                    <option value="avg">Encrypted Average</option>
                </select>

                <select name="theme">
                    <option value="dark">Dark</option>
                    <option value="light">Light</option>
                </select>

                <label>
                    <input type="checkbox" name="show" checked> Show Encryption Steps
                </label>

                <hr>

                <!-- calculator -->
                <input name="a" placeholder="A" value="{a}">
                <input name="b" placeholder="B" value="{b}">
                <select name="op">
                    <option value="add">A + B</option>
                    <option value="mul">A × B</option>
                    <option value="cmp">A > B</option>
                </select>

                <!-- voting -->
                <p>Voting (private)</p>
                <input type="checkbox" name="vote" value="yes"> Yes
                <input type="checkbox" name="vote" value="no"> No

                <!-- average -->
                <textarea name="values" placeholder="Encrypted Average (e.g. 10,20,30)"></textarea>

                <button type="submit">Run Encrypted Compute</button>
            </form>

            <h3>{result}</h3>
            {steps}

            <div class="footer">
                POWERED BY <b>TUB</b>
            </div>
        </div>
    </body>
    </html>
    """
