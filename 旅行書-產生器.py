import re, html as H, io

src = open('旅行書-素材.md', encoding='utf-8').read().split('\n')

def inline(s):
    s = H.escape(s)
    s = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', s)
    s = re.sub(r'`(.+?)`', r'<code>\1</code>', s)
    s = re.sub(r'(?<!\*)\*([^*]+?)\*(?!\*)', r'<i>\1</i>', s)
    return s

# ── 解析 ──────────────────────────────────────
days, sections, appendix = [], {}, []
i, cur, mode = 0, None, None
while i < len(src):
    ln = src[i]
    if ln.startswith('## 📋'):
        appendix = src[i:]; break
    if ln.startswith('## '):
        sections[len(days)] = ln[3:].strip()
    elif ln.startswith('### '):
        m = re.match(r'### (D\d+)　(\S+)　(.*)', ln)
        cur = {'d': m.group(1), 'date': m.group(2), 'title': m.group(3),
               'sub': '', 'tags': [], 'sch': [], 'nb': []}
        days.append(cur); mode = None
    elif cur is not None:
        if ln.startswith('*') and not cur['sub'] and ln.endswith('*'):
            cur['sub'] = ln.strip('*')
        elif ln.startswith('摘要：'):
            cur['tags'] = [t.strip() for t in ln[3:].split('｜') if t.strip()]
        elif ln.startswith('**🕐'): mode = 'sch'
        elif ln.startswith('**📌'): mode = 'nb'
        elif ln.startswith('- ') and mode:
            cur[mode].append(ln[2:])
        elif ln.startswith('  ') and ln.strip() and mode and cur[mode]:
            cur[mode][-1] += '\n' + ln.strip()
    i += 1

# ── 產出 ──────────────────────────────────────
o = io.StringIO(); w = o.write
w('''<!doctype html><html lang="zh-Hant"><head><meta charset="utf-8">
<title>歐洲 12 天旅行書 · 2026/11/11–11/22</title>
<style>
@page { size: A5 portrait; margin: 11mm 10mm 12mm; }
*{box-sizing:border-box}
html{-webkit-print-color-adjust:exact;print-color-adjust:exact}
body{margin:0;font:9.2pt/1.55 system-ui,"Noto Sans TC","PingFang TC","Heiti TC",sans-serif;color:#000}
code{font:inherit;font-weight:700;font-variant-numeric:tabular-nums}
.pg{break-after:page}
.pg:last-child{break-after:auto}

/* 封面 */
.cover{height:100%;display:flex;flex-direction:column;justify-content:center;text-align:center;padding:0 6mm}
.cover .kk{font-size:8pt;letter-spacing:.42em;text-transform:uppercase;margin-bottom:7mm}
.cover h1{font-size:27pt;line-height:1.2;margin:0 0 4mm;letter-spacing:.02em}
.cover .dt{font-size:12.5pt;font-weight:700;margin-bottom:2mm;font-variant-numeric:tabular-nums}
.cover .sub{font-size:9pt;margin-bottom:9mm}
.cover .rule{border:0;border-top:1.6pt solid #000;width:34mm;margin:0 auto 9mm}
.cover .who{font-size:10pt;font-weight:700;letter-spacing:.2em}
.cover .foot{margin-top:11mm;font-size:7.6pt;line-height:1.7}

/* 目錄 */
h2.sec{font-size:12.5pt;margin:0 0 4mm;padding-bottom:1.6mm;border-bottom:1.6pt solid #000;letter-spacing:.03em}
.toc-g{font-size:8pt;font-weight:700;margin:4mm 0 1.6mm;padding:1mm 2mm;background:#000;color:#fff}
.toc{width:100%;border-collapse:collapse;font-size:8.6pt}
.toc td{padding:1.5mm 1mm;border-bottom:.4pt dotted #999;vertical-align:top}
.toc td.n{width:9mm;font-weight:700}
.toc td.dd{width:13mm;font-variant-numeric:tabular-nums}

/* 每日 */
.day{break-before:page}
.dh{border:1.6pt solid #000;padding:2.4mm 3mm;margin-bottom:3mm}
.dh .top{display:flex;align-items:baseline;gap:2.5mm;font-size:8pt}
.dh .num{font-size:15pt;font-weight:800;letter-spacing:.02em}
.dh .date{font-weight:700;font-variant-numeric:tabular-nums}
.dh h3{font-size:11pt;margin:1.4mm 0 0;line-height:1.35}
.tags{margin-top:2mm;font-size:7.4pt}
.tags span{display:inline-block;border:.6pt solid #000;padding:.5mm 1.6mm;margin:.6mm .8mm .6mm 0}

h4{font-size:8.4pt;margin:4mm 0 2mm;padding-left:2mm;border-left:2.4pt solid #000;letter-spacing:.06em}
.sch{width:100%;border-collapse:collapse}
.sch td{padding:1.5mm 0;border-bottom:.4pt solid #ccc;vertical-align:top;font-size:8.6pt}
.sch td.t{width:17mm;padding-right:2mm;font-weight:700;font-variant-numeric:tabular-nums;white-space:nowrap}
.nb{margin:0;padding-left:4.5mm;font-size:8.4pt}
.nb li{margin-bottom:1.8mm;line-height:1.5}
.memo{margin-top:4mm;border:.5pt dashed #666;height:15mm;padding:1mm 2mm;font-size:6.8pt;color:#666}

/* 附錄 */
table.ap{width:100%;border-collapse:collapse;font-size:8pt;margin-bottom:4mm}
table.ap th,table.ap td{border:.5pt solid #000;padding:1.4mm 1.6mm;text-align:left;vertical-align:top}
table.ap th{background:#000;color:#fff;font-size:7.6pt}
ul.ap{padding-left:4.5mm;font-size:8.4pt;margin:0 0 4mm}
ul.ap li{margin-bottom:1.6mm}
.blank td{height:7.5mm}
</style></head><body>
''')

