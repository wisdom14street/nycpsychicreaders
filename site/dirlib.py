"""Directory renderer shared by the two NYC reader directories. All prose comes from the site's own sitecopy (T dict);
this file only lays out verified data from site/listings.json and site/featured.json."""
import json, os, re
from html import escape as E
HERE = os.path.dirname(os.path.abspath(__file__))
BOOK = 'https://namastebookshop.com/pages/book-a-reading'
NB = {'name': 'Namaste Bookshop', 'street': '2 W 14th St', 'locality': 'New York', 'postal': '10011', 'phone': '212-645-0141', 'url': 'https://namastebookshop.com/', 'neighborhood': 'Union Square'}
BORO = ['Manhattan', 'Brooklyn', 'Queens', 'Bronx', 'Staten Island']
def slug(s): return re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')
def load(T):
    L = json.load(open(os.path.join(HERE, 'listings.json')))
    F = json.load(open(os.path.join(HERE, 'featured.json')))
    L = [x for x in L if T['keep'](x)]
    F = [r for r in F if T['keep_featured'](r)]
    return L, F
def tel(p): return 'tel:+1' + re.sub(r'\D', '', p)[-10:]
def addr(x):
    a = ', '.join(p for p in [x.get('street'), x.get('locality') or x['borough'], ('NY ' + x['postal']) if x.get('postal') else 'NY'] if p)
    return a
OFFER = {'tarot': 'Tarot', 'psychic': 'Psychic', 'palm': 'Palm', 'astrology': 'Astrology', 'mediumship': 'Mediumship', 'reiki': 'Reiki', 'energy': 'Energy work', 'classes': 'Classes', 'spiritual': 'Spiritual consultation'}
MODE = {'in-person': 'In person', 'walk-in': 'Walk-ins', 'phone': 'Phone', 'video': 'Video', 'events': 'Events', 'classes': 'Classes'}

def css():
    return '''<style>.dgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:14px;margin:1rem 0 1.6rem}
.dcard{background:var(--card);border:1px solid var(--line);border-radius:var(--r);padding:14px 16px;display:flex;flex-direction:column;gap:6px}
.dcard h3{margin:0;font-size:1.05rem;line-height:1.25}.dcard h3 a{text-decoration:none;color:inherit}.dcard p{margin:0;font-size:.92rem;color:var(--muted)}
.tags{display:flex;flex-wrap:wrap;gap:5px;margin:2px 0}.tags span{font-size:.75rem;padding:2px 8px;border-radius:999px;background:var(--soft);color:var(--ink)}
.feat{position:relative;border:2px solid var(--accent)}.badge{display:inline-block;font-size:.7rem;font-weight:700;letter-spacing:.04em;text-transform:uppercase;background:var(--accent);color:var(--onaccent);padding:2px 8px;border-radius:999px;align-self:flex-start}
.fgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:14px;margin:1rem 0 1.6rem}
.fcard{background:var(--card);border:2px solid var(--accent);border-radius:var(--r);overflow:hidden;display:flex;flex-direction:column;text-decoration:none;color:inherit}
.fcard img{width:100%;aspect-ratio:1/1;object-fit:cover;object-position:50% 20%;background:var(--soft);display:block}.fcard div{padding:8px 10px;display:flex;flex-direction:column;gap:3px}.fcard b{font-size:.95rem;line-height:1.2}.fcard small{color:var(--muted);line-height:1.3;font-size:.8rem;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}
.boros{display:grid;grid-template-columns:repeat(auto-fill,minmax(170px,1fr));gap:10px;margin:1rem 0}.boros a{display:block;padding:14px;border-radius:var(--r);background:var(--ink);color:var(--onink);text-decoration:none}.boros a b{display:block;font-size:1.1rem}.boros a span{font-size:.85rem;opacity:.85}
.prof{display:grid;grid-template-columns:minmax(0,300px) 1fr;gap:24px;align-items:start}.prof img{width:100%;aspect-ratio:1/1;object-fit:cover;border-radius:var(--r);background:var(--soft)}
@media(max-width:700px){.prof{grid-template-columns:1fr}.prof img{max-width:320px}}
.svc{width:100%;border-collapse:collapse;margin:.6rem 0}.svc td{padding:.45rem .3rem;border-bottom:1px solid var(--line)}.svc td:last-child{text-align:right;font-weight:700}
.btns{display:flex;flex-wrap:wrap;gap:8px;margin:.8rem 0}.claim{background:var(--soft);border-radius:var(--r);padding:14px 16px;margin:1.4rem 0}
.facts2{display:grid;grid-template-columns:max-content 1fr;gap:6px 14px;margin:1rem 0}.facts2 dt{font-weight:700}.facts2 dd{margin:0;overflow-wrap:anywhere}
.dhero{background:var(--ink);color:var(--onink);padding:34px 0 30px}.dhero h1{font-family:var(--display);font-size:clamp(1.9rem,6vw,3rem);line-height:1.08;margin:.2rem 0 .6rem}.dhero p{max-width:640px;opacity:.92}
.dhero .eyebrow{text-transform:uppercase;letter-spacing:.08em;font-size:.78rem;opacity:.8}.dhero .btn.ghost{color:var(--onink);border-color:currentColor}
.dstats{display:flex;flex-wrap:wrap;gap:18px;margin-top:14px;font-size:.9rem}.dstats b{font-size:1.3rem;display:block}</style>'''

