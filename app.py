from flask import Flask, render_template_string

app = Flask(__name__)

with open("index.htm", "r", encoding="utf-8") as f:
    index_html = f.read()

@app.route("/")
def home():
    return render_template_string(index_html)
