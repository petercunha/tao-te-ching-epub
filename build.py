import zipfile, uuid, html, re, copy
from bs4 import BeautifulSoup
s=BeautifulSoup(open('page.html').read(),'html.parser')
c=s.select_one('.entry-content')
for d in c.select('div.sharedaddy, div.jp-relatedposts, div'): d.decompose()

def clean(el):
    el=copy.copy(el)
    for t in el.find_all(True):
        if t.name not in ('strong','em','br','b','i'): t.unwrap()
        else: t.attrs={}
    h=el.decode_contents().strip()
    h=re.sub(r'\s*<br/>\s*','<br/>\n',h)
    h=h.replace('&nbsp;',' ').replace('\xa0',' ')
    return h

FIX={'TREU GREATNESS':'TRUE GREATNESS'}

# Typos in the source post, keyed by chapter number (0 = the Epictetus preview).
# Each correction must match exactly once.
CORRECTIONS={
 2:[('the high and the loaw','the high and the low'),('if it not sincere','if it is not sincere')],
 3:[('silent don’t he subject','silent on the subject'),('hearts of their people','hearts of their people.')],
 4:[('<br/>\nYet it is never','<br/>\nyet it is never')],
 9:[('ist he way','is the way')],
 12:[('appearnaces','appearances')],
 13:[('both to be feared.','both to be feared,')],
 16:[('Seek and open mind','Seek an open mind'),('seeing the big-picture','seeing the big picture')],
 21:[('infinitely illusive','infinitely elusive'),('Illusive, indeed','Elusive, indeed')],
 24:[('things things—','these things—'),('fi to be trimmed','fit to be trimmed')],
 27:[('no scrips','no scripts'),('an oucast','an outcast')],
 31:[('never exalt over','never exult over'),('with sorro.','with sorrow.')],
 32:[('sweet ew drops','sweet dew drops'),('knowing where to stop,','Knowing where to stop,')],
 33:[('who dar risk','who dare risk')],
 34:[('not pround','not proud')],
 38:[('ist he mere','is the mere'),('appearnace','appearance')],
 39:[('it would fall<br/>','it would fall;<br/>'),('would issipate','would dissipate')],
 42:[('things which is a gain','things which it is a gain')],
 44:[('what they ahve','what they have')],
 46:[('than disconent','than discontent')],
 49:[('the treats <strong>[<em>sic</em>]</strong> the unfaithful','and treats the unfaithful')],
 52:[('those who babble and meddle in other’s business.','Those who babble and meddle in others’ business')],
 54:[('well-lanted','well-planted'),('One nation for','one nation for')],
 57:[('restraingt','restraint')],
 60:[('rule and empire','rule an empire')],
 64:[('That which is meager','that which is meager')],
 65:[('people ar difficult to govern.','people are difficult to govern,')],
 67:[('Their mediocrity','their mediocrity')],
 78:[('conqueror <strong>[<em>sic</em>]</strong>','conquer'),('Every one knows','Everyone knows')],
 80:[('safe and ocntent','safe and content')],
 81:[('steal from other ','steal from others ')],
 0:[('| What, then','What, then')],
}
def correct(num,paras):
    joined='\x00'.join(paras)
    for old,new in CORRECTIONS.get(num,[]):
        n=joined.count(old)
        assert n==1, f'correction {old!r} in chapter {num} matched {n} times'
        joined=joined.replace(old,new)
    return joined.split('\x00')

els=[e for e in c.find_all(recursive=False)]
sections=[]  # (kind, title, num, paras)
cur=None
pending_num=None
for e in els:
    t=e.get_text(strip=True)
    if e.name=='hr' or (e.name=='p' and e.find('img')) : continue
    if e.name in('h2','h3'):
        if t=='REFLECTIONS':
            cur=['reflections','Reflections',None,[]]; sections.append(cur)
        elif t.isdigit(): pending_num=int(t)
        elif pending_num is not None:
            cur=['chapter',FIX.get(t,t).title().replace('’S','’s').replace("'S","'s"),pending_num,[]]; sections.append(cur); pending_num=None
        elif t=='A PREVIEW OF':
            cur=['preview','A Preview of The Manual',None,[]]; sections.append(cur)
        elif cur and cur[0]=='preview':
            cur[3].append(('h',t))
        continue
    if e.name=='p' and cur and t:
        cur[3].append(('p',clean(e)))
