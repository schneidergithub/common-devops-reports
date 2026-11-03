"""Build the October web and PDF editions from newsletter.md. Requires reportlab."""
from pathlib import Path
import re
from html import escape
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph
from reportlab.lib.colors import HexColor

ROOT = Path(__file__).resolve().parents[1]
ISSUE = ROOT / 'reports/2026-10'
md = (ISSUE / 'newsletter.md').read_text()
parts = md.strip().split('\n\n')
title = parts[0][2:]
period = parts[1].strip('*')
intro = parts[2]
note = parts[-1].strip('*')
stories = []
for i in range(3, len(parts)-1, 2):
    heading, date = parts[i].split('\n')
    number, heading = heading[3:].split(' · ', 1)
    stories.append((number, heading, date.strip('*'), parts[i+1]))
assert len(stories) == 10

def linked(text, pdf=False):
    pattern = r'\[([^\]]+)\]\((https://[^)]+)\)'
    out, end = [], 0
    for m in re.finditer(pattern, text):
        out.append(escape(text[end:m.start()]))
        url, label = escape(m[2], quote=True), escape(m[1])
        out.append(f'<a href="{url}" color="#1c527f"><u>{label}</u></a>' if pdf else f'<a href="{url}">{label}</a>')
        end = m.end()
    return ''.join(out) + escape(text[end:])

