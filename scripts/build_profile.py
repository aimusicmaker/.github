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
def language_badge(name,active):
 text=('✓ ' if active else '')+name
 width=max(60,round(sum(12 if ord(c)>255 else 7 for c in text)+20))
 bg,fg=('#6d28d9','#ffffff') if active else ('#f6f8fa','#334155')
 return f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="28" viewBox="0 0 {width} 28"><rect x="0.5" y="0.5" width="{width-1}" height="27" rx="5" fill="{bg}" stroke="#cbd5e1"/><text x="50%" y="18" text-anchor="middle" font-family="Arial,sans-serif" font-size="12" font-weight="600" fill="{fg}">{html.escape(text)}</text></svg>\n'
def button(code,i,label,url,color,outline=False):
 asset=f'assets/{code}-{i}.svg';write(asset,badge(label,color,outline))
 return f'<a href="{url}"><img src="{RAW}/{asset}" height="40" alt="{html.escape(label,quote=True)}"></a>'
def header_badge(code, key, label, text, url, color):
 def measure(value):
  return max(65, round(sum(12 if ord(c)>255 else 7.3 for c in value)+24))
 left, right = measure(label), measure(text)
 width = left + right
 svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="28" viewBox="0 0 {width} 28"><rect width="{left}" height="28" fill="#555"/><rect x="{left}" width="{right}" height="28" fill="{color}"/><g fill="white" font-family="Arial,sans-serif" font-size="11" text-anchor="middle"><text x="{left/2}" y="18">{html.escape(label)}</text><text x="{left+right/2}" y="18" font-weight="700">{html.escape(text)}</text></g></svg>\n'
 asset = f'assets/{code}-{key}.svg'
 write(asset, svg)
 return f'<a href="{url}"><img src="{RAW}/{asset}" alt="{html.escape(text, quote=True)}"></a>'
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
  language_buttons=[]
  for c,n in LANGS:
   active=c==code
   asset=f'assets/lang-{c}{"-active" if active else ""}.svg'
   write(asset,language_badge(n,active))
   alt=html.escape(n+(' — '+t['language_current'] if active else ''),quote=True)
   current=' aria-current="page"' if active else ''
   language_buttons.append(f'<a href="{REPO}/blob/main/{folder}/{file(c)}"{current}><img src="{RAW}/{asset}" height="28" alt="{alt}"></a>')
  lang='<p align="center">'+' '.join(language_buttons)+'</p>'
  nav=' · '.join(f'[{t["nav"][i]}](#{anchor})' for i,anchor in [(1,'guides'),(0,'start'),(2,'tools'),(3,'about'),(4,'affiliate')])
  buttons=(' <br> ' if mobile else ' ').join(button(code,i,label,url,color,i==2) for i,(label,url,color) in enumerate(zip(t['buttons'],[site+'ai-song-generator/','#guides',site+'discover/'],['#6d28d9','#0f766e','#9a3412'])))
  website_button = header_badge(code, 'website', 'AI MUSIC MAKER', t['website_button'].upper(), site, '#7c3aed')
  github_button = header_badge(code, 'github', 'GITHUB', t['nav'][1].upper(), '#guides', '#181717')
  header_buttons = website_button + (' <br> ' if mobile else ' ') + github_button
  sections=[f'<div align="center">\n\n<img src="{RAW}/assets/musicmaker-logo.svg" width="88" height="88" alt="AI Music Maker">\n\n# AI Music Maker\n\n**{t["tagline"]}**\n\n{header_buttons}\n\n</div>\n\n---\n\n<p align="center">{switch}</p>\n\n{lang}\n\n---\n', f'{t["intro"]}\n\n{nav}\n\n<p align="center">{buttons}</p>\n', f'## {t["why_title"]}\n\n{t["why"]}\n',f'<a id="guides"></a>\n\n## {t["projects_title"]}\n']
  cards=[]
  for i,(slug,title,icon) in enumerate([('awesome-suno-creator-guide','Suno Music Creation Guide: Prompts, Examples & Tutorials','♫'),('awesome-music-video-creator-guide','Awesome Music Video Creator Guide','▶')]):
   url=f'https://github.com/aimusicmaker/{slug}/blob/main/{"mobile/" if mobile else ""}{file(code)}'
   asset = ['songwriting-guide.jpg', 'music-video-workflow.jpg'][i]
   caption = html.escape(t['project_image_captions'][i], quote=True)
   cards.append(f'### {icon} {title}\n\n{t["projects"][i]}\n\n<a href="{url}"><img src="{RAW}/assets/{asset}" width="100%" alt="{caption}"></a>\n\n{t["project_image_captions"][i]}\n\n[{t["image_zoom"]}]({RAW}/assets/{asset})\n\n**{t["project_labels"][0]}:** {t["project_audiences"][i]}\n\n**{t["project_labels"][1]}:** {t["project_learning"][i]}\n\n**[{t["project_actions"][i]}]({url})**\n')
  sections += ['\n---\n\n'.join(cards),f'<a id="start"></a>\n\n## {t["start_title"]}\n']
  sections += [f'{i}. {step}' for i,step in enumerate(t['start'],1)]
  sections += [f'\n```text\n{t["prompt"]}\n```\n\n> {t["prompt_note"]}\n',f'<a id="tools"></a>\n\n## {t["tools_title"]}\n\n{t["links_note"]}\n']
  if mobile:
   for row,route in zip(t['tools'],ROUTES):
    sections.append(f'### {row[0]}\n\n[{row[1]}](https://musicmaker.im/{route}/) ↗\n\n{row[2]}\n')
  else:
   sections.append('| '+' | '.join(t['table_headers'])+' |\n| :-- | :-- | :-- |')
   for row,route in zip(t['tools'],ROUTES): sections.append(f'| {row[0]} | [{row[1]}](https://musicmaker.im/{route}/) ↗ | {row[2]} |')
  if mobile:
   rewards='\n\n'.join(f'**{row[0]}** — {row[1]}' for row in t['affiliate_rewards'])
  else:
   rewards='| '+' | '.join(t['affiliate_headers'])+' |\n| :-- | :-- |\n'+'\n'.join('| '+' | '.join(row)+' |' for row in t['affiliate_rewards'])
  affiliate_steps='\n'.join(f'{i}. {step}' for i,step in enumerate(t['affiliate_steps'],1))
  sections += ['\n'+t['terms']+'\n\n'+' · '.join(f'[{label}](https://musicmaker.im/{route}/)' for label,route in zip(t['policy_links'],['pricing','commercial-license','terms-of-service']))+'\n',f'<a id="about"></a>\n\n## {t["trust_title"]}\n\n{t["trust"]}\n\n<details>\n<summary>{t["source_link"]}</summary>\n\n{t["reviewed"]}\n\n[{t["source_link"]}]({REPO}/blob/main/docs/SOURCES.md)\n\n</details>\n',f'## {t["contribute_title"]}\n\n{t["contribute"]}\n\n'+' · '.join(f'[{label}]({url})' for label,url in zip(t['contribute_links'],[REPO+'/issues','https://github.com/orgs/aimusicmaker/repositories','https://discord.gg/dykaXheA3e']))+'\n',f'<a id="affiliate"></a>\n\n## {t["affiliate_title"]}\n\n{t["affiliate"]}\n\n{rewards}\n\n{t["affiliate_rules"]}\n\n### {t["affiliate_steps_title"]}\n\n{affiliate_steps}\n\n'+button(code,'affiliate',t['affiliate_actions'][0],'https://musicmaker.im/affiliate-program/','#9a3412')+f'\n\n[{t["affiliate_actions"][1]}](https://musicmaker.im/affiliate-agreement/)\n']
  content='\n'.join(sections)
  # GitHub supports dir on HTML blocks; Markdown paragraphs remain outside them.
  if code=='ar': content='<div dir="rtl">\n\n'+content+'\n</div>\n'
  write(folder+'/'+file(code),content)
  if code=='en' and not mobile: write('README.md',content)
print(f'{len(LANGS)} desktop + {len(LANGS)} mobile profiles + repository README: '+('up to date' if args.check else 'generated'))