def tags(items, M): return '<div class="tags">' + ''.join(f'<span>{E(M.get(i, i))}</span>' for i in items) + '</div>'
def lcard(T, x):
    loc = E(x['neighborhood'])
    return (f'<article class="dcard"><h3><a href="/{T["lp"]}/{x["slug"]}/">{E(x["name"])}</a></h3><p>{loc}, {E(x["borough"])}</p>{tags(x["offers"], OFFER)}'
            f'<p>{E(x["note"])}</p><p><a href="/{T["lp"]}/{x["slug"]}/">Details &rarr;</a></p></article>')
def fcard(T, r):
    return (f'<a class="fcard" href="/{T["fp"]}/{r["slug"]}/"><img src="{E(r["image"])}" alt="{E(r["name"])}" width="400" height="400" loading="lazy">'
            f'<div><span class="badge">Featured</span><b>{E(r["name"])}</b><small>{E(r["specialty"])}</small></div></a>')
def featured_grid(T, F, n=None): return '<div class="fgrid">' + ''.join(fcard(T, r) for r in (F[:n] if n else F)) + '</div>'
def lgrid(T, xs): return '<div class="dgrid">' + ''.join(lcard(T, x) for x in xs) + '</div>'

def nb_ld(): return {'@type': 'LocalBusiness', 'name': NB['name'], 'url': NB['url'], 'telephone': NB['phone'],
                    'address': {'@type': 'PostalAddress', 'streetAddress': NB['street'], 'addressLocality': NB['locality'], 'addressRegion': 'NY', 'postalCode': NB['postal'], 'addressCountry': 'US'}}
def biz_ld(T, S, x):
    o = {'@context': 'https://schema.org', '@type': 'LocalBusiness', 'name': x['name'], 'url': x['website'], 'sameAs': [x['website']],
         'description': x['note'], 'areaServed': {'@type': 'City', 'name': 'New York'}, '@id': f'{S.SITE}/{T["lp"]}/{x["slug"]}/#listing'}
    if x.get('phone'): o['telephone'] = x['phone']
    if x.get('street'):
        o['address'] = {'@type': 'PostalAddress', 'streetAddress': x['street'], 'addressLocality': x.get('locality') or x['borough'], 'addressRegion': 'NY', 'addressCountry': 'US'}
        if x.get('postal'): o['address']['postalCode'] = x['postal']
    return o
def itemlist(S, name, urls):
    return {'@context': 'https://schema.org', '@type': 'ItemList', 'name': name, 'numberOfItems': len(urls),
            'itemListElement': [{'@type': 'ListItem', 'position': i + 1, 'url': S.SITE + u, 'name': n} for i, (n, u) in enumerate(urls)]}

