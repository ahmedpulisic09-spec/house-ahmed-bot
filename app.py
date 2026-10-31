import os
import requests
from flask import Flask, request

app = Flask(__name__)

def get_player(q):
    if not q:
        return None
    try:
        # Get summary + image from Wikipedia
        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{q}"
        r = requests.get(url, timeout=5)
        data = r.json()
        title = data.get('title','')
        extract = data.get('extract','Player not found, try another name!')
        img = data.get('thumbnail',{}).get('source') or data.get('originalimage',{}).get('source')
        return {'title': title, 'extract': extract, 'img': img}
    except:
        return {'title': q, 'extract': 'Error fetching data', 'img': None}

@app.route('/')
def home():
    q = request.args.get('q','').strip()
    player = get_player(q) if q else None

    html = f"""
    <html>
    <head>
        <title>House Ahmed Bot</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body{{font-family:Arial;background:#0f172a;color:white;text-align:center;padding:20px}}
            input{{padding:12px;width:70%;max-width:300px;border-radius:10px;border:none}}
            button{{padding:12px 20px;border-radius:10px;border:none;background:#38bdf8;font-weight:bold;margin-left:5px}}
            .card{{background:white;color:black;max-width:500px;margin:20px auto;padding:20px;border-radius:20px;box-shadow:0 10px 30px rgba(0,0,0,0.5)}}
            img{{max-width:200px;border-radius:15px;margin-top:10px}}
            a{{color:#38bdf8;text-decoration:none}}
        </style>
    </head>
    <body>
        <h1>⚽ House Ahmed Bot</h1>
        <p>Ask any football player!</p>
        <form method="GET">
            <input name="q" placeholder="Type: messi, ronaldo, modric..." value="{q}">
            <button type="submit">Ask</button>
        </form>
    """

    if player:
        html += f"""
        <div class="card">
            <h2>{player['title']}</h2>
            {f'<img src="{player["img"]}">' if player['img'] else ''}
            <p>{player['extract']}</p>
        </div>
        """

    html += """
        <p style="margin-top:30px;font-size:12px">Built by Ahmed 🔥 | <a href="https://github.com/ahmedpulisic09-spec/house-ahmed-bot">GitHub</a></p>
    </body></html>
    """
    return html

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
