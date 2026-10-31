from flask import Flask, render_template_string
import random

app = Flask(__name__)

# Sample players data - KEEP YOUR PLAYERS, just example
players = {
    "ronaldo": {
        "name": "Cristiano Ronaldo",
        "desc": "Cristiano Ronaldo dos Santos Aveiro is a Portuguese professional footballer who plays as a forward for and captains both the Saudi Pro League club Al-Nassr and the Portugal national team. Nicknamed CR7, he is widely regarded as one of the greatest footballers of all time. He has won numerous individual accolades throughout his career, including five Ballons d'Or, a record three UEFA Men's Player of the Year Awards, and four European Golden Shoes. He was named the world's best player five times b",
        "img": "https://upload.wikimedia.org/wikipedia/commons/8/8c/Cristiano_Ronaldo_2018.jpg",
        "video": "OUKGsb8Cp9k" # WORKING highlight video ID
    },
    "messi": {
        "name": "Lionel Messi",
        "desc": "Lionel Messi is an Argentine professional footballer, widely regarded as the best ever.",
        "img": "https://upload.wikimedia.org/wikipedia/commons/b/b4/Lionel-Messi-Argentina-2022-FIFA-World-Cup_%28cropped%29.jpg",
        "video": "bWP1qF3g1s0"
    }
}

HTML = """
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
body { background:#0f172a; color:white; font-family: sans-serif; text-align:center; padding:10px; }
.card { background:white; color:black; border-radius:20px; padding:15px; max-width:400px; margin:auto; }
img { width:100%; border-radius:15px; }
button { padding:12px 20px; border:none; border-radius:10px; margin:5px; font-weight:bold; cursor:pointer; }
.voice { background:#8b5cf6; color:white; }
.video-btn { background:#ef4444; color:white; }
.wa { background:#25D366; color:white; }
iframe { width:100%; height:200px; border-radius:10px; margin-top:10px; }
</style>
</head>
<body>
<div class="card">
<img src="{{ p['img'] }}">
<h2>{{ p['name'] }}</h2>
<p>{{ p['desc'] }}</p>

<button class="voice" onclick="playVoice()">🔊 Play Voice</button>
<button class="video-btn" onclick="document.getElementById('vid').style.display='block'">🎥 Watch Videos</button>
<button class="wa" onclick="shareWA()">Share on WhatsApp</button>

<div id="vid" style="display:none;">
<iframe src="https://www.youtube.com/embed/{{ p['video'] }}" allowfullscreen></iframe>
</div>

</div>
<p>V5 by Ahmed 🔥 | Voice + Video + WhatsApp</p>

<script>
let text = "{{ p['desc'] }}";
function playVoice() {
  if ('speechSynthesis' in window) {
    window.speechSynthesis.cancel();
    let utter = new SpeechSynthesisUtterance(text);
    utter.rate = 0.9;
    utter.lang = 'en-US';
    window.speechSynthesis.speak(utter);
  } else {
    alert("Voice not supported on this browser, try Chrome!");
  }
}
function shareWA() {
  let url = window.location.href;
  window.open("https://wa.me/?text=" + encodeURIComponent("Check {{ p['name'] }} on House Ahmed Bot: " + url));
}
</script>
</body>
</html>
"""

@app.route('/')
@app.route('/<name>')
def home(name="ronaldo"):
    name = name.lower()
    p = players.get(name, players["ronaldo"])
    return render_template_string(HTML, p=p)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
