from flask import Flask
from Pyfhel import Pyfhel
import os

app = Flask(__name__)

HE = Pyfhel()
HE.contextGen(p=65537)
HE.keyGen()

@app.route("/")
def home():
    return """
    <h1>FHE Demo</h1>
    <a href="/run">Click to Run Encrypted Calculation</a>
    """

@app.route("/run")
def run():
    a = 15
    b = 25

    enc_a = HE.encryptInt(a)
    enc_b = HE.encryptInt(b)

    enc_sum = enc_a + enc_b
    result = HE.decryptInt(enc_sum)

    return f"<h2>Encrypted Result: {result}</h2>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