def pages(T, S):
    L, F = load(T)
    lp, fp, dp = T['lp'], T['fp'], T['dp']
    out = []
    # data file
    dd = os.path.join(HERE, '..', 'dist', 'data'); os.makedirs(dd, exist_ok=True)
    json.dump({'site': S.SITE, 'featured': [dict(name=r['name'], page=f'{S.SITE}/{fp}/{r["slug"]}/', specialty=r['specialty'], booking=BOOK, source_url=r['source_url'], location=NB) for r in F],
               'listings': [dict(x, page=f'{S.SITE}/{lp}/{x["slug"]}/') for x in L]}, open(os.path.join(dd, 'listings.json'), 'w'), indent=1, ensure_ascii=False)
    claim_href = lambda x: f'/claim/?listing={x["slug"]}'
    # featured profiles
    for r in F:
        svc = ''.join(f'<tr><td>{E(a)}</td><td>{E(b)}</td></tr>' for a, b in r['services'])
        sch = ''.join(f'<li>{E(d)}: {E(h)}</li>' for d, h in r['schedule'])
        body = f'''<div class="prof"><img src="{E(r['image'])}" alt="{E(r['name'])}" width="600" height="600"><div>
<span class="badge">Featured &middot; reads at Namaste Bookshop</span><p class="lead">{E(r['specialty'])}</p>{tags(r['tags'], {})}
<p>{T['featured_intro'](r)}</p>
<p><i>&ldquo;{E(r['hook'])}&rdquo;</i> <span class="small">(from the reader's page on namastebookshop.com)</span></p>
<div class="btns"><a class="btn" href="{BOOK}" rel="noopener">Book a reading</a><a class="btn ghost" href="{E(r['book_direct'])}" rel="noopener nofollow">Book {E(r['name'].split(' (')[0])} directly</a></div>
{('<h2>Sessions and prices</h2><table class="svc">' + svc + '</table><p class="small">As listed on namastebookshop.com; confirm the price when you book.</p>') if svc else '<p>Session options are shown when you book.</p>'}
<h2>When to find them</h2>{('<ul>' + sch + '</ul>') if sch else '<p>' + E(r['schedule_note'] or 'Schedule varies; the booking page shows current times.') + '</p>'}
<h2>Where</h2><p>Inside Namaste Bookshop, 2 West 14th Street (south side, just west of Fifth Avenue), Manhattan 10011. Readings line: <a href="tel:+12126450141">212-645-0141</a>. <a href="/visit/">How to find the shop</a>.</p>
<p class="small">Source: <a href="{E(r['source_url'])}" rel="noopener">{E(r['name'])} on namastebookshop.com</a>. Featured placement: these readers work at Namaste Bookshop, which shares an owner with this site.</p>
</div></div>'''
        ld = {'@context': 'https://schema.org', '@type': 'Person', 'name': r['name'], 'image': r['image'], 'jobTitle': r['specialty'], 'url': f'{S.SITE}/{fp}/{r["slug"]}/',
              'sameAs': [r['source_url']], 'worksFor': nb_ld()}
        if r['services']:
            ld['makesOffer'] = [{'@type': 'Offer', 'name': a, 'price': re.sub(r'[^\d.]', '', b), 'priceCurrency': 'USD'} for a, b in r['services'] if re.search(r'\d', b)]
        out.append({'path': f'/{fp}/{r["slug"]}/', 'title': T['ftitle'](r), 'desc': T['fdesc'](r), 'h1': E(r['name']), 'html': body, 'ld': [ld], 'wide': True,
                    'crumbs': [('Home', '/'), (T['dir_name'], f'/{dp}/'), ('Featured', f'/{fp}/'), (r['name'], f'/{fp}/{r["slug"]}/')]})
    out.append({'path': f'/{fp}/', 'title': T['fhub_title'], 'desc': T['fhub_desc'], 'h1': T['fhub_h1'], 'wide': True,
                'html': f'<p class="lead">{T["fhub_lead"]}</p><div class="btns"><a class="btn" href="{BOOK}" rel="noopener">See the booking page</a><a class="btn ghost" href="/visit/">How to find the shop</a></div>{featured_grid(T, F)}',
                'ld': [itemlist(S, T['fhub_h1'], [(r['name'], f'/{fp}/{r["slug"]}/') for r in F]), {'@context': 'https://schema.org', **nb_ld()}]})
    # listing pages
    for x in L:
        rows = [('Neighborhood', E(f'{x["neighborhood"]}, {x["borough"]}'))]
        if x.get('street') or x.get('postal'): rows.append(('Address', E(addr(x))))
        if x.get('phone'): rows.append(('Phone', f'<a href="{tel(x["phone"])}">{E(x["phone"])}</a>'))
        rows.append(('Website', f'<a href="{E(x["website"])}" rel="noopener nofollow">{E(re.sub(r"^https?://(www\.)?", "", x["website"]).rstrip("/"))}</a>'))
        rows.append(('Offers', ', '.join(OFFER[o] for o in x['offers'])))
        rows.append(('How', ', '.join(MODE[m] for m in x['modes'])))
        near = [y for y in L if y['borough'] == x['borough'] and y['slug'] != x['slug']][:3]
        body = f'''<p class="lead">{E(x['note'])}</p><dl class="facts2">{''.join(f'<dt>{a}</dt><dd>{b}</dd>' for a, b in rows)}</dl>
<div class="btns"><a class="btn" href="{E(x['website'])}" rel="noopener nofollow">Visit their website</a>{f'<a class="btn ghost" href="{tel(x["phone"])}">Call</a>' if x.get('phone') else ''}</div>
<p class="small">{T['listing_note']} Details checked against <a href="{E(x['source_url'])}" rel="noopener nofollow">their own website</a> on {x['verified_on']}. Prices, hours and availability change, so confirm with them before you go.</p>
<div class="claim"><b>Is this your business?</b> <a href="{claim_href(x)}">Claim this listing</a> to correct details, add photos and hours, or ask to be removed. Free, and no account or password needed.</div>
<h2>{T['also_in'](x['borough'])}</h2>{lgrid(T, near)}<p><a href="/{dp}/{slug(x['borough'])}/">{T['all_in'](x['borough'])} &rarr;</a></p>
<h2>{T['or_featured']}</h2>{featured_grid(T, F, 4)}'''
        out.append({'path': f'/{lp}/{x["slug"]}/', 'title': T['ltitle'](x), 'desc': T['ldesc'](x), 'h1': E(x['name']), 'html': body, 'ld': [biz_ld(T, S, x)], 'wide': True,
                    'crumbs': [('Home', '/'), (T['dir_name'], f'/{dp}/'), (x['borough'], f'/{dp}/{slug(x["borough"])}/'), (x['name'], f'/{lp}/{x["slug"]}/')]})
    # borough pages
    for b in BORO:
        xs = [x for x in L if x['borough'] == b]
        if not xs: continue
        hoods = {}
        for x in xs: hoods.setdefault(x['neighborhood'], []).append(x)
        secs = ''.join(f'<h2 id="{slug(h)}">{E(h)}</h2>{lgrid(T, ys)}' for h, ys in sorted(hoods.items(), key=lambda kv: (-len(kv[1]), kv[0])))
        fe = (f'<h2>{T["feat_h"]}</h2><p>{T["feat_p"]}</p>{featured_grid(T, F, 8)}<p><a href="/{fp}/">{T["feat_all"]} &rarr;</a></p>') if b == 'Manhattan' else (f'<p class="small">{T["feat_other"]} <a href="/{fp}/">{T["feat_all"]}</a>.</p>')
        jump = '<p class="small">Jump to: ' + ' &middot; '.join(f'<a href="#{slug(h)}">{E(h)}</a>' for h in sorted(hoods)) + '</p>'
        out.append({'path': f'/{dp}/{slug(b)}/', 'title': T['btitle'](b, len(xs)), 'desc': T['bdesc'](b, len(xs), sorted(hoods)), 'h1': T['bh1'](b), 'wide': True,
                    'html': f'<p class="lead">{T["bintro"][b]}</p>{jump}{fe if b == "Manhattan" else ""}{secs}{fe if b != "Manhattan" else ""}<div class="claim">{T["missing"]}</div>',
                    'ld': [itemlist(S, T['bh1'](b), ([(r['name'], f'/{fp}/{r["slug"]}/') for r in F] if b == 'Manhattan' else []) + [(x['name'], f'/{lp}/{x["slug"]}/') for x in xs])],
                    'crumbs': [('Home', '/'), (T['dir_name'], f'/{dp}/'), (b, f'/{dp}/{slug(b)}/')]})
    # extra topic/area pages
    for g in T['topics']:
        xs = [x for x in L if g['match'](x)]
        fs = [r for r in F if g.get('fmatch', lambda r: False)(r)]
        if len(xs) + len(fs) < 3: continue
        out.append({'path': f'/{dp}/{g["slug"]}/', 'title': g['title'], 'desc': g['desc'](len(xs) + len(fs)), 'h1': g['h1'], 'wide': True,
                    'html': f'<p class="lead">{g["intro"]}</p>' + (featured_grid(T, fs) if fs else '') + lgrid(T, xs) + f'<div class="claim">{T["missing"]}</div>',
                    'ld': [itemlist(S, g['h1'], [(r['name'], f'/{fp}/{r["slug"]}/') for r in fs] + [(x['name'], f'/{lp}/{x["slug"]}/') for x in xs])],
                    'crumbs': [('Home', '/'), (T['dir_name'], f'/{dp}/'), (g['h1'], f'/{dp}/{g["slug"]}/')]})
    # directory index
    bt = boro_tiles(T, L)
    tl = ''.join(f'<li><a href="/{dp}/{g["slug"]}/">{E(g["h1"])}</a></li>' for g in T['topics'] if len([x for x in L if g['match'](x)]) + len([r for r in F if g.get('fmatch', lambda r: False)(r)]) >= 3)
    allb = ''.join(f'<h2 id="{slug(b)}">{b}</h2>{lgrid(T, [x for x in L if x["borough"] == b])}' for b in BORO if any(x['borough'] == b for x in L))
    out.append({'path': f'/{dp}/', 'title': T['dtitle'](len(L) + len(F)), 'desc': T['ddesc'](len(L) + len(F)), 'h1': T['dir_h1'], 'wide': True,
                'html': f'<p class="lead">{T["dir_lead"]}</p>{bt}<p class="small">{T["browse_by"]}</p><ul>{tl}</ul><h2>{T["feat_h"]}</h2><p>{T["feat_p"]}</p>{featured_grid(T, F, 8)}<p><a href="/{fp}/">{T["feat_all"]} &rarr;</a></p>{allb}<div class="claim">{T["missing"]}</div>',
                'ld': [itemlist(S, T['dir_h1'], [(r['name'], f'/{fp}/{r["slug"]}/') for r in F] + [(x['name'], f'/{lp}/{x["slug"]}/') for x in L])],
                'crumbs': [('Home', '/'), (T['dir_name'], f'/{dp}/')]})
    # claim + advertise
    opts = ''.join(f'<option value="{x["slug"]}">{E(x["name"])}</option>' for x in L)
    mail = T['email']
    out.append({'path': '/claim/', 'title': T['claim_title'], 'desc': T['claim_desc'], 'h1': T['claim_h1'],
                'html': f'''<p class="lead">{T['claim_lead']}</p>
<form class="claimform" onsubmit="var s=this.l.value,n=this.l.options[this.l.selectedIndex].text,w=this.w.value;location.href='mailto:{mail}?subject='+encodeURIComponent('Claim listing: '+n+' ('+s+')')+'&body='+encodeURIComponent('Listing: {S.SITE}/{lp}/'+s+'/\\nWhat I want changed:\\n'+w+'\\n\\nMy name and role:\\nBest way to reach me:\\n');return false">
<p><label>Which listing?<br><select name="l" id="claim-l">{opts}<option value="new">Not listed yet, please add me</option></select></label></p>
<p><label>What should change? (optional)<br><textarea name="w" rows="4" style="width:100%"></textarea></label></p>
<p><button class="btn" type="submit">Open an email to us</button></p></form>
<p class="small">This opens your own email app with the details filled in; nothing is sent until you press send. We never ask for passwords. Prefer to talk? Call Namaste Bookshop at <a href="tel:+16468761401">646-876-1401</a>. Or email <a href="mailto:{mail}">{mail}</a>.</p>
<h2>What happens next</h2><ol><li>We check that you run the business, usually by calling the number on your own website.</li><li>We update the listing with your corrections, hours and photo.</li><li>If you would rather not be listed, we remove you.</li></ol>
<script>(function(){{var m=location.search.match(/listing=([a-z0-9-]+)/);if(m){{var s=document.getElementById('claim-l');if(s)s.value=m[1];}}}})()</script>'''})
    out.append({'path': '/advertise/', 'title': T['ad_title'], 'desc': T['ad_desc'], 'h1': T['ad_h1'],
                'html': f'''<p class="lead">{T['ad_lead']}</p>
<h2>Ways to stand out</h2><ul><li><b>Featured listing:</b> {T['ad_feat']}</li><li><b>Borough spotlight:</b> a top spot on one borough page, clearly labeled as a paid placement.</li><li><b>Event or class listing:</b> promote a reading night, workshop or course.</li></ul>
<p>Paid placements are always labeled. Free listings stay free, and we never sell reviews or ratings.</p>
<p><a class="btn" href="mailto:{mail}?subject={E(T['ad_subject'])}">Ask about featured placement</a></p><p class="small">Or call <a href="tel:+16468761401">646-876-1401</a>. Already listed? <a href="/claim/">Claim your listing</a> first.</p>'''})
    # guides
    for g in T['guides']:
        out.append({'path': g['path'], 'title': g['title'], 'desc': g['desc'], 'h1': g['h1'], 'html': g['html'] + f'<p><a class="btn" href="/{dp}/">{T["guide_cta"]}</a></p>',
                    'ld': [{'@context': 'https://schema.org', '@type': 'Article', 'headline': g['h1'], 'author': {'@type': 'Organization', 'name': S.BRAND}, 'publisher': {'@type': 'Organization', 'name': 'Wealth Edge Ventures Inc.'}}]})
    return out

def boro_tiles(T, L):
    return '<div class="boros">' + ''.join(f'<a href="/{T["dp"]}/{slug(b)}/"><b>{b}</b><span>{sum(1 for x in L if x["borough"] == b) + (len(load(T)[1]) if b == "Manhattan" else 0)} {T["unit"]}</span></a>' for b in BORO if any(x['borough'] == b for x in L)) + '</div>'
