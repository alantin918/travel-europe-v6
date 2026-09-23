import re

path = '/Users/weilun/歐洲旅行計劃書/web-v6/index.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace Harpa to Sægreifinn walking
old_walk = """          <li><i>18:05<br>18:15</i><p>🚶 <b>走去 Sægreifinn「海怪」</b>（Geirsgata 8）—— 🔑 <b>從哈帕走過去只要 6 分鐘，兩個都在舊港</b>。</p></li>"""
new_walk = """          <li><i>18:05<br>18:15</i><p>🚶 <b>走去 Svarta Kaffið 麵包湯</b>（Laugavegur 54）—— 🔑 <b>從哈帕走回主街大約 10 分鐘</b>。</p></li>"""
content = content.replace(old_walk, new_walk)

# Replace Sægreifinn dinner
old_dinner = """          <li><i>18:15<br>19:00</i><p>🦞 <b>晚餐：Sægreifinn 龍蝦湯 ＋ 烤魚串</b>（約兩人 <b>2,600 元</b>）。<br>🔄 <b>2026-09-11 改：原本這格是「吃一頓好的」8,000–12,000。</b><br>🔑 <b>改的理由是疲勞管理，不是省錢</b> —— 今天要連走 <b>8.5 小時、約 6 公里</b>，其中一段上坡、一半在 0–3 度的黑夜裡，而<b>隔天 09:00 就要出三日團</b>（全程最貴的一筆，約 61,578）。<b>龍蝦湯 30 分鐘吃完，正式餐廳要 90 分鐘</b>。<br>🏆 <b>而「吃一頓好的」移到倫敦 11/20 的 Blacklock</b> —— 那天本來就排好了，<b>所以沒有真的失去什麼</b>。<br>⚠️ <b>只有約 20 個座位，可能要排 10–15 分</b>，但 ✅ <b>營業時間已查證：淡季每日 11:30–22:00</b>（旺季 5/15–9/15 到 23:00，11 月算淡季）。<br>✅ <b>所以 18:15 這格有近 4 小時餘裕，時間上完全沒有壓力 —— 唯一的變數只剩排隊</b>。🟡 <b>備案：Grandi Mathöll 美食廣場（每日 11:00–21:00）</b>，就在下一站 Omnom 隔壁，選擇多、一定有位。</p></li>"""
new_dinner = """          <li><i>18:15<br>19:00</i><p>🥣 <b>晚餐：Svarta Kaffið 麵包湯</b>（約兩人 <b>1,500 元</b>）。<br>🔄 <b>2026-09-23 改：依據指令，取消龍蝦湯，改吃市區最著名的麵包湯。</b><br>🔑 <b>這間店在主街上非常熱門，只有兩種口味（通常是肉湯跟素湯）</b>。直接把熱湯裝在挖空的酸種麵包裡，吃完湯再把吸滿湯汁的麵包吃掉，在零度的冰島吃這個非常滿足且保暖。<br>⚠️ <b>由於後續行程全數取消，吃完晚餐就可以慢慢散步回飯店，獲得極度充足的睡眠。</b>（如果需要買明天的零食，可在回程路上的超商解決）。</p></li>"""
content = content.replace(old_dinner, new_dinner)

# Remove the rest from 19:00 to 21:00
old_omnom = """          <li><i>19:00<br>19:10</i><p>🚕 <b>叫車去 Grandi 舊港西端</b>（約 4 分、ISK 約 2,000 ≈ <b>520 元</b>）。💡 走路 15 分、沿海風大又全黑 —— <b>這 520 元很值得</b>。</p></li>
          <li><i>19:10<br>19:50</i><p>🍫 <b>Omnom 巧克力工廠店</b>（Hólmaslóð 4・<b>每日 11:00–20:30</b>）—— 工廠直營，包裝設計極美，<b>伴手禮一次買完</b>。<br>✅ <b>20:30 才關，還有 40 分鐘緩衝，完全不用趕</b>。<br>🍦 <b>順便吃招牌冰淇淋</b> —— 在零度的冰島吃冰是當地人的日常，而且<b>剛好接在龍蝦湯後面當甜點</b>。</p></li>
          <li><i>19:50<br>20:20</i><p>🛒 <b>Krónan 超市 · Grandi 分店</b>（<b>每日 09:00–21:00</b>，就在 Omnom 旁邊）—— <b>甘草糖、海鹽，以及明天三日團要帶的麵包火腿起司</b>（團費不含午晚餐，沿途休息站一餐 ISK 3,000–4,000）。<br>🔴 <b>要去 Krónan 不是 Bónus</b> —— Bónus 週六 <b>19:00</b> 就關。⚠️ <b>要先確認 ASKA Holt 有冰箱</b>，生鮮要放到隔天 09:00。</p></li>
          <li><i>20:20<br>20:35</i><p>🚕 <b>叫車回 ASKA Holt</b> —— ✅ <b>20:35 收工，比原本的 21:45 早了 1 小時 10 分</b>。<br>🧳 <b>然後收行李</b>：大行李隔天丟上導遊拖車（每人 1 件 <b>20kg</b>、三邊之和 <b>≤158cm</b>），<b>小背包裝三天的隨身物</b>。<br>😴 <b>22:00 睡 → 07:30 起床 ＝ 9.5 小時</b> —— 🔑 <b>這才是整個重排真正要買到的東西</b>。</p></li>
          <li><i>21:00</i><p>🌌 <b>（選・我建議跳過）</b>　<b>Grótta 燈塔</b>（市區最西端，免費、光害低，走／搭車 20 分）。<br>🎯 <b>11/15、11/16 住教堂鎮光害極低，機會好得多</b> —— 🔴 <b>今晚的重點是睡飽</b>。除非 vedur.is 顯示 KP 高又剛好晴天，否則直接睡。⚠️ <b>真要去，先把行李收完再出門。</b></p></li>"""
new_omnom = """          <li><i>19:15<br>19:40</i><p>🚶 <b>散步回 ASKA Holt</b> —— ✅ <b>取消 Omnom 與後續行程，提早收工回飯店！</b><br>🧳 <b>收行李</b>：大行李隔天丟上導遊拖車（每人 1 件 <b>20kg</b>、三邊之和 <b>≤158cm</b>），<b>小背包裝三天的隨身物</b>。<br>😴 <b>21:00 就能睡覺 → 07:30 起床 ＝ 高達 10.5 小時的完美睡眠！</b> 為了明天 09:00 的三日團保留最完整的體力，這絕對是最高明的戰略捨棄。</p></li>"""
content = content.replace(old_omnom, new_omnom)

# Find and remove references that say 龍蝦湯不是
content = content.replace("🔴 <b>那是這趟唯一的冰島海鮮</b>（龍蝦湯 ＋ 烤魚串，兩人約 2,600 元）。<b>麵包湯在冰島到處都有，龍蝦湯不是。</b><br>", "")
content = content.replace("🔴 <b>代價是放棄 Sægreifinn 的龍蝦湯與烤魚串</b> —— 那是這天唯一的海鮮，而<b>麵包湯在冰島到處都有、龍蝦湯不是</b>。</p></div></div>", "</p></div></div>")
content = content.replace("🦞 <b>Sægreifinn 龍蝦湯 ＋ 烤魚串</b>", "🥣 <b>Svarta Kaffið 麵包湯</b>")

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Done")
