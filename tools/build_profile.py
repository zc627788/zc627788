"""Build the GitHub portfolio. Python 3 + fonttools; all assets stay in this repo.

Fonts use the SIL Open Font License (see assets/fonts). Text becomes SVG paths
so the intended typefaces work without remote font requests. SVG titles, image
alt text and the text edition retain accessible descriptions. No live counters.
"""
from pathlib import Path
from html import escape
import base64
import hashlib
import re
import xml.etree.ElementTree as ET
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from fontTools.pens.svgPathPen import SVGPathPen
import observatory

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'assets'
NS = 'http://www.w3.org/2000/svg'
ET.register_namespace('', NS)
FONTS = {}
for name, weight in [('SpaceGrotesk', 600), ('Manrope', 450)]:
    f = instantiateVariableFont(TTFont(A/'fonts'/f'{name}.ttf'), {'wght': weight})
    FONTS[name] = (f.getGlyphSet(), f.getBestCmap(), f['head'].unitsPerEm)

STYLE = '''
.drift{animation:drift 7s ease-in-out infinite}.pulse{animation:pulse 4s ease-in-out infinite}
.trace{stroke-dasharray:32 240;animation:trace 6s linear infinite}
.slow{animation-duration:11s}.delay{animation-delay:-3s}
.scan{animation:scan 8s ease-in-out infinite}
@keyframes drift{50%{transform:translateY(-7px)}}
@keyframes pulse{50%{opacity:.32}}
@keyframes trace{to{stroke-dashoffset:-544}}
@keyframes scan{50%{transform:translateX(80px);opacity:.25}}
@media(prefers-reduced-motion:reduce){*{animation:none!important}}
'''

def txt(x, y, s, size=22, color='#a8bab9', face='Manrope', **attrs):
    extra=' '.join(f'{k.replace("_","-")}="{v}"' for k,v in attrs.items())
    return f'<text x="{x}" y="{y}" font-family="{face}" font-size="{size}" fill="{color}" {extra}>{escape(s)}</text>'

def outline(root):
    def visit(el, inherited):
        style = dict(inherited)
        style.update(el.attrib)
        for child in list(el):
            if child.tag != f'{{{NS}}}text':
                visit(child, style)
                continue
            attrs = dict(style); attrs.update(child.attrib)
            label = ''.join(child.itertext())
            size = float(attrs.get('font-size',22))
            face = attrs.get('font-family','SpaceGrotesk')
            face = face if face in FONTS else ('SpaceGrotesk' if size>=28 else 'Manrope')
            glyphs,cmap,em = FONTS[face]
            scale = size/em
            spacing = float(attrs.get('letter-spacing',0))
            widths = [glyphs[cmap.get(ord(c),'.notdef')].width*scale+spacing for c in label]
            w = sum(widths)-spacing if widths else 0
            x,y = float(attrs.get('x',0)),float(attrs.get('y',0))
            if attrs.get('text-anchor')=='end': x-=w
            elif attrs.get('text-anchor')=='middle': x-=w/2
            viewport_width = float(root.attrib['viewBox'].split()[2])
            if x < -0.1 or x+w > viewport_width+0.1:
                raise ValueError(f'Text exceeds the viewBox: {label}')
            missing = [c for c in label if ord(c) not in cmap]
            if missing:
                raise ValueError(f'Missing font glyphs: {missing}')
            group = ET.Element(f'{{{NS}}}g', {'aria-label':label})
            for attr in ['fill','opacity','class','transform']:
                if attr in child.attrib: group.set(attr,child.attrib[attr])
                elif attr=='fill' and attr in attrs: group.set(attr,attrs[attr])
            for c,advance in zip(label,widths):
                pen=SVGPathPen(glyphs)
                glyphs[cmap.get(ord(c),'.notdef')].draw(pen)
                d=pen.getCommands()
                if d: ET.SubElement(group,f'{{{NS}}}path',{'d':d,'transform':f'translate({x:.3f} {y:.3f}) scale({scale:.6f} {-scale:.6f})'})
                x+=advance
            idx=list(el).index(child); el.remove(child); el.insert(idx,group)
    visit(root,{})

def save(name, content):
    root=ET.fromstring(content)
    outline(root)
    (A/name).write_text(ET.tostring(root,encoding='unicode'),encoding='utf-8')

