from pathlib import Path
root=Path(__file__).resolve().parent
for name in ('app.js','app.bundle.js'):
    p=root/'web'/name;s=p.read_text(encoding='utf-8-sig')
    replacements={
      'uniform sampler2D tSubject, tBackground, tText, tLine, tEffects;':'''uniform sampler2D tSubject, tBackground, tText, tLine, tEffects, tTail, tGohei;
uniform float uTailDepth, uGoheiDepth;''',
      'vec3 col = mix(bg,subject.rgb,subject.a);':'''// Three registered cutouts: tail behind body; gohei is pinned at the grip.
  vec2 direction = uView.xy / max(abs(uView.z), .4) * .10 * uScale;
  vec2 tu = su + direction * (uTailDepth-uDepth);
  vec4 tail = texture2D(tTail,clamp(tu,0.,1.));
  float grip = smoothstep(.025,.20,distance(su,vec2(.664,.365)));
  vec2 gu = su + direction * (uGoheiDepth-uDepth) * grip;
  vec4 gohei = texture2D(tGohei,clamp(gu,0.,1.));
  vec3 col = mix(bg,tail.rgb,tail.a*inside(tu));
  col = mix(col,gohei.rgb,gohei.a*inside(gu));
  col = mix(col,subject.rgb,subject.a);''',
      'tEffects: { value: effects },':'''tEffects: { value: effects },
    tTail: { value: await textureLoader.loadAsync(config.assets.tail) },
    tGohei: { value: await textureLoader.loadAsync(config.assets.gohei) },
    uTailDepth: { value: config.characterLayers.tailDepth },
    uGoheiDepth: { value: config.characterLayers.goheiDepth },''',
      '["depth", "uDepth"],':'["depth", "uDepth"],\n  ["tail-depth", "uTailDepth"],\n  ["gohei-depth", "uGoheiDepth"],',
    }
    for old,new in replacements.items():
        if new not in s:
            assert old in s,(name,old)
            s=s.replace(old,new,1)
    # The additional controls use the existing settings event binding.
    old='"bg-depth": p.backgroundDepth ?? -0.18'
    assert old in s
    if '"tail-depth": config.characterLayers.tailDepth' not in s:
        s=s.replace(old,'"tail-depth": config.characterLayers.tailDepth,\n    "gohei-depth": config.characterLayers.goheiDepth,\n    '+old,1)
    p.write_text(s,encoding='utf8')
p=root/'web/index.html';s=p.read_text(encoding='utf-8-sig')
s=s.replace('<div class="panel-heading">','''<label class="range-row" for="tail-depth"><span>狐尾景深</span><output id="tail-depth-value"></output><input id="tail-depth" type="range" min="-0.8" max="0.5" step="0.01" /></label>
<label class="range-row" for="gohei-depth"><span>御币景深</span><output id="gohei-depth-value"></output><input id="gohei-depth" type="range" min="0" max="1.4" step="0.01" /></label>
<div class="panel-heading">''')
s=s.replace('铃响三界，福照此身。','照 · 三神御主')
p.write_text(s,encoding='utf8')
