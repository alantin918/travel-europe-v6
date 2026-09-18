# -*- coding: utf-8 -*-
"""產出給 AI 生圖當版面參考（image_0.png）的底稿：左欄行程 + 地圖 + 路線圖例 + 住宿。"""
import re, html as H, io

h = open('index.html', encoding='utf-8').read()

sec = h[h.index('id="days"'):h.index('</section>', h.index('id="days"'))]
days = []
for m in re.finditer(r'<article class="day[^"]*">(.*?)</article>', sec, re.S):
    a = m.group(1)
    dn = re.search(r'<span class="dnum">(D\d+)<span>(.*?)</span>', a)
    tt = re.search(r'<span class="dttl"><b>(.*?)</b><em>(.*?)</em>', a)
    tg = re.search(r'<span class="dtag">(.*?)</span></span>', a, re.S)
    days.append({'d': dn.group(1), 'date': dn.group(2),
                 'title': re.sub(r'<[^>]+>', '', tt.group(1)),
                 'tags': [re.sub(r'<[^>]+>', '', x) for x in re.findall(r'<span>(.*?)</span>', tg.group(1))] if tg else []})

ms = h[h.index('id="maps"'):h.index('</section>', h.index('id="maps"'))]
svgs = re.findall(r'<svg.*?</svg>', ms, re.S)
keys = re.findall(r'<div class="mapkey">(.*?)</div>', ms, re.S)
def legend(k):
    return ''.join(f'<span><i style="background:{c}"></i>{t}</span>'
                   for c, t in re.findall(r'background:(#[0-9a-fA-F]{6})"></i>(.*?)</span>', k))

HOTELS = [('A', '南岸 Airbnb', '倫敦 · 2 晚', '11/11–13'),
          ('B', 'KONVIN Hotel', '雷克雅維克 · 1 晚', '11/13–14'),
          ('C', 'ASKA Holt', '雷克雅維克 · 1 晚', '11/14–15'),
          ('D', 'Hotel Geirland', '南岸 · 2 晚（含團費）', '11/15–17'),
          ('E', 'ASKA Holt', '雷克雅維克 · 1 晚', '11/17–18'),
          ('F', 'studios2Let', '倫敦 Bloomsbury · 3 晚', '11/18–21')]
FLIGHTS = [('D1', '11/11', '✈︎', '台北 TPE → 倫敦 LHR', 'CI81 · 15h40m'),
           ('D3', '11/13', '✈︎', '倫敦 LTN → 凱夫拉維克 KEF', 'easyJet · 15:55'),
           ('D8', '11/18', '✈︎', '凱夫拉維克 KEF → 倫敦 LTN', 'easyJet · 12:05'),
           ('D11', '11/21', '✈︎', '倫敦 LHR → 台北 TPE', 'CI82 · 13h30m')]