description = 'Ten brief stories on AI development, software trust, the Binance heist, and cybersecurity. Coverage from October 1 to November 1, 2026.'
css = '''
:root{--navy:#08192e;--ink:#17253b;--muted:#54637a;--red:#c5383f;--coral:#ff7c79;--line:#dbe3ec}
*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:#eaf0f6;color:var(--ink);font:16px/1.6 Arial,Helvetica,sans-serif}
a{color:#1c527f;text-underline-offset:3px}a:focus-visible{outline:3px solid var(--red);outline-offset:4px}
.wrap{max-width:1060px;margin:36px auto;background:#fff;box-shadow:0 10px 60px #08192e16}
.masthead{padding:30px 45px;background:var(--navy);color:#fff}.brand{display:flex;justify-content:space-between;gap:20px;align-items:center;border-bottom:1px solid #ffffff35;padding-bottom:17px}
.brand strong{font-size:22px;letter-spacing:1.4px}.brand span{color:#b1c4d9;font-size:11px;letter-spacing:1.7px;text-transform:uppercase}
.kicker{font-size:11px;text-transform:uppercase;letter-spacing:1.7px;color:#67d5e3;font-weight:bold;margin:21px 0 9px}
h1{font-size:49px;line-height:1.1;letter-spacing:-1.7px;margin:0}h1 span{display:block;color:var(--coral)}.deck{color:#c4d3e5;font-size:13px;margin:17px 0 0}
.content{padding:0 45px 30px}.publication-links{display:flex;flex-wrap:wrap;justify-content:space-between;gap:12px;padding:15px 0;border-bottom:1px solid var(--line);font-size:13px}.download{font-weight:bold}
.intro{font-size:18px;line-height:1.6;padding:24px 0;border-bottom:1px solid var(--line);margin:0 0 26px}
.stories{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:28px 36px}.story{border-bottom:1px solid var(--line);padding-bottom:22px;break-inside:avoid}
.label{display:flex;gap:10px;align-items:center;color:var(--muted);font-size:12px;margin-bottom:12px}.badge{display:inline-flex;flex-shrink:0;align-items:center;justify-content:center;width:27px;height:27px;background:var(--red);color:white;border-radius:50%;font-weight:bold}
h2{font-size:23px;line-height:1.22;letter-spacing:-.35px;margin:0 0 12px}p{margin:0}.reporting{margin:24px 0 0;font-size:12px;color:var(--muted)}footer{display:flex;flex-wrap:wrap;justify-content:space-between;gap:12px;border-top:1px solid var(--line);padding-top:16px;margin-top:22px;font-size:11px;color:var(--muted)}
@media(max-width:720px){.wrap{margin:0;box-shadow:none}.masthead{padding:25px 22px}.content{padding:0 22px 25px}.brand strong{font-size:18px}.brand span{font-size:9px}h1{font-size:36px;letter-spacing:-1px}.stories{grid-template-columns:1fr;gap:24px}.intro{font-size:16px}h2{font-size:23px}}
@media print{@page{size:Letter;margin:16mm}body{background:white;font-size:10pt}.wrap{margin:0;max-width:none;box-shadow:none}.masthead{padding:20px}.content{padding:0}h1{font-size:28pt}.stories{display:block}.story{margin:16px 0}h2{font-size:14pt}.publication-links{display:none}.intro{font-size:11pt}.brand strong{font-size:14pt}}
'''
head = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{escape(title)} | Common DevOps</title><meta name="description" content="{description}">
<link rel="canonical" href="https://www.aaronschneider.org/common-devops-reports/reports/2026-10/">
<meta property="og:type" content="article"><meta property="og:site_name" content="Common DevOps Reports">
<meta property="og:title" content="{escape(title)}"><meta property="og:description" content="{description}">
<meta property="og:url" content="https://www.aaronschneider.org/common-devops-reports/reports/2026-10/">
<meta name="twitter:card" content="summary"><meta name="twitter:title" content="{escape(title)}"><meta name="twitter:description" content="{description}">
<style>{css}</style></head><body><main class="wrap"><article>
<header class="masthead"><div class="brand"><strong>COMMON DEVOPS</strong><span>October 2026</span></div>
<p class="kicker">AI &amp; Cybersecurity Monthly Review</p><h1>Cybersecurity Must<span>Keep Pace with AI</span></h1>
<p class="deck">October 1 to November 1, 2026</p></header><div class="content">
<nav class="publication-links" aria-label="Report navigation"><a href="../../">Back to report archive</a><a class="download" href="./common-devops-october-2026.pdf" download>Download PDF</a></nav>
<p class="intro">{escape(intro)}</p><div class="stories">'''
body = '\n'.join(f'<section class="story" id="story-{n}"><div class="label"><span class="badge">{n}</span><span>{escape(d)}</span></div><h2>{escape(h)}</h2><p>{linked(b)}</p></section>' for n,h,d,b in stories)
tail = f'''</div><p class="reporting">{escape(note)}</p><footer><span>Report by Common DevOps</span><a href="https://www.youtube.com/@commondevops">Common DevOps on YouTube</a><span>October 1 to November 1, 2026</span></footer></div></article></main></body></html>'''
(ISSUE / 'index.html').write_text(head + body + tail)

# The PDF uses a compact single-column reading order, five stories per page.
pdf = Canvas(str(ISSUE / 'common-devops-october-2026.pdf'), pagesize=(612,792))
pdf.setTitle(title)
pdf.setAuthor('Common DevOps')
pdf.setSubject('AI and cybersecurity monthly review, October 1 to November 1, 2026')
navy, ink, muted = map(HexColor, ['#08192e','#17253b','#54637a'])
styles = {
    'body': ParagraphStyle('body', fontName='Helvetica', fontSize=10.4, leading=14.3, textColor=ink),
    'heading': ParagraphStyle('heading', fontName='Helvetica-Bold', fontSize=13, leading=15, textColor=navy),
    'intro': ParagraphStyle('intro', fontName='Helvetica', fontSize=11, leading=15.4, textColor=ink),
    'note': ParagraphStyle('note', fontName='Helvetica', fontSize=8.5, leading=11.5, textColor=muted),
}
width, left = 528, 42
def para(text, y, style):
    p = Paragraph(text, styles[style])
    _, height = p.wrap(width, 740)
    p.drawOn(pdf, left, y-height)
    return y-height

for page in range(2):
    if page == 0:
        pdf.setFillColor(navy); pdf.rect(0,650,612,142,fill=1,stroke=0)
        pdf.setFillColor(HexColor('#ffffff')); pdf.setFont('Helvetica-Bold',15); pdf.drawString(42,759,'COMMON DEVOPS')
        pdf.setFont('Helvetica',9); pdf.drawRightString(570,760,'OCTOBER 2026')
        pdf.setStrokeColor(HexColor('#506078')); pdf.line(42,744,570,744)
        pdf.setFont('Helvetica-Bold',26); pdf.drawString(42,710,'Cybersecurity Must')
        pdf.setFillColor(HexColor('#ff7c79')); pdf.drawString(42,679,'Keep Pace with AI')
        y = para(escape(intro), 630, 'intro')-18
    else:
        pdf.setFillColor(navy); pdf.setFont('Helvetica-Bold',12); pdf.drawString(42,752,'COMMON DEVOPS')
        pdf.setFont('Helvetica',9); pdf.drawRightString(570,753,'AI & CYBERSECURITY MONTHLY REVIEW')
        pdf.setStrokeColor(navy); pdf.line(42,741,570,741)
        y=722
    for n,h,d,b in stories[page*5:page*5+5]:
        pdf.setFillColor(HexColor('#c5383f')); pdf.setFont('Helvetica-Bold',8.5)
        pdf.drawString(left,y,f'{n}  /  {d.upper()}'); y-=9
        y = para(escape(h), y, 'heading')-5
        y = para(linked(b,pdf=True), y, 'body')-14
    if page == 1:
        y=para(escape(note),y-3,'note')
    assert y>53, f'Page {page+1} content exceeds footer boundary at {y}'
    pdf.setStrokeColor(HexColor('#dbe3ec')); pdf.line(42,42,570,42)
    pdf.setFillColor(muted); pdf.setFont('Helvetica',8)
    pdf.drawString(42,28,'OCTOBER 1 TO NOVEMBER 1, 2026')
    pdf.drawRightString(570,28,f'REPORT BY COMMON DEVOPS  /  {page+1:02}')
    pdf.showPage()
pdf.save()
print('Built web and two-page PDF editions from ten source stories.')