def panel(name,h,title,body):
    save(name,f'''<svg xmlns="{NS}" width="1200" height="{h}" viewBox="0 0 1200 {h}" role="img" aria-labelledby="title"><title id="title">{escape(title)}</title>
    <defs><linearGradient id="wash" x2="1" y2="1"><stop stop-color="#30264f"/><stop offset="1" stop-color="#080d13"/></linearGradient>
    <pattern id="grid" width="36" height="36" patternUnits="userSpaceOnUse"><path d="M36 0H0V36" fill="none" stroke="#93bfae" stroke-opacity=".035"/></pattern></defs>
    <style>{STYLE}</style><rect width="1200" height="{h}" rx="18" fill="#080d13"/><rect width="1200" height="{h}" rx="18" fill="url(#grid)"/>
    {observatory.backdrop(h) if h>200 else ''}{body}<path d="M44 {h-2}H1156" stroke="#373450"/><path d="M44 {h-2}H1156" stroke="#b1a1ff" stroke-opacity=".7" class="trace"/></svg>''')

# The eclipse echoes the existing profile avatar; its animation is conceptual.
save('orbit-header.svg',observatory.hero(txt))

panel('intro-panel.svg',260,'Python automation and full-stack delivery. Jackson builds web extraction tools, document workflows and React applications.',
      txt(44,46,'THE MISSION / TURN COMPLEXITY INTO SOMETHING USEFUL',15,'#b9a7ed','SpaceGrotesk',letter_spacing=1)+
      txt(44,104,'Less manual work. More useful software.',42,'#edf2e9','SpaceGrotesk')+
      txt(44,154,'I build Python tools that collect and organize data, then React applications that put it to work.',21)+
      txt(44,190,'Web extraction, document workflows and business systems — from API to screen.',21)+
      '<g class="drift"><path d="M44 228h40m18 0h40m18 0h40" stroke="#9bd5be" stroke-width="2"/></g>'+
      txt(1156,232,'INDEPENDENT DEVELOPER / SELECTED WORK BELOW',13,'#91aaa5',text_anchor='end'))

stack=''
for i,(label,x) in enumerate([('PYTHON',44),('REACT',240),('TYPESCRIPT',420),('NEXT.JS',680),('FASTAPI',880),('SQL',1090)]):
    stack+=txt(x,113,label,20,'#c1d5cb','SpaceGrotesk')
    stack+=f'<g class="drift" style="animation-delay:-{i}s"><path d="M{x+16} 26l27 15v29l-27 15-27-15V41Z" fill="#172139" stroke="#8a89cf"/><path d="M{x+16} 26v59m-27-44 54 29m0-29-54 29" stroke="#8cd8c9" stroke-opacity=".65"/><circle cx="{x+16}" cy="55" r="4" fill="#b9ecd3" class="pulse" style="animation-delay:-{i*.6}s"/></g>'
panel('stack-strip.svg',145,'Python, React, TypeScript, Next.js, FastAPI, SQL',stack)

def project(name,no,category,title,sub,metric,metric_label,lines,screenshot,proof):
    png=base64.b64encode((A/screenshot).read_bytes()).decode()
    body=observatory.motif('court' if 'court' in name else 'reports' if 'reports' in name else 'opc')
    body+=txt(44,47,category,15,'#b9a7ed','SpaceGrotesk',letter_spacing=2)
    body+=txt(1156,47,no,15,'#b6cfc2','SpaceGrotesk',text_anchor='end')
    body+=txt(44,119,title,45,'#edf2e9','SpaceGrotesk')+txt(44,162,sub,21)
    body+=txt(44,250,metric,66,'#b8ebd1','SpaceGrotesk')+txt(44,289,metric_label,20)
    for i,line in enumerate(lines): body+=txt(44,361+i*36,line,21)
    body+='<path d="M620 330v180" stroke="#2d4540"/><path d="M620 330v180" stroke="#c8e7d4" class="trace"/>'
    body+='<rect x="667" y="210" width="494" height="320" rx="14" fill="none" stroke="#8b7bbb" stroke-opacity=".25" class="pulse"/><rect x="672" y="215" width="484" height="310" rx="11" fill="#101c21" stroke="#776696"/>'
    body+=txt(690,243,'ACTUAL OUTPUT / PROJECT EVIDENCE',12,'#c3d8cc','SpaceGrotesk',letter_spacing=1)
    body+='<circle cx="1137" cy="238" r="3" fill="#c8af89" class="pulse"/>'
    body+=f'<image x="686" y="258" width="456" height="252" preserveAspectRatio="xMidYMid meet" href="data:image/png;base64,{png}"/>'
    # Decorative corner marks move; the actual screenshot remains unchanged.
    body+='<g class="drift slow" fill="none" stroke="#aacbb9"><path d="M660 270v-20h20m464 263h24v-24"/></g>'
    body+=txt(44,574,proof,14,'#93aaa4')+txt(1156,574,'EXPLORE THE PROJECT ↗',14,'#cfb58c','SpaceGrotesk',text_anchor='end')
    panel(name,610,title+'. '+metric+' '+metric_label+'. '+' '.join(lines)+' '+proof,body)

