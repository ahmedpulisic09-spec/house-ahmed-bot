from flask import Flask, render_template_string
import difflib
app = Flask(__name__)

players = {
    "ronaldo": {"name": "Cristiano Ronaldo", "desc": "CR7, 5 Ballons d'Or, Portugal & Al-Nassr legend. One of greatest of all time.", "img": "https://upload.wikimedia.org/wikipedia/commons/8/8c/Cristiano_Ronaldo_2018.jpg"},
    "messi": {"name": "Lionel Messi", "desc": "Lionel Messi, Argentine GOAT, 8 Ballons d'Or, World Cup winner 2022.", "img": "https://upload.wikimedia.org/wikipedia/commons/b/b4/Lionel-Messi-Argentina-2022-FIFA-World-Cup_%28cropped%29.jpg"},
    "van dijk": {"name": "Virgil van Dijk", "desc": "Virgil van Dijk, Dutch wall, Liverpool captain, best defender in world.", "img": "https://upload.wikimedia.org/wikipedia/commons/1/1c/Virgil_van_Dijk_2019.jpg"},
    "neymar": {"name": "Neymar Jr", "desc": "Neymar Jr, Brazilian magician, Santos & Brazil superstar.", "img": "https://upload.wikimedia.org/wikipedia/commons/8/83/Neymar_PSG.jpg"},
    "mbappe": {"name": "Kylian Mbappe", "desc": "Kylian Mbappe, French speed king, Real Madrid striker.", "img": "https://upload.wikimedia.org/wikipedia/commons/5/57/2019-07-17_SG_Dynamo_Dresden_vs._Paris_Saint-Germain_by_Sandro_Halank%E2%80%93129_%28cropped%29.jpg"},
    "haaland": {"name": "Erling Haaland", "desc": "Erling Haaland, Norwegian goal machine, Man City striker.", "img": "https://upload.wikimedia.org/wikipedia/commons/1/11/Erling_Haaland_2023.jpg"},
    "pele": {"name": "Pele", "desc": "Pele, Brazilian legend, 3x World Cup winner, King of Football.", "img": "https://upload.wikimedia.org/wikipedia/commons/9/98/Pele_2008.jpg"},
    "maradona": {"name": "Diego Maradona", "desc": "Diego Maradona, Argentine legend, Hand of God, 1986 World Cup hero.", "img": "https://upload.wikimedia.org/wikipedia/commons/0/0e/Diego_Maradona_1986.jpg"},
    "zidane": {"name": "Zinedine Zidane", "desc": "Zinedine Zidane, French maestro, World Cup winner, Real Madrid legend.", "img": "https://upload.wikimedia.org/wikipedia/commons/2/22/Zidane_in_2017.jpg"},
    "benzema": {"name": "Karim Benzema", "desc": "Karim Benzema, French striker, Ballon d'Or 2022.", "img": "https://upload.wikimedia.org/wikipedia/commons/f/f2/Karim_Benzema_2018.jpg"},
}

def find_player(q):
    q = q.lower().strip()
    if q in players: return players[q], None
    # contains
    for k,v in players.items():
        if q in k or k in q: return v, None
    # fuzzy correct
    matches = difflib.get_close_matches(q, players.keys(), n=1, cutoff=0.5)
    if matches:
        return players[matches[0]], f"Did you mean {players[matches[0]]['name']}?"
    # check name
    names = {v['name'].lower(): v for v in players.values()}
    matches2 = difflib.get_close_matches(q, list(names.keys()), n=1, cutoff=0.5)
    if matches2:
        return names[matches2[0]], f"Did you mean {names[matches2[0]]['name']}?"
    return players["ronaldo"], "Not found, showing Ronaldo"

HTML = """
<!DOCTYPE html>
<html>
<head><meta name="viewport" content="width=device-width, initial-scale=1">
<style>
body{background:#0f172a;color:white;font-family:sans-serif;text-align:center;margin:0;padding:10px}
.top{display:flex;gap:5px;justify-content:center;margin-bottom:10px;position:sticky;top:0;background:#0f172a;padding:10px;z-index:10}
.top input{padding:10px;border-radius:10px;border:none;width:60%}
.top button{padding:10px 15px;border-radius:10px;border:none;font-weight:bold;cursor:pointer}
.card{background:white;color:black;border-radius:20px;padding:15px;max-width:400px;margin:auto}
img{width:100%;border-radius:15px}
.btn{padding:12px 20px;border:none;border-radius:10px;margin:5px;font-weight:bold;cursor:pointer}
.voice{background:#8b5cf6;color:white}.video-btn{background:#ef4444;color:white}
.wa{background:#25D366;color:white}.home{background:#38bdf8}
.videos{background:#fef2f2;border-radius:12px;padding:10px;margin-top:12px;display:none}
.videos a{display:block;background:#111;color:white;padding:10px;margin:6px 0;border-radius:8px;text-decoration:none}
.correct{background:#fef3c7;color:#92400e;padding:6px;border-radius:8px;margin-bottom:8px;font-size:13px}
</style>
</head>
<body>
<div class="top">
<button class="home" onclick="location.href='/'">🏠 Home</button>
<input id="search" placeholder="Try: ronalod, masei, vandik...">
<button onclick="doSearch()">🔍 Search</button>
</div>
<div class="card">
{% if msg %}<div class="correct">{{msg}}</div>{% endif %}
<img src="{{ p['img'] }}">
<h2>{{ p['name'] }}</h2>
<p>{{ p['desc'] }}</p>
<button class="btn voice" onclick="playVoice()">🔊 Play Voice</button>
<button class="btn video-btn" onclick="toggleVid()">🎥 Watch Videos</button>
<button class="btn wa" onclick="shareWA()">Share on WhatsApp</button>
<div id="vid" class="videos">
<b>Watch {{ p['name'] }} (always works):</b>
<a href="https://www.youtube.com/results?search_query={{ p['name'] }}+goals" target="_blank">⚽ Goals & Highlights</a>
<a href="https://www.youtube.com/results?search_query={{ p['name'] }}+best+skills" target="_blank">🔥 Best Skills</a>
<a href="https://www.youtube.com/results?search_query={{ p['name'] }}+interview" target="_blank">🎙️ Interviews</a>
</div>
</div>
<p>V8 by Ahmed 🔥 | Smart Search + No Block</p>
<script>
let text=`{{ p['desc'] }}`;
function playVoice(){speechSynthesis.cancel();let u=new SpeechSynthesisUtterance(text);u.rate=0.9;u.lang='en-US';speechSynthesis.speak(u);}
function toggleVid(){let d=document.getElementById('vid');d.style.display=d.style.display==='none'?'block':'none';}
function doSearch(){let q=document.getElementById('search').value.trim();if(q) location.href='/'+encodeURIComponent(q.toLowerCase());}
function shareWA(){window.open("https://wa.me/?text="+encodeURIComponent("Check {{ p['name'] }}: "+location.href));}
document.getElementById('search').addEventListener('keydown',e=>{if(e.key==='Enter') doSearch();});
</script>
</body>
</html>
"""

@app.route('/')
@app.route('/<name>')
def home(name="ronaldo"):
    p, msg = find_player(name)
    return render_template_string(HTML, p=p, msg=msg)

if __name__=='__main__':
    app.run(host='0.0.0.0', port=10000)
