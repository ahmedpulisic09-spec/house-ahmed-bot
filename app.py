import os, requests
from flask import Flask, request
app = Flask(__name__)
VERIFY_TOKEN = os.environ.get("VERIFY_TOKEN", "ahmed123")
def search_wiki_title(q):
    try:
        headers = {'User-Agent': 'HouseAhmedBot/4.0'}
        url = f"https://en.wikipedia.org/w/api.php?action=opensearch&search={q}&limit=1&namespace=0&format=json"
        r = requests.get(url, headers=headers, timeout=10)
        data = r.json()
        return data[1][0] if data[1] else q
    except:
        return q
def get_player(q):
    if not q: return None
    try:
        real_title = search_wiki_title(q)
        headers = {'User-Agent': 'HouseAhmedBot/4.0'}
        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{real_title}"
        r = requests.get(url, headers=headers, timeout=10)
        if r.status_code != 200:
            return None
        data = r.json()
        return {'title': data.get('title',''),'extract': data.get('extract','')[:500],'img': data.get('thumbnail',{}).get('source') or data.get('originalimage',{}).get('source'),'url': data.get('content_urls',{}).get('desktop',{}).get('page','')}
    except:
        return None
@app.route('/')
def home():
    q = request.args.get('q','').strip()
    player = get_player(q) if q else None
    yt_search = f"https://www.youtube.com/results?search_query={player['title']}+highlights" if player else ""
    html = f"""<html><head><meta name="viewport" content="width=device-width, initial-scale=1"><style>body{{font-family:Arial;background:#0f172a;color:white;text-align:center;padding:20px}}input{{padding:12px;width:65%;max-width:300px;border-radius:10px;border:none}}button{{padding:12px 18px;border-radius:10px;border:none;background:#38bdf8;font-weight:bold}}.card{{background:white;color:black;max-width:520px;margin:20px auto;padding:20px;border-radius:20px}}img{{max-width:220px;border-radius:15px}}.btn{{display:inline-block;margin:8px;padding:10px 18px;border-radius:10px;text-decoration:none;font-weight:bold;color:white}}.wa{{background:#25D366}} .yt{{background:#ff0000}} .voice{{background:#8b5cf6}}</style></head><body><h1>⚽ House Ahmed Bot V4</h1><p>Voice + Video + WhatsApp!</p><form><input name="q" placeholder="messi, ronaldo, van dijk" value="{q}"><button>Ask</button></form>"""
    if player:
        img_tag = f'<img src="{player["img"]}"><br>' if player['img'] else ''
        voice_js = f"speechSynthesis.speak(new SpeechSynthesisUtterance(`{player['title']}. {player['extract']}`))"
        html += f"""<div class="card"><h2>{player['title']}</h2>{img_tag}<p>{player['extract']}</p><a class="btn voice" href="#" onclick='{voice_js};return false'>🔊 Play Voice</a><a class="btn yt" href="{yt_search}" target="_blank">🎥 Watch Videos</a><br><a class="btn wa" href="https://wa.me/?text=Check {player['title']}: {player['url']}" target="_blank">Share on WhatsApp</a><br><br><iframe width="100%" height="250" src="https://www.youtube.com/embed?listType=search&list={player['title']}+highlights" frameborder="0" allowfullscreen></iframe></div>"""
    html += '<p>V4 by Ahmed 🔥 | Voice + Video + WhatsApp</p></body></html>'
    return html
@app.route('/whatsapp', methods=['GET','POST'])
def whatsapp():
    if request.method == 'GET':
        mode = request.args.get('hub.mode'); token = request.args.get('hub.verify_token'); challenge = request.args.get('hub.challenge')
        if mode == 'subscribe' and token == VERIFY_TOKEN:
            return challenge, 200
        return "Verification failed", 403
    return "OK", 200
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000)); app.run(host='0.0.0.0', port=port)
