import os
import requests
from flask import Flask, request
app = Flask(__name__)

def get_player(q):
    if not q:
        return None
    try:
        headers = {'User-Agent': 'HouseAhmedBot/1.0'}
        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{q}"
        r = requests.get(url, headers=headers, timeout=10)
        if r.status_code != 200:
            return {'title': q, 'extract': f'Could not find "{q}". Try full name like Lionel_Messi', 'img': None}
        data = r.json()
        title = data.get('title','')
        extract = data.get('extract','Not found')
        img = data.get('thumbnail',{}).get('source') or data.get('originalimage',{}).get('source')
        return {'title': title, 'extract': extract, 'img': img}
    except Exception as e:
        return {'title': q, 'extract': f'Error: {e}', 'img': None}

@app.route('/')
def home():
    q = request.args.get('q','').strip()
    player = get_player(q) if q else None
    html = f"""
    <html><head><meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
    body{{font-family:Arial;background:#0f172a;color:white;text-align:center;padding:20px}}
    input{{padding:12px;width:70%;max-width:300px;border-radius:10px;border:none}}
    button{{padding:12px 20px;border-radius:10px;border:none;background:#38bdf8;font-weight:bold;margin-left:5px}}
    .card{{background:white;color:black;max-width:500px;margin:20px auto;padding:20px;border-radius:20px}}
    img{{max-width:200px;border-radius:15px;margin-top:10px}}
    </style></head><body>
    <h1>⚽ House Ahmed Bot</h1>
    <p>Ask any football player!</p>
    <form method="GET">
    <input name="q" placeholder="Type: messi, ronaldo..." value="{q}">
    <button>Ask</button>
    </form>
    """
    if player:
        img_tag = f'<img src="{player["img"]}">' if player['img'] else ''
        html += f'<div class="card"><h2>{player["title"]}</h2>{img_tag}<p>{player["extract"]}</p></div>'
    html += "</body></html>"
    return html

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
