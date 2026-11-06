import re

path = '/Users/weilun/歐洲旅行計劃書/web-v6/aurora.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace title and metadata
content = content.replace('Luna Ultra × S23 Ultra 分工', 'Action 6 × S23 Ultra 分工')
content = content.replace('Luna Ultra 跑 8K 縮時', 'Action 6 跑 4K 縮時')

# Section: 分工
content = content.replace('<div class="name">Luna Ultra</div>', '<div class="name">DJI Action 6</div>')
content = content.replace('<li><b>8K 縮時攝影</b>（Timelapse）</li>', '<li><b>4K 星空縮時</b>（Night Lapse）</li>')
content = content.replace('<li>1 吋感光元件，解析度與單格畫質最好</li>', '<li>1/1.1 吋大底 ＋ <b>微距鏡頭解鎖 f/2.0 大光圈</b></li>')
content = content.replace('<li>可做<b>移動縮時</b>（雲台運鏡）——手機做不到</li>', '<li>極地防凍電池，零下暴雪絕不當機</li>')
content = content.replace('<li>Luna 跑縮時的那 20～30 分鐘', '<li>Action 6 跑縮時的那 20～30 分鐘')

# Section: 快門速查
content = content.replace('<div class="val">1–3 秒</div>', '<div class="val">4–6 秒</div>')
content = content.replace('<div class="val">4–8 秒</div>', '<div class="val">10–15 秒</div>')
content = content.replace('<div class="val">10–15 秒</div>', '<div class="val">20–25 秒</div>')

# Section: 兩台設定
content = content.replace('<h3>Luna Ultra · 縮時</h3>', '<h3>DJI Action 6 · 縮時 (需掛上微距鏡頭)</h3>')
content = content.replace('<tr><td class="nowrap">模式</td><td><b>Timelapse</b>（間隔拍攝）</td></tr>', '<tr><td class="nowrap">模式</td><td><b>Night Lapse</b>（靜止延時）</td></tr>')
content = content.replace('<tr><td class="nowrap">快門</td><td>2～8 秒（依上方速查）</td></tr>', '<tr><td class="nowrap">快門</td><td>4～25 秒（極光越快、快門越短）</td></tr>')
content = content.replace('<tr><td class="nowrap">間隔</td><td>等於或略大於快門時間</td></tr>', '<tr><td class="nowrap">間隔</td><td><b>絕對大於快門 3~5 秒</b>（防存檔當機）</td></tr>')
content = content.replace('<tr><td class="nowrap">輸出</td><td>8K</td></tr>', '<tr><td class="nowrap">輸出</td><td>4K / RAW</td></tr>')
content = content.replace('<b>拿到相機第一件事：進專業模式看最長快門能調到幾秒。</b><br>≥4 秒 → 很好用｜2～3 秒 → 可用，ISO 拉高｜只有 1 秒 → 效果受限，那晚改以 S23U 為主力。', '<b>設定大絕招：</b>務必裝上原廠「微距鏡頭配件」，才能在 M 手動模式下強制解鎖 f/2.0 最大光圈，且千萬不要用 Auto 模式 (快門會被鎖在 1 秒)。')

# Section: 現場流程
content = content.replace('<li>兩台電池充滿 ＋ <b>續航手柄</b>充滿 ＋ 行動電源</li>', '<li>兩台電池充滿 ＋ <b>Action 6 微距鏡頭配件</b> ＋ 行動電源</li>')
content = content.replace('<li><b>Luna Ultra 繼續跑，絕對不要動它</b></li>', '<li><b>Action 6 繼續跑，絕對不要動它</b></li>')

# Section: 防風
content = content.replace('Luna Ultra 的雲台防抖就是為手持而生', 'Action 6 的電子防抖極強')

# Section: 電池
content = content.replace('標配<b>續航手柄</b> ＋ 行動電源', '使用<b>極地防凍電池</b> ＋ 備用電池放口袋')

# Section: 出門前清單
content = content.replace('<li><label><input type="checkbox" data-id="c1"><span>Luna Ultra 電池滿 ＋ <b>續航手柄</b>滿</span></label></li>', '<li><label><input type="checkbox" data-id="c1"><span>Action 6 電池滿 ＋ <b>微距鏡頭配件</b></span></label></li>')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated aurora.html")
