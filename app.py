import os, requests
from flask import Flask, request

app = Flask(__name__)

# ====== CONFIG - YOU WILL FILL THESE LATER ======
VERIFY_TOKEN = os.environ.get("VERIFY_TOKEN", "ahmed123")
WHATSAPP_TOKEN = os.environ.get("WHATSAPP_TOKEN", "")
PHONE_NUMBER_ID = os.environ.get("PHONE_NUMBER_ID", "")

def search_wiki_title(q):
    try:
        headers = {'User-Agent': 'HouseAhmedBot/3.0'}
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
        headers = {'User-Agent': 'HouseAhmedBot/3.0'}
        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{real_title}"
        r = requests.get(url, headers=headers, timeout=10)
        if r.status_code != 200:
            return None
        data = r.json()
        return {
            'title': data.get('title',''),
            'extract': data.get('extract','')[:400],
            'img': data.get('thumbnail',{}).get('source') or data.get('originalimage',{}).get('source'),
            'url': data.get('content_urls',{}).get('desktop',{}).get('page','')
        }
    except:
        return None

def send_whatsapp_message(to, text, image_url=None):
    if not WHATSAPP_TOKEN or not PHONE_NUMBER_ID:
        return
    url = f"https://graph.facebook.com/v20.0/{PHONE_NUMBER_ID}/messages"
    headers = {"Authorization": f"Bearer {WHATSAPP_TOKEN}", "Content-Type": "application/json"}
    
    # Send image first if exists
    if image_url:
        data = {
            "messaging_product": "whatsapp",
            "to": to,
            "type": "image",
            "image": {"link": image_url, "caption": text[:1000]}
        }
        requests.post(url, headers=headers, json=data, timeout=10)
    else:
        data = {
            "messaging_product": "whatsapp",
            "to": to,
            "type": "text",
            "text": {"body": text[:1000]}
        }
        requests.post(url, headers=headers, json=data, timeout=10)

@app.route('/')
def home():
    q = request.args.get('q','').strip()
    player = get_player(q) if q else None
    html = f"""
    <html><head><meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
    body{{font-family:Arial;background:#0f172a;color:white;text-align:center;padding:20px}}
    input{{padding:12px;width:70%;max-width:300px;border-radius:10px;border:none}}
    button{{padding:12px 20px;border-radius:10px;border:none;background:#38bdf8;font-weight:bold}}
    .card{{background:white;color:black;max-width:500px;margin:20px auto;padding:20px;border-radius:20px}}
    img{{max-width:200px;border-radius:15px}}
    .wa{{background:#25D366;color:white;padding:12px 20px;border-radius:10px;text-decoration:none;display:inline-block;margin-top:15px;font-weight:bold}}
    </style></head><body>
    <h1>⚽ House Ahmed Bot V3</h1>
    <p>Website + True WhatsApp Auto-Bot!</p>
    <form><input name="q" placeholder="messi, ronaldo, hakimi" value="{q}"><button>Ask</button></form>
    """
    if player:
        img_tag = f'<img src="{player["img"]}"><br>' if player['img'] else ''
        html += f'<div class="card"><h2>{player["title"]}</h2>{img_tag}<p>{player["extract"]}</p><a class="wa" href="https://wa.me/?text={player["title"]}">Share on WhatsApp</a></div>'
    html += '<p>V3 by Ahmed | Auto WhatsApp Bot Ready</p></body></html>'
    return html

@app.route('/whatsapp', methods=['GET', 'POST'])
def whatsapp():
    # Verification for Meta
    if request.method == 'GET':
        mode = request.args.get('hub.mode')
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')
        if mode == 'subscribe' and token == VERIFY_TOKEN:
            return challenge, 200
        return "Verification failed", 403
    
    # Incoming message
    try:
        data = request.get_json()
        if data and 'entry' in data:
            for entry in data['entry']:
                for change in entry.get('changes', []):
                    value = change.get('value', {})
                    messages = value.get('messages', [])
                    for msg in messages:
                        if msg.get('type') == 'text':
                            from_number = msg['from']
                            text = msg['text']['body'].strip()
                            player = get_player(text)
                            if player:
                                reply = f"⚽ *{player['title']}*\n\n{player['extract']}\n\n🔗 {player['url']}\n\n- House Ahmed Bot V3"
                                send_whatsapp_message(from_number, reply, player['img'])
                            else:
                                send_whatsapp_message(from_number, f"Sorry, could not find '{text}'. Try: Messi, Ronaldo, Hakimi")
    except Exception as e:
        print(f"Error: {e}")
    return "OK", 200

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
