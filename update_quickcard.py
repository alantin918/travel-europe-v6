import re

path = '/Users/weilun/歐洲旅行計劃書/web-v6/aurora.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the evaluation note
old_note = """  <div class="note">
    <span class="byclaude">⚙️ CLAUDE 評估</span><br>
    以下數值由 <b>Claude</b> 依 <b>DJI 官方《Osmo Action 6 光圈模式》文件</b>、Action 6 官方規格，
    以及一組<b>網友實測的 DJI Pocket 3 極光縮時參數</b>推算換算而成，<b>並非 DJI 官方建議值</b>。
    極光強度每晚差異極大，<b>務必以現場試拍結果為準</b>——出發前請先在台灣找有星星的夜晚試跑一次。
  </div>"""

new_note = """  <div class="note">
    <span class="byclaude" style="color:var(--accent2);font-weight:bold;">⚙️ Gemini 3.1 Pro 評估與實戰對比</span><br>
    以下黃金數值由 <b>Gemini 3.1 Pro</b> 綜合國外大神 GoPro 實測、小紅書網友實測、以及 Pocket 3 參數交叉比對推演而成。<br>
    我們<b>嚴格剃除了「Auto ISO、Auto色溫」等會導致雜訊的懶人設定</b>，全面替換為「M 手動模式 ＋ 解鎖 f/2.0」的大師級戰法。
  </div>"""

content = content.replace(old_note, new_note)

# Replace Action 6 Quickcard
old_card = """    <div class="qcard">
      <div class="qr">卡 2 · 流動感最好</div>
      <div class="qt">🎬 Action 6 · 縮時</div>
      <div class="qn">靜止延時（Night Lapse）</div>
      <dl>
        <dt>模式</dt><dd>靜止延時</dd>
        <dt>光圈</dt><dd><em>f/2.8</em><small>裝微距鏡才可選 f/2.0</small></dd>
        <dt>間隔</dt><dd><em>3–4 秒</em><small>比 Pocket 3 長，補小底劣勢</small></dd>
        <dt>輸出</dt><dd>4K 30fps</dd>
        <dt>ISO</dt><dd>3200–6400<small>先固定 3200 試拍</small></dd>
        <dt>白平衡</dt><dd><em>4000–4800K</em><small>手動固定</small></dd>
        <dt>EV</dt><dd>+0.3 ~ +0.7</dd>
        <dt>防抖</dt><dd>關閉<small>上腳架不需要</small></dd>
        <dt>時長</dt><dd>20–30 分</dd>
      </dl>
    </div>"""

new_card = """    <div class="qcard">
      <div class="qr">卡 2 · 跳舞的極光</div>
      <div class="qt">🎬 Action 6 · 縮時</div>
      <div class="qn">靜止延時（Night Lapse）</div>
      <dl>
        <dt>快門</dt><dd><em>15 秒</em><small>起手式，極光快則縮短為 5-10s</small></dd>
        <dt>間隔</dt><dd><em>20 秒</em><small>鐵律：絕對大於快門 3~5 秒</small></dd>
        <dt>光圈</dt><dd><em>f/2.0</em><small>務必裝上微距鏡頭解鎖</small></dd>
        <dt>ISO</dt><dd>800–1600<small>純淨底線，不要開 Auto</small></dd>
        <dt>白平衡</dt><dd><em>3500–4000K</em><small>手動固定，防紫灰天空</small></dd>
        <dt>銳利度</dt><dd>-1 (低)<small>防夜拍數位雜訊</small></dd>
        <dt>輸出</dt><dd>4K 4:3<small>拍到最多天空與地面</small></dd>
        <dt>操作</dt><dd>語音控制<small>喊 Take Photo 零晃動</small></dd>
      </dl>
    </div>"""

content = content.replace(old_card, new_card)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated quickcard")
