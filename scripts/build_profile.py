#!/usr/bin/env python3
"""Build GitHub-safe localized profiles; --check detects stale output."""
import argparse, html, json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
REPO = 'https://github.com/aimusicmaker/.github'
RAW = 'https://raw.githubusercontent.com/aimusicmaker/.github/main'
LANGS = [('en','English'),('ja','日本語'),('id','Bahasa Indonesia'),('it','Italiano'),('pt','Português'),('es','Español'),('de','Deutsch'),('ru','Русский'),('fr','Français'),('zh','简体中文'),('tw','繁體中文'),('ko','한국어'),('th','ไทย'),('vi','Tiếng Việt'),('ar','العربية')]
ROUTES = ['ai-song-generator','ai-lyrics-generator','ai-music-video-generator','ai-image-generator/album-cover-maker','audio-to-midi','free-short-music-video-generator']
CHECK = argparse.ArgumentParser(); CHECK.add_argument('--check',action='store_true'); args=CHECK.parse_args()
def write(path,text):
 p=ROOT/path
 if args.check:
  assert p.exists() and p.read_text()==text, f'Stale file: {path}'
 else:
  p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text)
def file(code): return 'README.md' if code=='en' else f'README_{code.upper()}.md'
def badge(text,color,outline=False):
 width=max(110,round(sum(16 if ord(c)>255 else 8.8 for c in text)+40))
 return f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="40" viewBox="0 0 {width} 40"><rect x="1" y="1" width="{width-2}" height="38" rx="{19 if outline else 9}" fill="{ "#ffffff" if outline else color}" stroke="{color}" stroke-width="2"/><text x="50%" y="25" text-anchor="middle" font-family="Arial,sans-serif" font-size="15" font-weight="600" fill="{color if outline else "#ffffff"}">{html.escape(text)}</text></svg>\n'
def button(code,i,label,url,color,outline=False):
 asset=f'assets/{code}-{i}.svg';write(asset,badge(label,color,outline))
 return f'<a href="{url}"><img src="{RAW}/{asset}" height="40" alt="{html.escape(label,quote=True)}"></a>'
