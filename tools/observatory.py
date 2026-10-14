"""Original SVG art for the orbital data-station edition. No external assets."""
import math

MOTION = '''
.spin{animation:spin 36s linear infinite;transform-origin:600px 438px}
.counter{animation-direction:reverse;animation-duration:52s}
.breathe{animation:breathe 6s ease-in-out infinite}
.packet{stroke-dasharray:3 26;animation:packet 8s linear infinite}
.warp{stroke-dasharray:80 900;animation:packet 10s linear infinite}
.hover{animation:hover 8s ease-in-out infinite}
.blink{animation:blink 5s ease-in-out infinite}
.precess{animation:precess 18s ease-in-out infinite;transform-origin:600px 438px}
@keyframes spin{to{transform:rotate(360deg)}}
@keyframes breathe{50%{opacity:.45}}
@keyframes packet{to{stroke-dashoffset:-980}}
@keyframes hover{50%{transform:translateY(-12px)}}
@keyframes blink{50%{opacity:.15}}
@keyframes precess{50%{transform:rotate(9deg)}}
@media(prefers-reduced-motion:reduce){*{animation:none!important}}
'''

def hero(txt):
    stars=''.join(f'<circle cx="{(i*137+19)%1200}" cy="{(i*83+210)%640+160}" r="{.65+(i%3)*.45}" fill="{["#b6f5ef","#9e99ff","#fff1d2"][i%3]}" opacity="{.15+(i%5)*.12}" class="blink" style="animation-delay:-{i%7}s"/>' for i in range(100))
    ticks=''.join(f'<path d="M{600+233*math.cos(t):.2f} {438+233*math.sin(t):.2f}L{600+(244 if i%5==0 else 238)*math.cos(t):.2f} {438+(244 if i%5==0 else 238)*math.sin(t):.2f}"/>' for i in range(100) for t in [i*math.pi/50])
    grid=''.join(f'<path d="M600 490L{x} 820"/>' for x in range(-1800,3001,160))
    grid+=''.join(f'<path d="M0 {y}H1200"/>' for y in [545,560,579,604,637,681,739,815])
    rings=''
    for i in range(11):
        rings+=f'<ellipse cx="600" cy="438" rx="{175+i*9}" ry="{29+i*3.5}" transform="rotate(-25 600 438)" stroke="{["#70f0df","#8b87ff","#bba8ff"][i%3]}" stroke-opacity="{.12+i*.025}"/>'
    body=f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="830" viewBox="0 0 1200 830" role="img" aria-labelledby="title desc">
    <title id="title">Jackson — Orbital Data Station</title><desc id="desc">An original animated illustration of data travelling through an eclipse-like processing core into applications. Decorative concept art; not live telemetry. Python automation and React applications.</desc>
    <defs>
    <radialGradient id="nebula"><stop stop-color="#353167" stop-opacity=".8"/><stop offset=".5" stop-color="#12363e" stop-opacity=".45"/><stop offset="1" stop-color="#060a12" stop-opacity="0"/></radialGradient>
    <radialGradient id="corona"><stop offset=".64" stop-color="#050810"/><stop offset=".73" stop-color="#111b2c"/><stop offset=".79" stop-color="#9effed"/><stop offset=".81" stop-color="#edfff8"/><stop offset=".84" stop-color="#73cfdb" stop-opacity=".7"/><stop offset=".92" stop-color="#8582ff" stop-opacity=".12"/><stop offset="1" stop-color="#8582ff" stop-opacity="0"/></radialGradient>
    <linearGradient id="beam"><stop stop-color="#8c86ff" stop-opacity="0"/><stop offset=".5" stop-color="#bbfff1"/><stop offset="1" stop-color="#8c86ff" stop-opacity="0"/></linearGradient>
    <linearGradient id="type" x2="0.8" y2="1"><stop stop-color="#f4fff8"/><stop offset=".55" stop-color="#c9e9ec"/><stop offset="1" stop-color="#8e89db"/></linearGradient>
    <filter id="glow"><feGaussianBlur stdDeviation="5"/></filter>
    </defs><style>{MOTION}</style>
    <rect width="1200" height="830" rx="20" fill="#060a12"/>
    <ellipse cx="600" cy="442" rx="590" ry="350" fill="url(#nebula)"/>
    {stars}<g fill="none" stroke="#6cb6b3" stroke-opacity=".10">{grid}</g>
    <path d="M32 68V32h36m1064 0h36v36M32 762v36h36m1064 0h36v-36" fill="none" stroke="#749fba"/>
    {txt(48,59,'J / ORBITAL DATA STATION',14,'#a3d9d5','SpaceGrotesk',letter_spacing=2)}
    {txt(1152,59,'INDEPENDENT DEVELOPER',14,'#b4a4ef','SpaceGrotesk',text_anchor='end',letter_spacing=2)}
    {txt(600,202,'JACKSON',174,'url(#type)','SpaceGrotesk',text_anchor='middle',letter_spacing=-8)}
    <g opacity=".6"><path d="M60 438H1140" stroke="url(#beam)"/><path d="M600 264V672" stroke="#9ff3e5" stroke-opacity=".15"/></g>
    <g class="spin counter" fill="none" stroke="#6f9cba" stroke-opacity=".45">{ticks}</g>
    <circle cx="600" cy="438" r="185" fill="url(#corona)"/>
    <circle cx="600" cy="438" r="133" fill="#050a12"/>
    <g fill="none" class="precess">{rings}</g>
    <g class="spin" fill="none"><circle cx="600" cy="438" r="210" stroke="#9b8bff" stroke-opacity=".35" stroke-dasharray="300 170 70 780"/><circle cx="600" cy="228" r="5" fill="#c2fff0"/><path d="M600 228A210 210 0 0 1 810 438" stroke="#c2fff0" stroke-opacity=".8"/></g>
    <g class="spin counter"><circle cx="600" cy="670" r="4" fill="#c0a0ff"/><circle cx="600" cy="206" r="3" fill="#ffe0aa"/></g>
    <path d="M56 580C340 580 290 280 600 340S930 580 1144 320" fill="none" stroke="#9d8fff" stroke-opacity=".5"/>
    <path d="M56 580C340 580 290 280 600 340S930 580 1144 320" fill="none" stroke="#d0baff" stroke-width="3" class="warp"/>
    <path d="M64 330C350 330 320 640 600 560S900 310 1135 540" fill="none" stroke="#72e4d4" stroke-opacity=".3"/>
    <path d="M64 330C350 330 320 640 600 560S900 310 1135 540" fill="none" stroke="#aeffeb" stroke-width="2" class="packet"/>
    <g class="breathe"><path d="M555 438h28m34 0h28M600 393v28m0 34v28" stroke="#8caabb" stroke-opacity=".65"/>
    {txt(600,452,'{ j }',39,'#e0fff3','SpaceGrotesk',text_anchor='middle')}</g>
    <g class="hover"><rect x="64" y="370" width="177" height="100" rx="10" fill="#0b1725" stroke="#4a6c82"/>
    <path d="M82 395h48m-48 18h137m-137 18h106m-106 18h125" stroke="#739bad" stroke-opacity=".55"/>
    {txt(79,495,'01 / EXTRACT',13,'#9fe3d9','SpaceGrotesk',letter_spacing=2)}</g>
    <g class="hover" style="animation-delay:-4s"><rect x="966" y="405" width="171" height="111" rx="10" fill="#121326" stroke="#756296"/>
    <path d="M966 427h171m-138 0v89" stroke="#756296"/><path d="M1013 494v-29h22v29m12 0v-44h22v44m12 0v-58h22v58" fill="#7d73c7" fill-opacity=".3" stroke="#a59bdd"/>
    {txt(966,544,'03 / BUILD',13,'#c3b4ed','SpaceGrotesk',letter_spacing=2)}</g>
    {txt(600,652,'02 / TRANSFORM',13,'#a9c8ce','SpaceGrotesk',text_anchor='middle',letter_spacing=3)}
    <rect x="262" y="220" width="676" height="36" rx="18" fill="#060a12" fill-opacity=".96"/>
    {txt(600,244,'PYTHON AUTOMATION   /   REACT APPLICATIONS',16,'#a3b9d1','SpaceGrotesk',text_anchor='middle',letter_spacing=3)}
    {txt(48,745,'I make data move.',55,'#edf6ef','SpaceGrotesk')}
    {txt(1152,740,'FROM SOURCE TO SCREEN',14,'#b0ddd1','SpaceGrotesk',text_anchor='end',letter_spacing=2)}
    <path d="M48 770H1152" stroke="#3d465e"/><path d="M48 770H1152" stroke="#b6a2f0" class="warp"/>
    {txt(48,800,'CONCEPTUAL WORKFLOW / REAL PROJECTS BELOW',12,'#8ea4ba','SpaceGrotesk',letter_spacing=1)}
    <circle cx="943" cy="795" r="3" fill="#adffdb" class="blink"/>
    {txt(959,800,'OPEN TO REMOTE WORK',12,'#b9e5cd','SpaceGrotesk')}
    </svg>'''
    return body

def motif(kind):
    """Distinct small animated machines; deliberately separate from evidence."""
    art='<g fill="none" stroke-width="1.2">'
    if kind=='court':
        for i in range(7):
            t=i*math.pi*2/7
            x,y=1018+97*math.cos(t),106+61*math.sin(t)
            art+=f'<path d="M1018 106L{x:.2f} {y:.2f}" stroke="#7bcabc" opacity=".45"/><circle cx="{x:.2f}" cy="{y:.2f}" r="{6+i%3*2}" stroke="#a1f3d9" class="pulse" style="animation-delay:-{i}s"/>'
        art+='<circle cx="1018" cy="106" r="29" stroke="#9b8deb"/><rect x="1008" y="94" width="20" height="24" rx="2" stroke="#a5edd3"/>'
    elif kind=='reports':
        for i in range(5):
            x=902+i*39;y=89+(i%2)*16
            art+=f'<g class="drift" style="animation-delay:-{i}s"><path d="M{x} {y}l27-14 23 12v48l-50 4Z" fill="#152430" stroke="#9b9ae4"/><path d="M{x+9} {y+12}l30-3m-30 12 23-2m-23 12 30-3" stroke="#75b6bf"/></g>'
        art+='<path d="M910 167H1140" stroke="#a69bf0" class="trace"/>'
    else:
        for i in range(3):
            y=63+i*30
            art+=f'<g class="drift" style="animation-delay:-{i*2}s"><path d="M930 {y+30}l91-32 92 32-92 35Z" fill="#131c2e" stroke="{["#9489e0","#7ebdd5","#9bead4"][i]}"/><path d="M930 {y+30}v10l91 35 92-35v-10M1021 {y+65}v10" stroke="#62738c"/></g>'
    return art+'</g>'

def backdrop(h):
    # Sparse luminous edge work avoids passing animation over readable copy.
    return f'''<path d="M14 85V24h110M1186 {h-85}v61h-110" fill="none" stroke="#7f7ac7" stroke-opacity=".65"/>
    <path d="M14 100V{h-100}M1186 100V{h-100}" stroke="#364b63" stroke-opacity=".55"/>
    <path d="M14 100V{h-100}M1186 100V{h-100}" stroke="#94baf9" class="trace"/>
    <circle cx="1153" cy="24" r="2" fill="#9ce7d1" class="pulse"/>
    <circle cx="1139" cy="24" r="2" fill="#b6a2f0" class="pulse delay"/>'''
