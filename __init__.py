from flask import Flask, session, redirect, render_template, request
import requests, json

appID = ""
appSecret = ""

app = Flask(__name__)

@app.route('/')
def index():
    return """This is a demo for Alles Identity in Flask<br><a href="/auth">Signin here</a>"""

@app.route('/auth')
def auth():
    req = requests.post("https://identity.alles.cx/a/v1/flow", data={"callback":"https://allesidentity.chaosgb.co.uk/callback"}, auth=(appID,appSecret))
    token = json.loads(req.text)["token"]
    return redirect(f"https://identity.alles.cx/login?flow={token}")

@app.route('/callback', defaults={"code": None})
@app.route('/callback/<code>')
def callback(code):
    code = request.args.get('code')
    if not code:
        return "The code was not specified"
    req = requests.get(f"https://identity.alles.cx/a/v1/profile?code={code}", auth=(appID,appSecret))
    data = json.loads(req.text)
    return render_template("data.html", data=data)

if __name__=='__main__':
    app.run()
        
