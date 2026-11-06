# -*- coding: utf-8 -*-
import re
h=open('index.html',encoding='utf-8').read()

M={
'D1':['華航 CI81 起飛','抵達希斯洛 T3','叫 Uber 進市區','南岸晚餐','就寢'],
'D2':['出發','碎片塔','波羅市場','千禧橋','聖保羅大教堂','公車往 Bank','Horizon 22','倫敦塔','倫敦塔橋','Sky Garden','南岸晚餐','回住處'],
'D3':['南岸早餐','整理行李・退房','泰特現代（機動）','前往盧頓機場','easyJet 起飛','抵達 KEF','KONVIN 入住','飯店晚餐'],
'D4':['起床','KONVIN 退房','前往藍湖','藍湖入場・寄行李','藍湖 · 泡湯 3 小時','接駁巴士回市區','備案：13:15 那班','ASKA Holt 放行李','熱狗午餐','Kolaportið（已取消）','市政廳','彩虹街','哈爾格林姆教堂・登塔','Braud & Co 肉桂捲','Laugavegur 主街','哈帕音樂廳','走去麵包湯店','麵包湯晚餐','回 ASKA Holt'],
'D5':['出發・上車','沒被接到怎麼辦'],
'D7':['回到雷克雅維克','前往天空潟湖','天空潟湖・七步驟儀式','叫車回市區'],
'D8':['起床','早餐・最後整理','ASKA Holt 退房','Flybus 前往 KEF','KEF 出境・D 區','要不要退稅','免稅店（已取消）','起飛 → 盧頓','出關・前往市區','St Pancras 聖誕樹','進住處放行李','前往 Oxford Circus','W1 聖誕燈飾夜','Hamleys 玩具店','福楠梅森櫥窗','Bancone 晚餐'],
'D9':['大英博物館','Flat Iron 午餐','柯芬園・聖誕市集','倫敦交通博物館','劇前晚餐','哈利波特舞台劇'],
'D10':['出門','悠閒午餐','特拉法加廣場','The Mall 皇家大道','白金漢宮','聖詹姆斯公園','日落','大笨鐘・國會大廈','倫敦眼・南岸市集','過橋回北岸','Leicester Square 市集','Blacklock 晚餐'],
'D11':['波多貝羅市集','諾丁丘午餐','回 King\'s Cross 拿行李','前往希斯洛','華航 CI82 起飛'],
'D12':['抵達桃園'],
}

s=h.index('id="days"'); e=h.index('</section>',s)
sec=h[s:e]; out=[]; pos=0; n=0
for am in re.finditer(r'<article class="day[^"]*">(.*?)</article>', sec, re.S):
    a=am.group(1)
    dn=re.search(r'<span class="dnum">(D\d+)',a).group(1)
    labels=M.get(dn,[])
    olm=re.search(r'<ol class="sch">(.*?)</ol>',a,re.S)
    if not olm or not labels: continue
    ol=olm.group(1); newol=ol; idx=0; cursor=0; parts=[]
    for lim in re.finditer(r'<li>(.*?)</li>', ol, re.S):
        if idx>=len(labels): idx+=1; continue
        lab=labels[idx]; idx+=1
        inner=lim.group(1)
        pm=re.search(r'<p>', inner)
        if not pm: continue
        newinner=inner[:pm.end()]+f'<b class="spot">{lab}</b>'+inner[pm.end():]
        parts.append((lim.start(),lim.end(),'<li>'+newinner+'</li>'))
        n+=1
    if parts:
        buf=[];last=0
        for st,en,rep in parts:
            buf.append(ol[last:st]); buf.append(rep); last=en
        buf.append(ol[last:])
        newol=''.join(buf)
        sec=sec.replace(ol,newol,1)
h=h[:s]+sec+h[e:]

# CSS
css_anchor='.sch>li>p b{color:var(--text);font-weight:600}'
assert h.count(css_anchor)==1
h=h.replace(css_anchor, css_anchor+'''
  .sch>li>p b.spot{display:block;font-size:14.8px;font-weight:800;color:var(--text);
    letter-spacing:.01em;line-height:1.3;margin:0 0 4px}''',1)
m2='.sch>li>p,.nb li{font-size:13.4px}'
assert h.count(m2)==1
h=h.replace(m2, m2+'\n  .sch>li>p b.spot{font-size:14px;margin-bottom:3px}',1)

open('index.html','w',encoding='utf-8').write(h)
print(f'✅ 插入 {n} 個地點標題')
