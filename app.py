import requests, urllib.parse
from flask import Flask, request
app = Flask(__name__)
def ask_wiki(q):
    try:
        headers={"User-Agent":"HouseAhmedBot/1.0"}
        sr2=requests.get(f"https://en.wikipedia.org/w/api.php?action=opensearch&search={q}&limit=1&format=json",timeout=15,headers=headers).json()
        real_title=sr2[1][0] if len(sr2)>1 and sr2[1] else q
        enc=urllib.parse.quote(real_title.replace(" ","_"))
        r=requests.get(f"https://en.wikipedia.org/api/rest_v1/page/summary/{enc}",timeout=15,headers=headers)
        summary=r.json().get("extract","") if r.status_code==200 else "Not found"
        if not summary or len(summary)<5:
            summary=f"{real_title} - football legend!"
        return summary[:600]
    except Exception as e:
        return f"Try: ruud gullit, luka modric"
@app.route("/")
def home():
    q=request.args.get("q","messi")
    ans=ask_wiki(q)
    return f"<h1>House Ahmed Bot</h1><p><b>You:</b> {q}</p><p><b>Bot:</b> {ans}</p><form><input name='q' placeholder='ask player'><button>Ask</button></form>"
if __name__=="__main__":
    app.run(host="0.0.0.0",port=10000)
