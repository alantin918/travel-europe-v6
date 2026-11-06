# -*- coding: utf-8 -*-
"""從 index.html 抽出 12 天 + 兩張 SVG 地圖，產出 A4 橫式一頁總覽。"""
import re, html as H, io

h = open('index.html', encoding='utf-8').read()

# ── 抓 12 天 ──────────────────────────────
sec = h[h.index('id="days"'):h.index('</section>', h.index('id="days"'))]
days, groups = [], {}
for m in re.finditer(r'<div class="seg"><b>(.*?)</b><em>(.*?)</em>|<article class="day[^"]*">(.*?)</article>', sec, re.S):
    if m.group(1):
        groups[len(days)] = (re.sub(r'<[^>]+>', '', m.group(1)), re.sub(r'<[^>]+>', '', m.group(2)))
        continue
    a = m.group(3)
    dn = re.search(r'<span class="dnum">(D\d+)<span>(.*?)</span>', a)
    tt = re.search(r'<span class="dttl"><b>(.*?)</b><em>(.*?)</em>', a)
    tg = re.search(r'<span class="dtag">(.*?)</span></span>', a, re.S)
    days.append({
        'd': dn.group(1), 'date': dn.group(2),
        'title': re.sub(r'<[^>]+>', '', tt.group(1)),
        'sub': re.sub(r'<[^>]+>', '', tt.group(2)),
        'tags': [re.sub(r'<[^>]+>', '', x) for x in re.findall(r'<span>(.*?)</span>', tg.group(1))] if tg else [],
    })

# ── 抓兩張地圖 ─────────────────────────────
ms = h[h.index('id="maps"'):h.index('</section>', h.index('id="maps"'))]
svgs = re.findall(r'<svg.*?</svg>', ms, re.S)
keys = re.findall(r'<div class="mapkey">(.*?)</div>', ms, re.S)

def legend(k):
    out = []
    for c, t in re.findall(r'background:(#[0-9a-fA-F]{6})"></i>(.*?)</span>', k):
        out.append(f'<span><i style="background:{c}"></i>{t}</span>')
    return ''.join(out)

o = io.StringIO(); w = o.write
w('''<!doctype html><html lang="zh-Hant"><head><meta charset="utf-8">
<title>英國・冰島十二天 · 一頁總覽</title><style>
@page{size:A4 landscape;margin:7mm}
*{box-sizing:border-box}
html{-webkit-print-color-adjust:exact;print-color-adjust:exact}
body{margin:0;font:8pt/1.45 system-ui,"Noto Sans TC","PingFang TC",sans-serif;color:#111;
     width:283mm;height:196mm;display:flex;flex-direction:column;gap:2.5mm}
.hd{display:flex;align-items:baseline;gap:4mm;border-bottom:1.8pt solid #111;padding-bottom:1.8mm;flex:none}
.hd h1{font-size:16pt;margin:0;letter-spacing:.03em}
.hd .dt{font-size:10pt;font-weight:700;font-variant-numeric:tabular-nums}
.hd .wh{margin-left:auto;font-size:8.5pt;font-weight:700;letter-spacing:.16em}
.hd .su{font-size:7.5pt;color:#555}

.mid{display:flex;gap:3.5mm;flex:1;min-height:0}
.col-l{width:162mm;flex:none;display:flex;flex-direction:column}
.col-r{width:116mm;flex:none;display:flex;flex-direction:column;gap:2.5mm}

.grp{font-size:7.2pt;font-weight:700;background:#111;color:#fff;padding:.6mm 1.6mm;margin:1.2mm 0 .8mm;letter-spacing:.04em}
.grp:first-child{margin-top:0}
.grp em{float:right;font-size:6.6pt;font-style:normal;font-weight:400;opacity:.8}
table.dl{width:100%;border-collapse:collapse}
table.dl td{padding:.65mm 0;border-bottom:.4pt solid #ddd;vertical-align:top;font-size:8pt;line-height:1.4}
td.n{width:8mm;font-weight:800;font-size:8.3pt}
td.dd{width:19mm;font-variant-numeric:tabular-nums;color:#555}
td.tt b{font-size:8.3pt}
td.tt i{font-style:normal;color:#555;font-size:6.8pt}

.mapbox{display:flex;flex-direction:column;border:.6pt solid #bbb;padding:1.6mm}
.mapbox h3{font-size:7.6pt;margin:0 0 1mm;letter-spacing:.03em}
.mapbox svg{width:100%;height:auto;display:block}
.mapkey{margin-top:1.2mm;font-size:6.2pt;display:flex;flex-wrap:wrap;gap:0 2.6mm}
.mapkey span{display:inline-flex;align-items:center;gap:.9mm;white-space:nowrap}
.mapkey i{width:2.1mm;height:2.1mm;border-radius:50%;display:inline-block}

.ft{flex:none;border-top:1.2pt solid #111;padding-top:1.6mm;margin-top:1.5mm;display:flex;gap:5mm;font-size:7pt;line-height:1.55}
.ft div{flex:1;min-width:0}
.ft b{display:block;font-size:7.2pt;margin-bottom:.6mm;letter-spacing:.05em}

table.dead td{font-size:6.9pt;padding:.42mm 0;line-height:1.3}
table.dead td.dd{width:19mm;font-weight:700;color:#111}
</style></head><body>
<div class="hd">
  <h1>英國 · 冰島 十二天</h1>
  <span class="dt">2026.11.11 — 11.22</span>
  <span class="su">倫敦 · 雷克雅維克 · 南岸冰河</span>
  <span class="wh">ALAN &amp; ANNE</span>
</div>
<div class="mid"><div class="col-l">''')