for code,name in LANGS:
 for mobile in (False, True):
  t=json.loads((ROOT/f'i18n/{code}.json').read_text())
  base=json.loads((ROOT/'i18n/en.json').read_text())
  def shape(x): return {k:shape(v) for k,v in x.items()} if isinstance(x,dict) else [shape(v) for v in x] if isinstance(x,list) else type(x).__name__
  assert shape(t)==shape(base),f'Structure mismatch: {code}'
  folder = 'profile/mobile' if mobile else 'profile'
  other_folder = 'profile' if mobile else 'profile/mobile'
  switch = button(code, 'desktop' if mobile else 'mobile', t['view_switch'][1 if mobile else 0], f'{REPO}/blob/main/{other_folder}/{file(code)}', '#334155', True)
  site='https://musicmaker.im/'+('' if code=='en' else code+'/')
  lang=' · '.join(f'**{n}**' if c==code else f'[{n}]({REPO}/blob/main/{folder}/{file(c)})' for c,n in LANGS)
  nav=' · '.join(f'[{label}](#{anchor})' for label,anchor in zip(t['nav'],['start','guides','tools','about','affiliate']))
  buttons=(' <br> ' if mobile else ' ').join(button(code,i,label,url,color,i==2) for i,(label,url,color) in enumerate(zip(t['buttons'],[site+'ai-song-generator/','#guides',site+'discover/'],['#6d28d9','#0f766e','#9a3412'])))
  sections=[f'<div {"dir="+chr(34)+"rtl"+chr(34) if code=="ar" else ""} align="center">\n\n# [MusicMaker]({site})\n\n**{t["tagline"]}**\n\n{buttons}\n\n{switch}\n\n{lang}\n\n</div>\n', f'{t["intro"]}\n\n{nav}\n',f'<a id="start"></a>\n\n## {t["start_title"]}\n']
  sections += [f'{i}. {s}' for i,s in enumerate(t['start'],1)]
  sections += [f'\n```text\n{t["prompt"]}\n```\n\n> {t["prompt_note"]}\n',f'<a id="guides"></a>\n\n## {t["projects_title"]}\n\n{t["why"]}\n']
  cards=[]
  for i,(slug,title,icon) in enumerate([('awesome-suno-creator-guide','Awesome Suno Creator Guide','♫'),('awesome-music-video-creator-guide','Awesome Music Video Creator Guide','▶')]):
   url=f'https://github.com/aimusicmaker/{slug}/blob/main/{file(code)}'
   asset = ['songwriting-guide.png', 'music-video-workflow.png'][i]
   caption = html.escape(t['project_image_captions'][i], quote=True)
   if mobile:
    cards.append(f'### {icon} {title}\n\n{t["projects"][i]}\n\n<a href="{url}"><img src="{RAW}/assets/{asset}" width="900" alt="{caption}"></a>\n\n{t["project_image_captions"][i]}\n\n[{t["image_zoom"]}]({RAW}/assets/{asset})\n\n**[{t["project_actions"][i]}]({url})**\n')
   else:
    cards.append(f'<td width="50%" valign="top"><h3>{icon} {title}</h3><p>{html.escape(t["projects"][i])}</p><a href="{url}"><img src="{RAW}/assets/{asset}" width="440" alt="{caption}"></a><p>{html.escape(t["project_image_captions"][i])}</p><p><a href="{RAW}/assets/{asset}">{html.escape(t["image_zoom"])}</a></p><a href="{url}"><b>{html.escape(t["project_actions"][i])}</b></a></td>')
  sections += ['\n'.join(cards) if mobile else '<table><tr>\n'+'\n'.join(cards)+'\n</tr></table>\n', f'<a id="tools"></a>\n\n## {t["tools_title"]}\n\n{t["links_note"]}\n']
  if mobile:
   for row,route in zip(t['tools'],ROUTES):
    sections.append(f'### {row[0]}\n\n[{row[1]}](https://musicmaker.im/{route}/) ↗\n\n{row[2]}\n')
  else:
   sections.append('| '+' | '.join(t['table_headers'])+' |\n| :-- | :-- | :-- |')
   for row,route in zip(t['tools'],ROUTES): sections.append(f'| {row[0]} | [{row[1]}](https://musicmaker.im/{route}/) ↗ | {row[2]} |')
  sections += ['\n'+t['terms']+'\n\n'+' · '.join(f'[{label}](https://musicmaker.im/{route}/)' for label,route in zip(t['policy_links'],['pricing','commercial-license','terms-of-service']))+'\n',f'<a id="about"></a>\n\n## {t["trust_title"]}\n\n{t["trust"]}\n\n<details>\n<summary>{t["source_link"]}</summary>\n\n{t["reviewed"]}\n\n[{t["source_link"]}]({REPO}/blob/main/docs/SOURCES.md)\n\n</details>\n',f'## {t["contribute_title"]}\n\n{t["contribute"]}\n\n'+' · '.join(f'[{label}]({url})' for label,url in zip(t['contribute_links'],[REPO+'/issues','https://github.com/orgs/aimusicmaker/repositories','https://discord.gg/dykaXheA3e']))+'\n',f'<a id="affiliate"></a>\n\n## {t["affiliate_title"]}\n\n{t["affiliate"]}\n\n{t["affiliate_rules"]}\n\n{t["affiliate_steps"]}\n\n'+button(code,'affiliate',t['affiliate_actions'][0],'https://musicmaker.im/affiliate-program/','#9a3412')+f'\n\n[{t["affiliate_actions"][1]}](https://musicmaker.im/affiliate-agreement/)\n']
  content='\n'.join(sections)
  # GitHub supports dir on HTML blocks; Markdown paragraphs remain outside them.
  if code=='ar': content='<div dir="rtl">\n\n'+content+'\n</div>\n'
  write(folder+'/'+file(code),content)
  if code=='en' and not mobile: write('README.md',content)
print(f'{len(LANGS)} desktop + {len(LANGS)} mobile profiles + repository README: '+('up to date' if args.check else 'generated'))