print(len(sections), [x[2] for x in sections if x[0]=='chapter'][-3:])
assert sum(1 for x in sections if x[0]=='chapter')==81
for sec in sections:
    if sec[0] in ('chapter','preview'):
        ps=[p for k,p in sec[3] if k=='p']
        fixed=iter(correct(sec[2] or 0,ps))
        sec[3]=[(k,next(fixed) if k=='p' else p) for k,p in sec[3]]

CSS='''
@namespace epub "http://www.idpf.org/2007/ops";
body{font-family:Georgia,"Iowan Old Style",serif;line-height:1.55;margin:0 5%;}
h1,h2{font-weight:normal;text-align:center;}
.chap-num{text-align:center;font-size:2.6em;margin:2.2em 0 0;color:#8a6d3b;letter-spacing:.05em;font-variant:small-caps;}
h1.chap-title{font-size:1.05em;letter-spacing:.25em;text-transform:uppercase;margin:.4em 0 .4em;}
.orn{text-align:center;color:#8a6d3b;margin:.6em 0 2em;font-size:1.1em;}
p.verse{margin:0 0 1.15em;text-indent:0;text-align:left;}
.poem{margin:0 auto;max-width:28em;}
strong{font-weight:bold;}
p.prose{text-indent:1.4em;margin:0;text-align:justify;}
p.prose.first{text-indent:0;}
p.prose.first::first-letter{font-size:2.4em;float:left;line-height:1;margin:.05em .08em 0 0;color:#8a6d3b;}
h1.sec{font-size:1.5em;letter-spacing:.2em;text-transform:uppercase;margin-top:2.5em;}
.tp{text-align:center;margin-top:20%;}
.tp .t{font-size:2.6em;letter-spacing:.12em;margin:0;}
.tp .st{font-style:italic;font-size:1.2em;margin:.4em 0 2.5em;}
.tp .a{font-variant:small-caps;letter-spacing:.15em;font-size:1.2em;}
.tp .tr{font-size:.9em;margin-top:3em;color:#555;}
.tp .src{font-size:.75em;margin-top:4em;color:#777;}
h2.sub{font-size:1em;letter-spacing:.15em;text-transform:uppercase;margin:.3em 0;}
.cover{text-align:center;margin:0;padding:0;} .cover img{max-width:100%;max-height:100%;}
'''

def page(title,body):
    return f'''<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" lang="en" xml:lang="en">
<head><meta charset="utf-8"/><title>{html.escape(title)}</title><link rel="stylesheet" type="text/css" href="style.css"/></head>
<body>
{body}
</body></html>'''

