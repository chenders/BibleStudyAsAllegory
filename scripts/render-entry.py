#!/usr/bin/env python3
"""
render-entry.py - render a project story entry (markdown) into the project's
standard self-contained, dark, screen-native HTML reading page.

Usage:
    python render-entry.py ENTRY.md [OUTPUT.html]

OUTPUT defaults to <slug>.html beside ENTRY (slug taken from the entry's
**ID / slug:** field, else the entry's filename).

This is the canonical renderer: every entry goes through it so all stories look
and behave identically. The design standard it implements is documented in
12-rendering-spec.md. Requires: markdown, fonttools, brotli
(pip install --break-system-packages markdown fonttools brotli). The three fonts
are used from ./fonts if present, otherwise downloaded once from Google Fonts.
"""
import sys, os, re, base64, pathlib, urllib.request, html as H
import markdown

if len(sys.argv) < 2:
    sys.exit("usage: python render-entry.py ENTRY.md [OUTPUT.html]")
SRC = pathlib.Path(sys.argv[1])
md = SRC.read_text(encoding="utf-8")
lines = md.split("\n")
title = lines[0].lstrip("# ").strip()
idx = next(i for i,l in enumerate(lines) if l.strip()=="---")
meta_lines = [l for l in lines[1:idx] if l.strip()]
body_md = "\n".join(lines[idx+1:])

def inline(s):
    h=markdown.markdown(s); return re.sub(r"^<p>|</p>$","",h.strip())
def compact(v):
    v=re.sub(r"`","",v).strip()
    for sep in (" (", " — "):
        if sep in v: return v.split(sep)[0].strip()
    return v

rows=[]; score=None
for l in meta_lines:
    m=re.match(r"\*\*(.+?):\*\*\s*(.*)", l)
    if not m: continue
    k,v=m.group(1).strip(), m.group(2).strip()
    if k.startswith("Score"): score=v
    elif k.startswith("Keywords"): pass
    else: rows.append((k,v))

ref=next((v for k,v in rows if k=="Reference"),"")
eyebrow=f'<p class="eyebrow">{inline(ref)}</p>' if ref else ""
SHORT={"Genre / form":"Genre","Timeline position":"Setting","Canon(s)":"Canon","Parallel passages":"Parallels"}
ORDER=["Genre","Setting","Canon","Parallels"]
items=[]; slug=None
for k,v in rows:
    if k=="Reference": continue
    if k=="ID / slug": slug=re.sub(r"`","",v).strip(); continue
    items.append((SHORT.get(k,k),compact(v)))
items.sort(key=lambda it: ORDER.index(it[0]) if it[0] in ORDER else 99)
if slug: items.append(("ID",slug))
strip_html='<div class="strip">'+"".join(f'<span class="fi"><span class="fl">{H.escape(l)}</span><span class="fv">{H.escape(x)}</span></span>' for l,x in items)+'</div>'

NAMES={"I":"Influence","C":"Contested","P":"Popularity","H":"Harm","A":"Attestation"}
FULL={"I":"Influence","C":"Contestedness","P":"Popularity","H":"Harmful reception","A":"Historical attestation"}
DEFS={
    "I":"How deep a mark the passage has left on the wider culture \u2014 its language, art, law, and politics.",
    "C":"How much genuine scholarly dispute there is over the text, how it was composed, and how to read it.",
    "P":"How familiar the passage is to the general public, beyond specialists.",
    "H":"The documented history of the passage being used to cause harm. This rates the reception, not the text's plain meaning.",
    "A":"How far history and archaeology can actually support the events as real \u2014 kept separate from interpretive dispute.",
}
SCALE={"I":"0 none \u2192 5 foundational","C":"0 settled \u2192 5 fiercely contested","P":"0 obscure \u2192 5 universally known",
       "H":"0 none recorded \u2192 5 severe","A":"0 no testable claim \u2192 5 well-attested"}
