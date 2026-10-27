"""Procedural four-dimensional sculpture, rendered as self-contained SVG/CSS."""
import math


def sculpture(phase):
    vertices = []
    for i in range(16):
        v = [1 if i & (1 << j) else -1 for j in range(4)]
        for a, b, angle in [(0, 3, phase), (1, 2, phase / 1 + .45), (0, 2, .62), (1, 3, .37)]:
            c, s = math.cos(angle), math.sin(angle)
            v[a], v[b] = v[a] * c - v[b] * s, v[a] * s + v[b] * c
        perspective = 3.8 / (3.8 - v[3])
        x, y, z = [q * perspective for q in v[:3]]
        depth = 5.5 / (5.5 - z)
        vertices.append((600 + x * depth * 87, 465 + y * depth * 87))
    return ' '.join(f'M{vertices[i][0]:.2f},{vertices[i][1]:.2f}L{vertices[j][0]:.2f},{vertices[j][1]:.2f}'
                    for i in range(16) for k in range(4) for j in [i ^ (1 << k)] if i < j)


def hero(txt):
    frames = ''.join(f'{i / 24 * 100:.4f}%{{d:path("{sculpture(i * math.tau / 24)}")}}' for i in range(25))
    ribbons = ''
    for i in range(26):
        y = 340 + i * 8
        path = f'M-80 {y}C180 {y-150} 320 {710-i*5} 600 {570-i*7}S1000 {190+i*6} 1280 {480+i*4}'
        ribbons += f'<path d="{path}" stroke="url(#ribbon)" stroke-opacity="{.13+(i%5)*.035}"/>'
        if i % 6 == 0:
            ribbons += f'<path d="{path}" stroke="#a4edff" stroke-opacity=".8" class="flow" style="animation-delay:-{i/3}s"/>'
    stars = ''.join(f'<circle cx="{(i*173+37)%1200}" cy="{(i*97+91)%840}" r="{.6+(i%3)*.3}" fill="#b2c9ff" opacity="{.15+(i%5)*.09}"/>' for i in range(100))
    floor = ''.join(f'<path d="M600 570L{x} 900"/>' for x in range(-2200,3400,190))
    floor += ''.join(f'<path d="M0 {y}H1200"/>' for y in [625,645,672,708,755,818,898])
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="940" viewBox="0 0 1200 940" role="img" aria-labelledby="title desc">
    <title id="title">Jackson / Beyond the interface</title>
    <desc id="desc">A rotating four-dimensional data sculpture, luminous flowing ribbons and an oversized custom letterform composition. Conceptual motion artwork. Python automation, React applications, real project evidence below.</desc>
    <defs>
    <radialGradient id="aura"><stop stop-color="#49339b" stop-opacity=".65"/><stop offset=".52" stop-color="#153950" stop-opacity=".45"/><stop offset="1" stop-color="#070a12" stop-opacity="0"/></radialGradient>
    <linearGradient id="chrome" x1="0" y1="0" x2=".7" y2="1"><stop stop-color="#fff"/><stop offset=".4" stop-color="#dcfaff"/><stop offset=".64" stop-color="#91a4cc"/><stop offset=".7" stop-color="#e5e4ff"/><stop offset="1" stop-color="#8c79cd"/></linearGradient>
    <linearGradient id="ribbon"><stop stop-color="#6c5fff"/><stop offset=".5" stop-color="#a2fff1"/><stop offset="1" stop-color="#aa73ff"/></linearGradient>
    <linearGradient id="fade"><stop stop-color="#8b6fff" stop-opacity="0"/><stop offset=".5" stop-color="#c0faff"/><stop offset="1" stop-color="#8b6fff" stop-opacity="0"/></linearGradient>
    <filter id="glow"><feGaussianBlur stdDeviation="5"/></filter>
    </defs>
    <style>
    .fold{{animation:fold 28s linear infinite}}@keyframes fold{{{frames}}}
    .flow{{stroke-dasharray:80 1600;animation:flow 9s linear infinite}}@keyframes flow{{to{{stroke-dashoffset:-1680}}}}
    .orbit{{transform-origin:600px 465px;animation:orbit 45s linear infinite}}@keyframes orbit{{to{{transform:rotate(360deg)}}}}
    .rise{{animation:rise 7s ease-in-out infinite}}@keyframes rise{{50%{{transform:translateY(-10px)}}}}
    .signal{{animation:signal 4s ease-in-out infinite}}@keyframes signal{{50%{{opacity:.35}}}}
    @media(prefers-reduced-motion:reduce){{*{{animation:none!important}}}}
    </style>
    <rect width="1200" height="940" rx="20" fill="#070a12"/>
    <ellipse cx="600" cy="470" rx="610" ry="410" fill="url(#aura)"/>{stars}
    <g fill="none" stroke="#6f98cf" opacity=".12">{floor}</g>
    <path d="M36 80V36h44m1040 0h44v44M36 860v44h44m1040 0h44v-44" fill="none" stroke="#60759f"/>
    {txt(56,65,'J / INDEPENDENT DEVELOPER',13,'#b8c6e0','SpaceGrotesk',letter_spacing=2)}
    {txt(1144,65,'CODE × DATA × INTERFACES',13,'#c6bbeb','SpaceGrotesk',text_anchor='end',letter_spacing=2)}
    {txt(600,211,'JACKSON',202,'url(#chrome)','SpaceGrotesk',text_anchor='middle',letter_spacing=-9)}
    {txt(600,252,'BEYOND THE INTERFACE',14,'#bed2eb','SpaceGrotesk',text_anchor='middle',letter_spacing=7)}
    <g fill="none" stroke-width="1">{ribbons}</g>
    <g fill="none" stroke="#849af2" opacity=".4"><ellipse cx="600" cy="465" rx="315" ry="112" transform="rotate(-25 600 465)"/><ellipse cx="600" cy="465" rx="315" ry="112" transform="rotate(25 600 465)"/></g>
    <g class="orbit" fill="none"><circle cx="600" cy="465" r="268" stroke="#a99dff" stroke-opacity=".25" stroke-dasharray="2 15"/><circle cx="600" cy="197" r="4" fill="#d2ccff"/></g>
    <path d="{sculpture(0)}" class="fold" fill="none" stroke="#82baff" stroke-width="5" opacity=".45" filter="url(#glow)"/>
    <path d="{sculpture(0)}" class="fold" fill="none" stroke="url(#ribbon)" stroke-width="1.6" stroke-linejoin="round"/>
    <g class="rise"><path d="M77 390h125l26 26v70H77Z" fill="#0b1321" stroke="#415575"/>
    {txt(92,415,'INPUT / 01',12,'#a5a2f5','SpaceGrotesk',letter_spacing=1)}
    <path d="M93 436h98m-98 13h72m-72 13h86" stroke="#7b9cae" stroke-opacity=".65"/>
    {txt(78,513,'EXTRACT',14,'#c9d7ea','SpaceGrotesk',letter_spacing=3)}</g>
    <g class="rise" style="animation-delay:-3s"><path d="M974 443h130l22 22v81H974Z" fill="#101224" stroke="#5e4c85"/>
    {txt(990,471,'OUTPUT / 03',12,'#a6e9de','SpaceGrotesk',letter_spacing=1)}
    <path d="M990 522v-20h20v20m12 0v-32h20v32m12 0v-42h20v42m12 0v-54h20v54" fill="#a59bef" fill-opacity=".12" stroke="#a59bef"/>
    {txt(974,575,'BUILD',14,'#c9d7ea','SpaceGrotesk',letter_spacing=3)}</g>
    {txt(600,723,'02 / TRANSFORM THE COMPLEX',12,'#a8b7d6','SpaceGrotesk',text_anchor='middle',letter_spacing=3)}
    <path d="M100 755H1100" stroke="url(#fade)" stroke-opacity=".45"/>
    {txt(600,816,'Raw data. Real possibilities.',53,'#f0f3ff','SpaceGrotesk',text_anchor='middle',letter_spacing=-1)}
    {txt(600,859,'PYTHON AUTOMATION / REACT APPLICATIONS',15,'#b4bed6','SpaceGrotesk',text_anchor='middle',letter_spacing=3)}
    <circle cx="63" cy="904" r="3" fill="#a4efda" class="signal"/>
    {txt(78,909,'REMOTE / PART-TIME',12,'#a4c8c6','SpaceGrotesk',letter_spacing=1)}
    {txt(1144,909,'SCROLL TO EXPLORE THE WORK ↓',12,'#b4aacd','SpaceGrotesk',text_anchor='end',letter_spacing=1)}
    </svg>'''


def transit(txt):
    art = ''
    for i in range(15):
        art += f'<path d="M-40 {48+i*4}C280 {-75+i*14} 720 {230-i*13} 1240 {42+i*4}" fill="none" stroke="url(#ribbon)" stroke-opacity=".3"/>'
    return art + '<rect x="365" y="40" width="470" height="66" rx="33" fill="#080d13" stroke="#514778"/>' + txt(600,81,'SELECTED WORK / REAL EVIDENCE',16,'#d2d7f3','SpaceGrotesk',text_anchor='middle',letter_spacing=2)