project('project-court.svg','01 / 03','DATA EXTRACTION','Court document collection',
        'Web protocol analysis / partitioned tasks / saved checkpoints','7,296','distinct document IDs in verified saved output',
        ['Re-exported into a 12-column CSV.','Recovered 955 records missing from the older CSV.','Partitioned tasks and checkpoints support restarts.','Historical output audit; no new live crawl tested.'],
        'court-evidence.png','SAVED OUTPUT AUDIT / REDACTED SAMPLE AVAILABLE')
project('project-reports.svg','02 / 03','DOCUMENT AUTOMATION','Rating report pipeline',
        'Issuer search / PDF downloads / duplicate checks','15 → 10','downloaded PDFs → unique files',
        ['Download reports and retain their source links.','Flag identical files with SHA-256 hashes.','Deliver an Excel inventory for review.','Live sample: one issuer, first listing page.'],
        'reports-evidence.png','LIVE SAMPLE / 182 PAGES ACROSS THE UNIQUE FILES')
project('project-opc.svg','03 / 03','FULL-STACK APPLICATION','OPC business portal',
        'Next.js portal / React admin / FastAPI backend','UI → API → DB','a verified product-management demo',
        ['Sign in, create a product, reload: the record stays.','Original React UI and product API routes.','Isolated SQLite demo with fictional products.','Payments are mocked; integrations not exercised.'],
        'opc-demo.png','ACTUAL LOCAL DEMO / SOURCE AND RUN INSTRUCTIONS INCLUDED')

panel('contact-panel.svg',330,'Open to scoped remote, part-time projects, around 24 hours per week. Written updates and clear handover. Contact Jackson on Upwork or Eleduck.',
      '<ellipse cx="1110" cy="170" rx="220" ry="160" fill="url(#wash)"/>'+
      txt(44,49,'NEXT TRANSMISSION / YOUR PROJECT',15,'#b9a7ed','SpaceGrotesk',letter_spacing=2)+
      txt(44,117,'Have a workflow that needs fixing?',45,'#edf2e9','SpaceGrotesk')+
      txt(44,169,'A scraper repair. A document pipeline. A defined React or admin feature.',22)+
      txt(44,207,'Send the current workflow, the result you need and your deadline.',22)+
      txt(44,245,'Small first milestone. Written updates. Clear handover notes.',22)+
      '<circle cx="49" cy="294" r="4" fill="#b9ecd3" class="pulse"/>'+
      txt(64,300,'REMOTE / PART-TIME / ~24 HOURS A WEEK',15,'#bdd9c9','SpaceGrotesk')+
      '<g fill="none" stroke="#b4a0eb" stroke-opacity=".7" class="pulse"><circle cx="1080" cy="255" r="35"/><circle cx="1080" cy="255" r="55"/><circle cx="1080" cy="255" r="75"/></g><path d="M970 282h145m-18-18 18 18-18 18" stroke="#a6f5df" stroke-width="2" fill="none" class="scan"/>')

def button(file,label):
    panel(file,90,label,txt(44,53,label,22,'#cbded2','SpaceGrotesk')+
          '<circle cx="1127" cy="45" r="5" fill="#cdb18b" class="pulse"/>')
for file,label in [('link-court.svg','01 / VIEW THE FULL AUDIT & REDACTED SAMPLE ↗'),
                   ('link-reports.svg','02 / INSPECT THE DOWNLOAD MANIFEST ↗'),
                   ('link-opc.svg','03 / OPEN THE ORIGINAL DEMO SCREENSHOT ↗')]: button(file,label)

