from flask import Flask, render_template_string

app = Flask(__name__)

players = {
    "ronaldo": {
        "name": "Cristiano Ronaldo",
        "desc": "Cristiano Ronaldo dos Santos Aveiro is a Portuguese professional footballer who plays as a forward for and captains both Al-Nassr and Portugal. Nicknamed CR7, he is widely regarded as one of the greatest footballers of all time. Winner of 5 Ballons d'Or.",
        "img": "https://upload.wikimedia.org/wikipedia/commons/8/8c/Cristiano_Ronaldo_2018.jpg",
        "video": "0N2yW6sa-vE"  # NEW - embed allowed
    },
    "messi": {
        "name": "Lionel Messi",
        "desc": "Lionel Messi is Argentine GOAT, World Cup winner 2022, 8 Ballons d'Or.",
        "img": "https://upload.wikimedia.org/wikipedia/commons/b/b4/Lionel-Messi-Argentina-2022-FIFA-World-Cup_%28cropped%29.jpg",
        "video": "l9Jn0A5k94g"  # NEW - embed allowed
    },
    "van dijk": {
        "name": "Virgil van Dijk",
        "desc": "Virgil van Dijk is Dutch defender, Liverpool captain, one of best CBs in world.",
        "img": "https://upload.wikimedia.org/wikipedia/commons/1/1c/Virgil_van_Dijk_2019.jpg",
        "video": "d5gIm1y4H5w"
    }
}

HTML = """
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
body { background:#0f172a; color:white; font-family:sans-serif; text-align:center; margin:0; padding:10px; }
.top { display:flex; gap:5px; justify-content:center; margin-bottom:10px; position:sticky; top:0; background:#0f172a; padding:10px; z-index:10; }
.top input { padding:10px; border-radius:10px; border:none; width:60%; }
.top button { padding:10px 15px; border-radius:10px; border:none; font-weight:bold; cursor:pointer; }
.card { background:white; color:black; border-radius:20px; padding:15px; max-width:400px; margin:auto; }
img { width:100%; border-radius:15px; max-height:400px; object-fit:cover; }
.btn { padding:12px 20px; border:none; border-radius:10px; margin:5px; font-weight:bold; cursor:pointer; }
.voice { background:#8b5cf6; color:white; } .video-btn { background:#ef4444; color:white; }
.wa { background:#25D366; color:white; } .home { background:#38bdf8; }
iframe { width:100%; height:220px; border-radius:10px; margin-top:10px; border:none; }
a.ytlink { display:block; margin-top:8px; color:#ef4444; font-weight:bold; }
</style>
</head>
<body>

<div class="top">
<button class="home" onclick="window.location.href='/'">🏠 Home</button>
<input id="search" placeholder="Search player: messi, ronaldo...">
<button onclick="doSearch()">🔍 Search</button>
</div>

<div class="card">
<img src="{{ p['img'] }}">
<h2>{{ p['name'] }}</h2>
<p>{{ p['desc'] }}</p>

<button class="btn voice" onclick="playVoice()">🔊 Play Voice</button>
<button class="btn video-btn" onclick="toggleVid()">🎥 Watch Videos</button>
<button class="btn wa" onclick="shareWA()">Share on WhatsApp</button>

<div id="vid" style="display:none;">
<iframe id="ytframe" src="" allowfullscreen allow="autoplay"></iframe>
<a class="ytlink" id="ytlink" href="" target="_blank">▶️ Open on YouTube if not playing</a>
</div>

</div>
<p>V6 by Ahmed 🔥 | Search + Voice + Video</p>

<script>
let text = `{{ p['desc'] }}`;
let ytId = "{{ p['video'] }}";
function playVoice(){
  window.speechSynthesis.cancel();
  let u = new SpeechSynthesisUtterance(text);
  u.rate=0.9; u.lang='en-US';
  window.speechSynthesis.speak(u);
}
function toggleVid(){
  let div = document.getElementById('vid');
  let frame = document.getElementById('ytframe');
  let link = document.getElementById('ytlink');
  if(div.style.display==='none'){
    frame.src = "https://www.youtube-nocookie.com/embed/" + ytId + "?rel=0";
    link.href = "https://www.youtube.com/watch?v=" + ytId;
    div.style.display='block';
  } else {
    div.style.display='none';
    frame.src='';
  }
}
function doSearch(){
  let q = document.getElementById('search').value.toLowerCase().trim();
  if(q) window.location.href='/' + encodeURIComponent(q);
}
function shareWA(){
  window.open("https://wa.me/?text=" + encodeURIComponent("Check {{ p['name'] }}: " + window.location.href));
}
document.getElementById('search').addEventListener('keydown', function(e){ if(e.key==='Enter') doSearch(); });
</script>
</body>
</html>
"""

@app.route('/')
@app.route('/<name>')
def home(name="ronaldo"):
    key = name.lower().strip()
    p = players.get(key)
    if not p:
        # search partial
        for k,v in players.items():
            if key in k or k in key:
                p = v
                break
        if not p: p = players["ronaldo"]
    return render_template_string(HTML, p=p)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