ORD=["I","C","P","H","A"]
score_html=""
if score:
    sc=re.search(r"`([^`]+)`",score)
    axes=[a.strip() for a in re.split(r"[·•]", sc.group(1)) if a.strip()] if sc else []
    g=re.search(r"\*\((.+)\)\*",score, re.S)
    clauses=[]
    if g:
        note=re.split(r"\.\s*Full scale in", g.group(1).replace(chr(96),""))[0].strip().rstrip(".")
        clauses=[c.strip() for c in note.split(";")]
    def ax(t):
        L,n=t[0],t[1:]; hc=' class="h"' if (L=="H" and n!="0") else ''
        why=clauses[ORD.index(L)] if (L in ORD and ORD.index(L)<len(clauses)) else ""
        tip=(f'<b>{FULL[L]} \u00b7 {n} of 5</b>{H.escape(DEFS[L])}'
             f'<span class="scale">{H.escape(SCALE[L])}</span>'
             + (f'<span class="why"><i>This entry:</i> {H.escape(why)}.</span>' if why else ''))
        return (f'<span class="ax" tabindex="0" role="button" aria-label="{FULL[L]}, score {n} of 5">'
                f'<span class="lab">{NAMES.get(L,L)}</span><b{hc}>{n}</b>'
                f'<span class="tip">{tip}</span></span>')
    score_html='<div class="scorebar">'+"".join(ax(a) for a in axes)+'</div>'
meta_html=f'<div class="meta">{strip_html}{score_html}</div>'

body=markdown.markdown(body_md, extensions=["sane_lists"])
body=re.sub(r"<p><em>\(([^<]*)\)</em></p>", r'<p class="ednote">(\1)</p>', body)
body=re.sub(r"<p><em>([^<(][^<]*)</em></p>", r'<p class="aside">\1</p>', body)
body=re.sub(r"<em>\(([^<]*)\)</em>", r'<span class="gloss">(\1)</span>', body)
mv=re.search(r"(<h3>[^<]*[Rr]etelling[^<]*</h3>)(.*?)(<h3>)", body, flags=re.S)
if mv:
    seg=re.sub(r"<em>([^<]*)</em>", r'<span class="voice">\1</span>', mv.group(2))
    body=body[:mv.start(2)]+seg+body[mv.end(2):]

toc=[]
def _addid(m):
    tag=m.group(1); txt=H.unescape(re.sub("<[^>]+>","",m.group(2)))
    sid=re.sub(r"[^a-z0-9]+","-",txt.lower()).strip("-")
    toc.append((tag,txt,sid)); return f'<{tag} id="{sid}">{m.group(2)}</{tag}>'
body=re.sub(r"<(h2|h3)>(.*?)</\1>", _addid, body, flags=re.S)
def navlabel(t):
    for s in (" (", " — "):
        if s in t: t=t.split(s)[0].strip()
    return t
nav_html='<nav class="toc" aria-label="Sections"><div class="tocwrap">'+"".join(
    f'<a class="{"t2" if tag=="h2" else "t3"}" href="#{sid}">{H.escape(navlabel(txt))}</a>'
    for tag,txt,sid in toc)+'</div></nav>'
mtoc_html='<details class="mtoc"><summary>Click here to see the table of contents</summary><div class="mtoclist">'+"".join(
    f'<a class="{"m2" if tag=="h2" else "m3"}" href="#{sid}">{H.escape(navlabel(txt))}</a>'
    for tag,txt,sid in toc)+'</div></details>'
SCRIPT=("<script>(function(){var L=[].slice.call(document.querySelectorAll('.toc a')),"
        "M={};L.forEach(function(a){M[a.getAttribute('href').slice(1)]=a;});"
        "var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){"
        "L.forEach(function(l){l.classList.remove('on');});var a=M[e.target.id];if(a)a.classList.add('on');}});},"
        "{rootMargin:'-8% 0px -82% 0px',threshold:0});"
        "[].slice.call(document.querySelectorAll('h2[id],h3[id]')).forEach(function(h){io.observe(h);});"
        "var mt=document.querySelector('.mtoc');if(mt){mt.addEventListener('click',function(e){if(e.target.closest('a'))mt.removeAttribute('open');});}"
        "var AX=[].slice.call(document.querySelectorAll('.scorebar .ax'));"
        "AX.forEach(function(a){a.addEventListener('click',function(e){var o=a.classList.contains('open');AX.forEach(function(x){x.classList.remove('open');});if(!o)a.classList.add('open');e.stopPropagation();});});"
        "document.addEventListener('click',function(){AX.forEach(function(x){x.classList.remove('open');});});"
        "})();</script>")