o = io.StringIO(); w = o.write
w('''<!doctype html><html lang="zh-Hant"><head><meta charset="utf-8"><title>版面底稿</title><style>
*{box-sizing:border-box}
body{margin:0;width:1600px;height:1820px;display:flex;background:#faf7f0;
     font:14px/1.5 system-ui,"Noto Sans TC","PingFang TC",sans-serif;color:#2b2b2b}
.side{width:430px;flex:none;background:#f3ede0;border-right:3px solid #2b2b2b;padding:20px 18px;overflow:hidden}
.side h2{font-size:21px;margin:0 0 18px;letter-spacing:.12em;border-bottom:2.5px solid #2b2b2b;padding-bottom:7px}
.dy{margin-bottom:14px;padding-bottom:12px;border-bottom:1px dashed #b9ad95}
.dy .hd{display:flex;align-items:baseline;gap:7px}
.dy .n{font-size:16.5px;font-weight:800;letter-spacing:.03em}
.dy .dt{font-size:12px;color:#6b6152}
.dy .ti{font-size:14.5px;font-weight:700;margin-top:2px;line-height:1.35}
.dy ul{margin:5px 0 0;padding-left:16px;font-size:12.5px;color:#4a4335;line-height:1.5}

.main{flex:1;display:flex;flex-direction:column;padding:18px 20px;min-width:0}
.scroll{align-self:center;background:#2b2b2b;color:#faf7f0;padding:9px 40px;font-size:25px;
        font-weight:800;letter-spacing:.2em;margin-bottom:14px;position:relative}
.scroll::before,.scroll::after{content:'';position:absolute;top:0;bottom:0;width:16px;background:#2b2b2b}
.scroll::before{left:-16px;clip-path:polygon(100% 0,100% 100%,0 60%,0 40%)}
.scroll::after{right:-16px;clip-path:polygon(0 0,0 100%,100% 60%,100% 40%)}
.maps{flex:1;display:flex;flex-direction:column;gap:12px;min-height:0}
.mb{border:2.5px solid #2b2b2b;background:#fff;padding:9px 11px;position:relative}
.mb h3{font-size:14px;margin:0 0 5px;letter-spacing:.06em}
.mb svg{width:100%;height:auto;display:block}
.mapkey{margin-top:6px;font-size:10.5px;display:flex;flex-wrap:wrap;gap:2px 13px}
.mapkey span{display:inline-flex;align-items:center;gap:4px;white-space:nowrap}
.mapkey i{width:9px;height:9px;border-radius:50%;display:inline-block}

.bot{display:flex;gap:12px;margin-top:12px;flex:none}
.bx{border:2.5px solid #2b2b2b;background:#fff;padding:9px 11px;flex:1}
.bx h4{font-size:13px;margin:0 0 6px;letter-spacing:.08em;border-bottom:1.5px solid #2b2b2b;padding-bottom:4px}
table{width:100%;border-collapse:collapse;font-size:11px}
td{padding:2.5px 0;vertical-align:top;line-height:1.4}
td.k{width:30px;font-weight:800}
td.s{width:56px;color:#6b6152}
.pin{display:inline-block;width:18px;height:18px;border-radius:50%;background:#2b2b2b;color:#fff;
     text-align:center;line-height:18px;font-size:10px;font-weight:800;margin-right:5px}
</style></head><body>
<div class="side"><h2>行 程 ITINERARY</h2>''')

for d in days:
    w(f'<div class="dy"><div class="hd"><span class="n">{d["d"]}</span>'
      f'<span class="dt">{H.escape(d["date"])}</span></div>'
      f'<div class="ti">{H.escape(d["title"])}</div>')
    if d['tags']:
        w('<ul>' + ''.join(f'<li>{H.escape(t)}</li>' for t in d['tags']) + '</ul>')
    w('</div>')

w('</div><div class="main"><div class="scroll">倫敦 ✦ 冰島 ✦ 旅遊地圖</div><div class="maps">')
for t, sv, k in [('🧊 冰島 ICELAND · 西南角＋南岸', svgs[0], keys[0]),
                 ('🇬🇧 倫敦 LONDON · 依日期上色', svgs[1], keys[1])]:
    sv = re.sub(r'\s(width|height)="[^"]*"', '', sv, count=2)
    w(f'<div class="mb"><h3>{t}</h3>{sv}<div class="mapkey">{legend(k)}</div></div>')
w('</div><div class="bot">')

w('<div class="bx"><h4>✈︎ 航班 FLIGHTS</h4><table>')
for d, dt, ic, rt, nt in FLIGHTS:
    w(f'<tr><td class="k">{ic}</td><td class="s">{d} · {dt}</td><td><b>{rt}</b><br>{nt}</td></tr>')
w('</table></div>')

w('<div class="bx"><h4>🏨 住宿 ACCOMMODATION</h4><table>')
for k, n, p, dt in HOTELS:
    w(f'<tr><td class="k"><span class="pin">{k}</span></td><td class="s">{dt}</td>'
      f'<td><b>{n}</b><br>{p}</td></tr>')
w('</table></div></div></div></body></html>')

open('地圖底稿.html', 'w', encoding='utf-8').write(o.getvalue())
print(f'✅ {len(days)} 天・{len(svgs)} 地圖')