ROMAN=lambda n: ''.join(sym*(n//v) if (n:=n) and False else '' for v,sym in [])  # unused
files=[]  # (id, href, title, content)
files.append(('cover','cover.xhtml','Cover',page('Cover','<div class="cover"><img src="cover.jpg" alt="Tao Te Ching cover"/></div>')))
files.append(('title','title.xhtml','Title Page',page('Tao Te Ching','''<div class="tp">
<p class="t">TAO TE CHING</p><p class="st">The Book of the Way</p><p class="a">Lao Tzu</p>
<p class="tr">Ancient Renewal / Sam Torode, 2021</p>
<p class="src">Transcribed with reflections from<br/>vialogue.wordpress.com, December 14, 2021</p></div>''')))
for kind,title,num,paras in sections:
    if kind=='reflections':
        body='<h1 class="sec">Reflections</h1><div class="orn">❧</div>\n'+'\n'.join(f'<p class="prose{" first" if i==0 else ""}">{p}</p>' for i,(_,p) in enumerate(paras))
        files.append(('reflections','reflections.xhtml','Reflections',page('Reflections',body)))
    elif kind=='chapter':
        body=f'<p class="chap-num">{num}</p>\n<h1 class="chap-title" id="c{num}">{html.escape(title)}</h1>\n<div class="orn">· ☯ ·</div>\n<div class="poem">\n'+'\n'.join(f'<p class="verse">{p}</p>' for _,p in paras)+'\n</div>'
        files.append((f'ch{num:02d}',f'ch{num:02d}.xhtml',f'{num}. {title}',page(f'{num}. {title}',body)))
    else:
        parts=['<h1 class="sec">A Preview Of</h1>']
        first=True
        for k,p in paras:
            if k=='h': parts.append(f'<h2 class="sub">{html.escape(p)}</h2>')
            else:
                if first: parts.append('<div class="orn">❧</div>')
                parts.append(f'<p class="prose{" first" if first else ""}">{p}</p>'); first=False
        files.append(('preview','preview.xhtml','A Preview of The Manual (Epictetus)',page('A Preview of The Manual','\n'.join(parts))))

toc_items=[f for f in files if f[0] not in('cover',)]
nav=page('Contents','<nav epub:type="toc" id="toc"><h1 class="sec">Contents</h1><ol style="list-style:none;padding:0;">'+''.join(f'<li><a href="{h}">{html.escape(t)}</a></li>' for i,h,t,_ in toc_items)+'</ol></nav><nav epub:type="landmarks" hidden=""><ol><li><a epub:type="cover" href="cover.xhtml">Cover</a></li><li><a epub:type="bodymatter" href="ch01.xhtml">Begin</a></li></ol></nav>')
uid=str(uuid.uuid5(uuid.NAMESPACE_URL,'https://vialogue.wordpress.com/2021/12/14/tao-te-ching/'))
spine_ids=['cover','title','nav']+[f[0] for f in files[2:]]
manifest='\n'.join(f'<item id="{i}" href="{h}" media-type="application/xhtml+xml"/>' for i,h,_,_ in files)
opf=f'''<?xml version="1.0" encoding="utf-8"?>
<package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="uid">
<metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
<dc:identifier id="uid">urn:uuid:{uid}</dc:identifier>
<dc:title>Tao Te Ching: The Book of the Way</dc:title>
<dc:creator>Lao Tzu</dc:creator>
<dc:contributor>Sam Torode (translator)</dc:contributor>
<dc:language>en</dc:language>
<dc:source>https://vialogue.wordpress.com/2021/12/14/tao-te-ching/</dc:source>
<meta property="dcterms:modified">2026-10-07T00:00:00Z</meta>
<meta name="cover" content="cover-img"/>
</metadata>
<manifest>
<item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/>
<item id="css" href="style.css" media-type="text/css"/>
<item id="cover-img" href="cover.jpg" media-type="image/jpeg" properties="cover-image"/>
{manifest}
</manifest>
<spine>
{''.join(f'<itemref idref="{i}"/>' for i in spine_ids)}
</spine>
</package>'''
out='Tao Te Ching.epub'
with zipfile.ZipFile(out,'w') as z:
    z.writestr(zipfile.ZipInfo('mimetype'),'application/epub+zip',compress_type=zipfile.ZIP_STORED)
    z.writestr('META-INF/container.xml','<?xml version="1.0"?><container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container"><rootfiles><rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/></rootfiles></container>',zipfile.ZIP_DEFLATED)
    z.writestr('OEBPS/content.opf',opf,zipfile.ZIP_DEFLATED)
    z.writestr('OEBPS/style.css',CSS,zipfile.ZIP_DEFLATED)
    z.writestr('OEBPS/nav.xhtml',nav,zipfile.ZIP_DEFLATED)
    z.write('cover.jpg','OEBPS/cover.jpg',zipfile.ZIP_DEFLATED)
    for i,h,t,cont in files: z.writestr('OEBPS/'+h,cont,zipfile.ZIP_DEFLATED)
print('ok')
