import os
import requests
from flask import Flask, request
app = Flask(__name__)

def search_wiki_title(q):
    # Smart search: messi -> Lionel Messi
    try:
        headers = {'User-Agent': 'HouseAhmedBot/2.0'}
        url = f"https://en.wikipedia.org/w/api.php?action=opensearch&search={q}&limit=1&namespace=0&format=json"
        r = requests.get(url, headers=headers, timeout=10)
        data = r.json()
        if data[1]:
            return data[1][0]  # Best match
        return q
    except:
        return q

def get_player(q):
    if not q:
        return None
    try:
        # Smart search first
        real_title = search_wiki_title(q)
        headers = {'User-Agent': 'HouseAhmedBot/2.0'}
        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{real_title}"
        r = requests.get(url, headers=headers, timeout=10)
        if r.status_code != 200:
            return {'title': q, 'extract': f'Could not find "{q}". Try full name.', 'img': None, 'url': None}
        data = r.json()
        title = data.get('title','')
        extract = data.get('extract','Not found')
        img = data.get('thumbnail',{}).get('source') or data.get('originalimage',{}).get('source')
        page_url = data.get('content_urls',{}).get('desktop',{}).get('page','')
        return {'title': title, 'extract': extract, 'img': img, 'url': page_url}
    except Exception as e:
        return {'title': q, 'extract': f'Error: {e}', 'img': None, 'url': None}

@app.route('/')
def home():
    q = request.args.get('q','').strip()
    player = get_player(q) if q else None
    wa_text = ""
    if player:
        wa_text = f"⚽ {player['title']} - from House Ahmed Bot: {player['extract'][:100]}... https://house-ahmed-bot.onrender.com/?q={q}"
    
    html = f"""
    <html><head><meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
    body{{font-family:Arial;background:#0f172a;color:white;text-align:center;padding:20px}}
    input{{padding:12px;width:70%;max-width:300px;border-radius:10px;border:none}}
    button{{padding:12px 20px;border-radius:10px;border:none;background:#38bdf8;font-weight:bold;margin-left:5px}}
    .card{{background:white;color:black;max-width:500px;margin:20px auto;padding:20px;border-radius:20px;box-shadow:0 10px 30px rgba(0,0,0,0.5)}}
    img{{max-width:200px;border-radius:15px;margin-top:10px}}
    .wa{{background:#25D366;color:white;padding:12px 20px;border-radius:10px;text-decoration:none;display:inline-block;margin-top:15px;font-weight:bold}}
    .quick{{margin-top:20px}}
    .quick a{{background:#1e293b;color:white;padding:8px 12px;border-radius:20px;text-decoration:none;margin:5px;display:inline-block;font-size:14px}}
    </style></head><body>
    <h1>⚽ House Ahmed Bot V2</h1>
    <p>Ask any football player! Now with smart search!</p>
    <form method="GET">
    <input name="q" placeholder="Type: messi, ronaldo, hakimi..." value="{q}">
    <button>Ask</button>
    </form>
    <div class="quick">
        <a href="/?q=Messi">Messi</a>
        <a href="/?q=Ronaldo">Ronaldo</a>
        <a href="/?q=Hakimi">Hakimi</a>
        <a href="/?q=Ziyech">Ziyech</a>
        <a href="/?q=Bounou">Bounou</a>
    </div>
    """
    if player:
        img_tag = f'<img src="{player["img"]}">' if player['img'] else ''
        wa_link = f"https://wa.me/?text={requests.utils.quote(wa_text)}" if wa_text else "#"
        html += f'<div class="card"><h2>{player["title"]}</h2>{img_tag}<p>{player["extract"]}</p><a class="wa" href="{wa_link}">📱 Share on WhatsApp</a></div>'
    html += '<p style="margin-top:30px;font-size:12px">V2 by Ahmed 🔥 | Smart Search + WhatsApp</p></body></html>'
    return html

# WhatsApp Cloud API Webhook (for real WhatsApp bot later)
@app.route('/whatsapp', methods=['GET', 'POST'])
def whatsapp_webhook():
    if request.method == 'GET':
        return "WhatsApp Webhook Ready! Add this URL to Meta Developers."
    data = request.get_json()
    # You will connect this to Meta WhatsApp API later
    return "OK", 200

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
