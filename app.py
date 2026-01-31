from flask import Flask
import hashlib

app = Flask(__name__)

# --- Fake Encryption (Simulation) ---
def encrypt(value):
    return hashlib.sha256(str(value).encode()).hexdigest()

def decrypt_simulated(enc_a, enc_b):
    # In real FHE, server never decrypts
    # Here we simulate correct output
    return enc_a + enc_b

@app.route("/")
def home():
    return """
    <h1>FHE Concept Demo</h1>
    <p>Server computes on encrypted data without seeing raw values.</p>
    <a href="/run">Run Encrypted Calculation</a>
    """

@app.route("/run")
def run_demo():
    a = 10
    b = 20

    enc_a = encrypt(a)
    enc_b = encrypt(b)

    result = a + b  # simulated final output

    return f"""
    <h3>Encrypted A: {enc_a[:16]}...</h3>
    <h3>Encrypted B: {enc_b[:16]}...</h3>
    <h2>Final Result (after decryption): {result}</h2>
    """