from fontTools import subset as _ftsub
from fontTools.ttLib import TTFont as _TTFont
import io as _io, string as _string
_chars="".join(sorted(set(_string.printable) | set(md) |
                      set("Influence Contested Popularity Harm Attestation Genre Setting Canon Parallels ID "
                          "Click here to see the table of contents Sections Contents")))
def fontsub(path):
    f=_TTFont(path)
    o=_ftsub.Options(); o.flavor="woff2"
    o.hinting=False; o.name_IDs=[]; o.notdef_outline=True; o.recalc_timestamp=False
    s=_ftsub.Subsetter(options=o); s.populate(text=_chars); s.subset(f)
    f.flavor="woff2"
    b=_io.BytesIO(); f.save(b); return base64.b64encode(b.getvalue()).decode()
_FONT_URLS={
    "EBGaramond.ttf":"https://raw.githubusercontent.com/google/fonts/main/ofl/ebgaramond/EBGaramond%5Bwght%5D.ttf",
    "EBGaramond-Italic.ttf":"https://raw.githubusercontent.com/google/fonts/main/ofl/ebgaramond/EBGaramond-Italic%5Bwght%5D.ttf",
    "SourceSans3.ttf":"https://raw.githubusercontent.com/google/fonts/main/ofl/sourcesans3/SourceSans3%5Bwght%5D.ttf",
}
def _fontpath(name):
    for d in ("fonts", os.path.expanduser("~/.cache/bible-companion-fonts")):
        p=pathlib.Path(d)/name
        if p.exists(): return str(p)
    cache=pathlib.Path(os.path.expanduser("~/.cache/bible-companion-fonts")); cache.mkdir(parents=True,exist_ok=True)
    p=cache/name
    sys.stderr.write(f"fetching {name} from Google Fonts...\n")
    p.write_bytes(urllib.request.urlopen(_FONT_URLS[name], timeout=60).read())
    return str(p)
EBG=fontsub(_fontpath("EBGaramond.ttf")); EBI=fontsub(_fontpath("EBGaramond-Italic.ttf")); SS=fontsub(_fontpath("SourceSans3.ttf"))

