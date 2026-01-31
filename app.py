from flask import Flask
from Pyfhel import Pyfhel

app = Flask(__name__)

# FHE setup (run once)
HE = Pyfhel()
HE.contextGen(p=65537)
HE.keyGen()

@app.route("/")
def home():
    return """
    <h1>FHE Demo</h1>
    <p>This is a Fully Homomorphic Encryption demo</p>
    <a href="/run">Click here to run encrypted calculation</a>
    """

@app.route("/run")
def run_fhe():
    a = 10
    b = 20

    enc_a = HE.encryptInt(a)
    enc_b = HE.encryptInt(b)

    enc_sum = enc_a + enc_b
    result = HE.decryptInt(enc_sum)

    return f"<h2>Encrypted Result: {result}</h2>"
