import cowsay, requests, urllib.parse, re
name="Ahmed"
print(f"HOUSE AHMED v9 - FOOTBALL ONLY!")
print("Now understands gullit = Ruud Gullit")
print("Type bye to exit\n")

def ask_wiki(q):
    try:
        ql=q.lower().strip()
        headers={"User-Agent":"AhmedBot/1.0"}
        entity=re.sub(r'^(who|what|how many|how|tell me|search).*\b(is|are|does|has)?\s*', '', ql)
        entity=re.sub(r'\b(goals|goal|does|has|have|many|score)\b', '', entity).strip()
        if not entity: entity="Cristiano Ronaldo"
        
        # FORCE football search
        sq=urllib.parse.quote(entity)
        # First try with footballer to avoid guitar vs gullit!
        search_url=f"https://en.wikipedia.org/w/api.php?action=opensearch&search={sq} footballer&limit=1&format=json"
        sr=requests.get(search_url,timeout=15,headers=headers).json()
        if len(sr)>1 and sr[1]:
            real_title=sr[1][0]
        else:
            # fallback normal search
            search_url2=f"https://en.wikipedia.org/w/api.php?action=opensearch&search={sq}&limit=1&format=json"
            sr2=requests.get(search_url2,timeout=15,headers=headers).json()
            real_title=sr2[1][0] if len(sr2)>1 and sr2[1] else entity
        
        enc=urllib.parse.quote(real_title.replace(" ","_"))
        r=requests.get(f"https://en.wikipedia.org/api/rest_v1/page/summary/{enc}",timeout=15,headers=headers)
        summary=r.json().get("extract","") if r.status_code==200 else "Not found"
        if not summary or len(summary)<5:
            summary=f"{real_title} - football legend!"
        return summary
    except Exception as e:
        return f"Try full name: ruud gullit, luka modric"

while True:
    q=input("You: ").strip()
    if not q: continue
    if q.lower()=="bye":
        cowsay.cow(f"Valar Morghulis, {name}!"); break
    print("Bot: Searching...")
    ans=ask_wiki(q)
    cowsay.cow(ans[:600])
    print(f"Bot: {ans}\n")