for i, d in enumerate(days):
    if i in groups:
        if i: w('</table>')
        g = groups[i]
        w(f'<div class="grp">{H.escape(g[0])}<em>{H.escape(g[1])}</em></div><table class="dl">')
    tags = ' · '.join(d['tags'])
    w(f'<tr><td class="n">{d["d"]}</td><td class="dd">{H.escape(d["date"])}</td>'
      f'<td class="tt"><b>{H.escape(d["title"])}</b>'
      + (f'<br><i>{H.escape(tags)}</i>' if tags else '') + '</td></tr>')
w('</table>')
w('''<div class="grp">🗓️ 出發前的關鍵時間點<em>過了就是真的付出去了</em></div>
<table class="dl dead">
<tr><td class="dd">10/19 一</td><td>🆓 <b>Sky Garden 開搶</b>（每週一釋出、常 2–3 週前就滿）</td></tr>
<tr><td class="dd">10/27 一</td><td>🔭 <b>Horizon 22</b> 台北 18:00 開放（提前 14 天）</td></tr>
<tr><td class="dd">11/8</td><td>🔴 取消 ASKA Holt 11/16–17（已被取代）｜KONVIN 此後不可免費取消</td></tr>
<tr><td class="dd">11/10</td><td>🔴 取消格域機場飯店（多餘訂單）</td></tr>
<tr><td class="dd">11/12</td><td>🔴 取消 Forth House 愛丁堡（不去了）＋ 查隔天班機</td></tr>
<tr><td class="dd">11/13 09:00</td><td>♨️ 藍湖門票可全額退的最後時刻</td></tr>
<tr><td class="dd">11/13 12:15</td><td>🚌 GYG 藍湖回程接駁免費取消截止</td></tr>
<tr><td class="dd">11/14 09:00</td><td>🧊 <b>冰島三日團</b>可全額退的最後時刻（ISK 233,982）</td></tr>
</table>''')
w('</div><div class="col-r">')

for title, sv, k in [('🧊 冰島 · 西南角＋南岸（沒有環島）', svgs[0], keys[0]),
                     ('🇬🇧 倫敦 · 依日期上色', svgs[1], keys[1])]:
    sv = re.sub(r'\s(width|height)="[^"]*"', '', sv, count=2)
    w(f'<div class="mapbox"><h3>{title}</h3>{sv}<div class="mapkey">{legend(k)}</div></div>')

w('''</div></div>
<div class="ft">
<div><b>✈️ 航班</b>
11/11 CI81 TPE→LHR T3 09:15→16:55（15h40m）｜11/13 easyJet LTN→KEF 15:55<br>
11/18 easyJet KEF→LTN 12:05（走 D 閘口）｜11/21 CI82 LHR T3→TPE（APD £147 現場繳）</div>
<div><b>🏨 住宿</b>
11/11–13 南岸 Airbnb（68 Southwark Bridge Rd, SE1）｜11/13–14 KONVIN｜11/14–15 ASKA Holt<br>
11/15–17 Hotel Geirland（含團費）｜11/17–18 ASKA Holt｜11/18–21 studios2Let Bloomsbury</div>
<div><b>🚨 現場</b>
緊急電話 <b>112</b>（兩國通用）｜路況 road.is｜天氣與極光 vedur.is<br>
冰島不用小費・沒有 Uber（用 Hopp／Hreyfill）｜倫敦帳單 12.5% 服務費可請店家移除</div>
</div></body></html>''')

open('一頁總覽.html', 'w', encoding='utf-8').write(o.getvalue())
print(f'✅ {len(days)} 天・{len(svgs)} 張地圖・{len(o.getvalue())//1024} KB')