# Three independently clickable footer tiles; no links hidden inside SVG images.
for file,label in [('link-upwork.svg','UPWORK ↗'),('link-eleduck.svg','ELEDUCK ↗'),('link-text.svg','TEXT / ZH ↗')]:
    save(file,f'<svg xmlns="{NS}" width="390" height="88" viewBox="0 0 390 88" role="img"><title>{escape(label)}</title><style>{STYLE}</style><rect width="390" height="88" rx="12" fill="#10201f"/><path d="M24 86h342" stroke="#9ac6af" class="trace"/>{txt(28,53,label,22,"#cdded1","SpaceGrotesk")}<circle cx="354" cy="44" r="3" fill="#cdb18b" class="pulse"/></svg>')

panel('colophon.svg',100,'Evidence checked in October 2026. Animation is conceptual, screenshots are real outputs. Fonts: Space Grotesk and Manrope, SIL OFL.',
      txt(44,40,'REAL OUTPUTS. REPRODUCIBLE WORK. NO LIVE TELEMETRY.',14,'#9eb5ac','SpaceGrotesk',letter_spacing=1)+
      txt(44,72,'Evidence checked October 2026 · Original motion design · Space Grotesk + Manrope',15,'#8da79f'))

BASE='https://raw.githubusercontent.com/zc627788/zc627788/main/assets/'
GH='https://github.com/zc627788/'
def image(name,alt,link=None,width='100%'):
    revision=hashlib.sha256((A/name).read_bytes()).hexdigest()[:12]
    tag=f'<img src="{BASE+name}?v={revision}" width="{width}" alt="{escape(alt,quote=True)}" />'
    return f'<a href="{link}">{tag}</a>' if link else tag

blocks=[image('orbit-header.svg','Jackson — Data in. Clarity out. Python automation and React applications.'),
        image('intro-panel.svg','I build Python extraction tools, document workflows and React business applications, from frontend through API, database and deployment.'),
        image('stack-strip.svg','Python · React · TypeScript · Next.js · FastAPI · SQL')]
for stem,repo,alt,evidence,linkalt in [
    ('court','caipanbook_Crawler','Court document collection: 7,296 distinct saved IDs, a 12-column export, 955 records recovered. Historical output audit; no new live crawl tested.','docs/portfolio/project-evidence/redacted-preview.csv','Open the redacted sample'),
    ('reports','bond_and_money_scrapy','Rating report pipeline: 15 downloaded PDFs, 10 unique files, 182 pages. One issuer and its first listing page.','docs/portfolio/live-evidence/manifest.csv','Inspect the download manifest'),
    ('opc','poc_system','OPC: Next.js portal, React admin, FastAPI backend. Verified product demo uses SQLite and fictional products; payments mocked, integrations untested.','docs/portfolio/products-live.png','Open the original local demo screenshot')]:
    blocks += [image(f'project-{stem}.svg',alt,GH+repo),image(f'link-{stem}.svg',linkalt,GH+repo+'/blob/main/'+evidence)]
blocks += [image('contact-panel.svg','Remote part-time projects, approximately 24 hours/week. Scoped milestones, written progress updates and clear handover.'),
           '<p align="center">'+ '\n'.join([image('link-upwork.svg','Contact on Upwork','https://www.upwork.com/freelancers/~01ea3bc7d239147efd', '32%'),image('link-eleduck.svg','Contact on Eleduck','https://eleduck.com/users/87hD4V','32%'),image('link-text.svg','Read the Chinese and accessible text edition','README.zh-CN.md','32%')])+'</p>',
           image('colophon.svg','Evidence checked October 2026. Animations illustrate the workflow; embedded screenshots show actual output. Space Grotesk and Manrope are licensed under SIL OFL.')]
(ROOT/'README.md').write_text('\n\n'.join(blocks)+'\n',encoding='utf-8')
zh=ROOT/'README.zh-CN.md'
zh.write_text(re.sub(re.escape(BASE)+r'([\w.-]+)(?:\?v=[a-f0-9]+)?',
    lambda m:BASE+m[1]+'?v='+hashlib.sha256((A/m[1]).read_bytes()).hexdigest()[:12],
    zh.read_text(encoding='utf-8')),encoding='utf-8')
print('Built outlined, animated SVG portfolio and README.')