# 封面
w('''<section class="pg cover">
<div class="kk">Travel Handbook</div>
<h1>英國 · 冰島<br>十二天</h1>
<div class="dt">2026.11.11 — 11.22</div>
<div class="sub">倫敦 · 雷克雅維克 · 南岸冰河</div>
<hr class="rule">
<div class="who">ALAN &nbsp;&amp;&nbsp; ANNE</div>
<div class="foot">本手冊內容取自已查證的行程資料<br>時間與價格以現場公告為準</div>
</section>
''')

# 目錄
w('<section class="pg"><h2 class="sec">目錄</h2><table class="toc">')
for idx, d in enumerate(days):
    if idx in sections:
        w(f'</table><div class="toc-g">{inline(sections[idx])}</div><table class="toc">')
    w(f'<tr><td class="n">{d["d"]}</td><td class="dd">{d["date"]}</td>'
      f'<td>{inline(d["title"])}</td></tr>')
w('</table><div class="toc-g">附錄</div><table class="toc">'
  '<tr><td class="n">A</td><td class="dd">—</td><td>航班・住宿・已訂項目・緊急資訊</td></tr>'
  '<tr><td class="n">B</td><td class="dd">—</td><td>消費記錄・筆記</td></tr></table></section>')

# 每日
for idx, d in enumerate(days):
    grp = sections.get(idx, '')
    w('<section class="day"><div class="dh"><div class="top">'
      f'<span class="num">{d["d"]}</span>'
      f'<span class="date">{inline(d["sub"])}</span></div>'
      f'<h3>{inline(d["title"])}</h3>')
    if d['tags']:
        w('<div class="tags">' + ''.join(f'<span>{inline(t)}</span>' for t in d['tags']) + '</div>')
    w('</div>')
    if d['sch']:
        w('<h4>🕐 時間軸</h4><table class="sch">')
        for it in d['sch']:
            m = re.match(r'`(.*?)` ?(.*)', it, re.S)
            t, body = (m.group(1), m.group(2)) if m else ('', it)
            w(f'<tr><td class="t">{inline(t)}</td><td>'
              + inline(body).replace('\n', '<br>') + '</td></tr>')
        w('</table>')
    if d['nb']:
        w(f'<h4>📌 重點與備註 · {len(d["nb"])} 則</h4><ul class="nb">')
        for n in d['nb']:
            w('<li>' + inline(n).replace('\n', '<br>') + '</li>')
        w('</ul>')
    w('<div class="memo">現場筆記</div></section>')

# 附錄
w('<section class="day"><h2 class="sec">附錄 A · 基本資料</h2>')
j = 0
while j < len(appendix):
    ln = appendix[j]
    if ln.startswith('### '):
        w(f'<h4>{inline(ln[4:])}</h4>')
    elif ln.startswith('|'):
        rows = []
        while j < len(appendix) and appendix[j].startswith('|'):
            rows.append(appendix[j]); j += 1
        j -= 1
        w('<table class="ap">')
        for k, r in enumerate(rows):
            if set(r.replace('|', '').replace(' ', '')) <= set('-:'):
                continue
            cells = [c.strip() for c in r.strip('|').split('|')]
            tag = 'th' if k == 0 else 'td'
            w('<tr>' + ''.join(f'<{tag}>{inline(c)}</{tag}>' for c in cells) + '</tr>')
        w('</table>')
    elif ln.startswith('- '):
        items = []
        while j < len(appendix) and appendix[j].startswith('- '):
            items.append(appendix[j][2:]); j += 1
        j -= 1
        w('<ul class="ap">' + ''.join(f'<li>{inline(x)}</li>' for x in items) + '</ul>')
    j += 1
w('</section>')

# 空白記錄頁
w('<section class="day"><h2 class="sec">附錄 B · 消費記錄</h2>'
  '<table class="ap"><tr><th>日期</th><th>項目</th><th>誰付</th><th>金額</th><th>共同?</th></tr>'
  + '<tr class="blank"><td></td><td></td><td></td><td></td><td></td></tr>' * 18
  + '</table></section>')
w('<section class="day"><h2 class="sec">附錄 B · 筆記</h2>'
  '<table class="ap">' + '<tr class="blank"><td></td></tr>' * 22 + '</table></section>')

w('</body></html>')
open('旅行書.html', 'w', encoding='utf-8').write(o.getvalue())
print(f'✅ {len(days)} 天・{len(o.getvalue())//1024} KB')