CSS=f"""
@font-face{{font-family:'EB Garamond';font-style:normal;font-weight:400 800;src:url(data:font/woff2;base64,{EBG}) format('woff2');font-display:swap;}}
@font-face{{font-family:'EB Garamond';font-style:italic;font-weight:400 800;src:url(data:font/woff2;base64,{EBI}) format('woff2');font-display:swap;}}
@font-face{{font-family:'Source Sans 3';font-style:normal;font-weight:300 700;src:url(data:font/woff2;base64,{SS}) format('woff2');font-display:swap;}}
:root{{--ground:#0f1117;--panel:#161a22;--ink:#e7e9ef;--bright:#f5f6fa;--soft:#bfc6d3;--muted:#868ea0;--faint:#6b7280;--rule:#242935;--rubric:#c25a4d;}}
*{{box-sizing:border-box;}}
html,body{{margin:0;background:var(--ground);-webkit-text-size-adjust:100%;text-size-adjust:100%;}}
body{{font-family:'EB Garamond',Georgia,serif;color:var(--ink);font-size:13pt;line-height:1.62;-webkit-font-smoothing:antialiased;text-rendering:optimizeLegibility;overflow-wrap:break-word;}}
.wrap{{width:100%;max-width:56rem;margin-inline:auto;padding:18px clamp(20px,5vw,52px) 48px;}}
.eyebrow{{font-family:'Source Sans 3',sans-serif;font-size:8.8pt;font-weight:600;letter-spacing:.18em;text-transform:uppercase;color:var(--muted);margin:0 0 .42rem;}}
h1{{font-family:'EB Garamond',Georgia,serif;font-weight:600;font-size:24pt;line-height:1.18;color:var(--bright);margin:0 0 .6rem;}}
h2{{font-family:'Source Sans 3',sans-serif;font-weight:600;font-size:10pt;letter-spacing:.2em;text-transform:uppercase;color:var(--muted);margin:2.4rem 0 1.05rem;padding-top:.9rem;border-top:1px solid var(--rule);}}
h3{{font-family:'EB Garamond',Georgia,serif;font-weight:600;font-size:15.5pt;color:var(--bright);margin:1.75rem 0 .55rem;line-height:1.3;padding-left:.66rem;border-left:3px solid var(--rubric);}}
p{{margin:0 0 .82rem;}}
strong{{color:var(--bright);font-weight:600;}}
em{{font-style:italic;}}
a{{color:var(--soft);text-decoration:none;border-bottom:1px solid var(--rule);}}
code{{font-family:'Source Sans 3',sans-serif;font-size:.85em;color:var(--soft);background:#161a22;border-radius:4px;padding:.02em .32em;}}
hr{{display:none;}}
ul{{margin:.25rem 0 .95rem;padding-left:1.15rem;}}
li{{margin:.42rem 0;}} li p{{margin:.5rem 0;}}
blockquote{{margin:.7rem 0 1rem;padding:.1rem 0 .1rem 1rem;border-left:2px solid var(--rule);color:var(--soft);font-size:.96em;}}
.ednote{{font-family:'Source Sans 3',sans-serif;font-size:9.8pt;line-height:1.5;color:var(--muted);font-style:normal;margin:.05rem 0 .85rem;}}
.aside{{color:var(--soft);font-style:normal;margin:.55rem 0 .9rem;}}
.ednote em,.aside em{{font-style:italic;}}
.gloss{{color:var(--muted);}}
.voice{{color:var(--soft);font-style:normal;}}
.meta{{margin:0 0 .2rem;}}
.strip{{display:flex;flex-wrap:wrap;gap:.16rem 1.05rem;line-height:1.32;margin:0 0 .5rem;}}
.fi{{display:inline-flex;align-items:baseline;gap:.36rem;}}
.fl{{font-family:'Source Sans 3',sans-serif;font-size:7.8pt;font-weight:600;letter-spacing:.1em;text-transform:uppercase;color:var(--faint);}}
.fv{{font-family:'Source Sans 3',sans-serif;font-size:10pt;color:var(--soft);}}
.scorebar{{position:relative;display:flex;flex-wrap:wrap;gap:.12rem 1.05rem;line-height:1.32;margin:.1rem 0 0;padding-top:.4rem;border-top:1px solid var(--rule);}}
.ax{{display:inline-flex;align-items:baseline;gap:.34rem;cursor:help;border-bottom:1px dotted #353b49;padding-bottom:1px;outline:none;}}
.ax:hover,.ax:focus,.ax.open{{border-bottom-color:var(--rubric);}}
.ax .lab{{font-family:'Source Sans 3',sans-serif;font-size:7.8pt;font-weight:600;letter-spacing:.1em;text-transform:uppercase;color:var(--faint);}}
.ax b{{font-family:'Source Sans 3',sans-serif;font-size:10.5pt;font-weight:600;color:var(--bright);}}
.ax b.h{{color:var(--rubric);}}
.tip{{position:absolute;top:calc(100% + 10px);left:0;width:min(370px,100%);background:#1a1f29;border:1px solid #2f3543;border-radius:9px;padding:.72rem .82rem;font-family:'Source Sans 3',sans-serif;font-size:9.6pt;line-height:1.5;color:var(--soft);box-shadow:0 10px 30px rgba(0,0,0,.45);opacity:0;visibility:hidden;transform:translateY(-4px);transition:opacity .14s,transform .14s;z-index:30;pointer-events:none;}}
.ax:hover .tip,.ax:focus .tip,.ax.open .tip{{opacity:1;visibility:visible;transform:translateY(0);}}
.tip b{{display:block;color:var(--bright);font-size:10.5pt;font-weight:700;letter-spacing:.01em;margin-bottom:.32rem;}}
.tip .scale{{display:block;color:var(--faint);font-size:8.4pt;letter-spacing:.02em;margin-top:.42rem;}}
.tip .why{{display:block;color:var(--soft);margin-top:.5rem;padding-top:.5rem;border-top:1px solid var(--rule);}}
.tip .why i{{color:var(--muted);font-style:italic;}}
@media (max-width:600px){{ h1{{font-size:21pt;}} .fl,.ax .lab{{font-size:8.6pt;}} .fv{{font-size:10.6pt;}} .eyebrow{{font-size:9.2pt;}} .tip{{font-size:10pt;}} }}
a:focus-visible{{outline:2px solid var(--rubric);outline-offset:2px;border-radius:2px;}}
@media (prefers-reduced-motion:reduce){{*{{animation:none!important;transition:none!important;scroll-behavior:auto!important;}}}}
html{{scroll-behavior:smooth;}}
h2[id],h3[id]{{scroll-margin-top:20px;}}
.toc{{display:none;}}
@media (min-width:1220px){{
  .toc{{display:block;position:fixed;top:0;bottom:0;left:24px;width:min(196px,calc((100vw - 56rem)/2 - 40px));overflow-y:auto;padding:30px 0;-webkit-mask-image:linear-gradient(transparent,#000 24px,#000 calc(100% - 24px),transparent);mask-image:linear-gradient(transparent,#000 24px,#000 calc(100% - 24px),transparent);}}
}}
.toc a{{display:block;text-decoration:none;border:0;font-family:'Source Sans 3',sans-serif;}}
.toc .t2{{font-size:8pt;font-weight:600;letter-spacing:.14em;text-transform:uppercase;color:var(--faint);margin:1.2rem 0 .4rem;}}
.toc .tocwrap>.t2:first-child{{margin-top:0;}}
.toc .t2.on{{color:var(--muted);}}
.toc .t3{{font-size:9.2pt;line-height:1.32;color:var(--muted);padding:.2rem 0 .2rem .72rem;border-left:2px solid transparent;transition:color .15s,border-color .15s;}}
.toc .t3:hover{{color:var(--soft);}}
.toc .t3.on{{color:var(--bright);border-left-color:var(--rubric);}}
.toc a:focus-visible{{outline:2px solid var(--rubric);outline-offset:2px;}}
.mtoc{{display:none;}}
@media (max-width:1219px){{ .mtoc{{display:block;margin:.5rem 0 .7rem;}} }}
.mtoc summary{{display:flex;align-items:center;justify-content:space-between;gap:.6rem;font-family:'Source Sans 3',sans-serif;font-size:10pt;font-weight:600;color:var(--soft);padding:.62rem .85rem;cursor:pointer;list-style:none;border:1px solid var(--rule);border-radius:8px;background:var(--panel);}}
.mtoc summary::-webkit-details-marker{{display:none;}}
.mtoc summary::after{{content:"+";color:var(--rubric);font-size:13pt;line-height:1;font-weight:400;}}
.mtoc[open] summary{{border-bottom-left-radius:0;border-bottom-right-radius:0;}}
.mtoc[open] summary::after{{content:"\\2013";}}
.mtoc summary:hover{{border-color:#3a4150;color:var(--bright);}}
.mtoclist{{padding:.5rem .85rem .7rem;border:1px solid var(--rule);border-top:0;border-radius:0 0 8px 8px;}}
.mtoc a{{display:block;text-decoration:none;border:0;font-family:'Source Sans 3',sans-serif;}}
.mtoc .m2{{font-size:8pt;font-weight:600;letter-spacing:.12em;text-transform:uppercase;color:var(--faint);margin:.85rem 0 .25rem;}}
.mtoc .m3{{font-size:10.5pt;line-height:1.3;color:var(--soft);padding:.42rem 0 .42rem .72rem;border-left:2px solid var(--rule);}}
.mtoc a:focus-visible{{outline:2px solid var(--rubric);outline-offset:2px;}}
"""

doc=('<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">'
     '<meta name="viewport" content="width=device-width, initial-scale=1">'
     f'<title>{H.escape(title)}</title><style>{CSS}</style></head><body>'+nav_html+'<main class="wrap"><article>'
                                                                                   f'{eyebrow}<h1>{H.escape(title)}</h1>{meta_html}'+mtoc_html+f'{body}</article></main>'+SCRIPT+'</body></html>')
out=pathlib.Path(sys.argv[2]) if len(sys.argv)>2 else SRC.with_name((slug or SRC.stem)+".html")
out.write_text(doc, encoding="utf-8")
# integrity
stack=[]; longest=0
for m in re.finditer(r"<em>|</em>", doc):
    if m.group()=="<em>": stack.append(m.start())
    elif stack: longest=max(longest, m.end()-stack.pop())
print("HTML:", out, round(len(doc)/1024), "KB | unclosed em:", len(stack), "| longest em:", longest)