"""NYC Psychic Readers (nycpsychicreaders.com): a guide to psychics, mediums, palm readers and intuitive healers in New York City,
sorted by the kind of reading, with featured intuitives at Namaste Bookshop and a shop of oracle decks and pendulums. Copy written for this site only."""
import re, types, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dirlib
E = __import__('html').escape
ICON = 'tag'
FAM_LABEL, FAM_ALL, STYLE_LABEL, STYLE_ALL = 'Theme', 'All themes', 'Format', 'All formats'
NO_FAMILY = ()
NAV_AISLES = False
NAV_EXTRA = '<a href="/psychics/">Find a psychic</a><a href="/psychics/mediums/">Mediums</a><a href="/featured-psychics/">Featured</a><a href="/guide/psychic-vs-tarot-reading/">Guides</a><a href="/advertise/">List your practice</a><a href="/shop/oracle-decks/">Oracle decks</a>'
BOOK = dirlib.BOOK
_BOOKT = ('books', 'Book', 'Books', 'Spiritual Book')
def category(p):
    t, ty = p['title'], p.get('product_type', '')
    if ty in ('Oracle Cards', 'Oracle Deck', 'Celtic Oracle Deck', 'Dream Oracle Deck', 'Astrology Oracle Deck'): return 'oracle'
    if ty in ('Pendulum', 'Pendulum Board', 'Scrying Mirror', 'Dowsing Rod'): return 'tools'
    if ty in ('Affirmation Deck', 'Affirmation Cards', 'Inspirational Cards', 'Inspiration Cards', 'Mini Deck'): return 'affirm'
    if ty in _BOOKT and re.search(r'psychic|intuiti|medium|clairvoy|spirit guide|palmistry|palm reading|pendulum|scrying|akashic|aura|empath|channel', t, re.I) and not re.search(r'\btarot\b', t, re.I): return 'books'
    return None
def assign(x): return x['base']
FAMILIES = [('angels', 'Angels & guides', r'angel|guide|archangel|spirit guide|ancestor'), ('goddess', 'Goddess & feminine', r'goddess|feminine|women|priestess|queen'),
            ('moon-stars', 'Moon, stars & astrology', r'moon|lunar|star|astrolog|zodiac|cosmic|planet|sun\b'), ('animals', 'Animal spirits', r'animal|totem|wolf|bird|cat\b|cats\b|horse|power animal'),
            ('nature', 'Nature & earth', r'nature|earth|forest|tree|flower|plant|herb|botanic|garden|faer|fairy|elemental'), ('crystals', 'Crystals & energy', r'crystal|chakra|aura|energy|reiki|healing'),
            ('dreams', 'Dreams & the unseen', r'dream|shadow|mystic|psychic|intuition|oracle of the|mystery|magic|witch|spell'),
            ('love', 'Love & self-worth', r'love|heart|self|affirm|worth|soul')]
def style_of(t, b, base):
    if base == 'tools': return 'Pendulum' if re.search(r'pendulum', t, re.I) else 'Scrying & dowsing'
    if base in ('oracle', 'affirm'): return 'Deck with guidebook' if re.search(r'guidebook|book|set|kit', t, re.I) else 'Deck'
    return ''
_B = [('hay-house', 'Hay House', r'hay house', ['Hay House']), ('rockpool', 'Rockpool', r'rockpool', ['Simon Rockpool']), ('blue-angel', 'Blue Angel', r'blue angel', ['Blue Angel Publishing']),
      ('us-games', 'U.S. Games Systems', r'u\.?s\.? games', ['U.S. Games Systems, Inc.', 'U.S. Games Systems', 'US Games Systems']), ('llewellyn', 'Llewellyn', r'llewellyn', ["Llewellyn's Card", 'Llewellyn Publications', 'Llewellyn Worldwide Ltd.'])]
_V = {v: k for k, _, _, vs in _B for v in vs}
def _bo(title, vendor=''):
    for k, _, rx, _ in _B:
        if re.search(rx, title, re.I): return k
    return _V.get(vendor or '', '')
BR = types.SimpleNamespace(NAME={k: n for k, n, _, _ in _B}, brand_of=_bo, FACTS={})
AISLES = {
 'oracle': ('Oracle Decks', 'Oracle', 'oracle-decks', 'Oracle cards for intuitive readings: angels, goddesses, animals, moon and more.', '#0f766e'),
 'tools': ('Pendulums, Boards & Scrying Mirrors', 'Pendulums', 'pendulums-scrying', 'Crystal and metal pendulums, pendulum boards, scrying mirrors and dowsing rods.', '#7c3aed'),
 'affirm': ('Affirmation & Mini Decks', 'Affirmations', 'affirmation-decks', 'Daily affirmation, inspiration and mini card decks.', '#db2777'),
 'books': ('Psychic Development Books', 'Books', 'psychic-development-books', 'Books on intuition, mediumship, auras, pendulums and palmistry.', '#92400e'),
}
VISIT_EYEBROW = 'Meet a psychic in person'
def STORE_DESC(S): return 'Guide to psychics, mediums and intuitive readers in New York City, with featured readers at Namaste Bookshop near Union Square, plus oracle decks and pendulums.'
REVIEW_TITLE = 'Had a reading at Namaste Bookshop?'
REVIEW_TEXT = 'A quick Google review helps the next person find a reader they can trust.'
LOGO_SVG = '<svg viewBox="0 0 40 40"><circle cx="20" cy="20" r="14" fill="none" stroke="currentColor" stroke-width="2.2"/><path d="M8 20c4-6 20-6 24 0-4 6-20 6-24 0z" fill="none" stroke="currentColor" stroke-width="2"/><circle cx="20" cy="20" r="3.6" fill="#5eead4"/></svg>'
WORDMARK = 'NYC <b>Psychic Readers</b>'
SEARCH_PLACEHOLDER = 'Search oracle decks, pendulums'
QUIZ = None

def _keep(x): return bool(set(x['offers']) & {'psychic', 'mediumship', 'spiritual', 'palm', 'astrology', 'energy'})
_PSY = {'Clairvoyant', 'Psychic', 'Clairaudient', 'Spirit', 'Astrology', 'Healing', 'Energy Work', 'Hypnotherapy', 'Past Life'}
def _keepf(r): return bool(set(r['tags']) & _PSY)
T = {
 'keep': _keep, 'keep_featured': _keepf, 'lp': 'psychics', 'fp': 'featured-psychics', 'dp': 'psychics', 'unit': 'psychics & intuitives',
 'email': 'claim@namastebookshop.com', 'dir_name': 'Psychics',
 'featured_intro': lambda r: f'You can sit with {E(r["name"])} in person at Namaste Bookshop, 2 West 14th Street, between Union Square and Sixth Avenue. Reserve a time through the shop\'s calendar, or phone the readings desk to see who is reading today.',
 'ftitle': lambda r: f'{r["name"]}: Psychic & Intuitive Reader, Namaste Bookshop NYC',
 'fdesc': lambda r: f'Meet {r["name"]}: {r["specialty"]}. Reads in person at Namaste Bookshop, 2 W 14th St, Manhattan. Session lengths, prices, usual days and how to book.',
 'fhub_title': 'Featured Psychics, Mediums & Healers at Namaste Bookshop', 'fhub_h1': 'Featured psychics and intuitives at Namaste Bookshop',
 'fhub_desc': 'Clairvoyants, mediums, astrologers and energy healers who see clients at Namaste Bookshop on West 14th Street, Manhattan.',
 'fhub_lead': 'Clairvoyants, mediums, astrologers and energy healers who see clients at Namaste Bookshop on West 14th Street. Their specialties, session prices and usual days below come from each reader\'s page on namastebookshop.com. Namaste Bookshop and this guide have the same owner, which is why they are featured.',
 'ltitle': lambda x: f'{x["name"]}: Psychic Readings, {x["neighborhood"].split(" (")[0]}, {x["borough"]} NYC',
 'ldesc': lambda x: f'{x["name"]} in {x["neighborhood"]}, {x["borough"]}. {x["note"]} Contact details confirmed on their own website.',
 'listing_note': 'Listed for free.', 'also_in': lambda b: f'Other psychics in {b}', 'all_in': lambda b: f'Every psychic we list in {b}', 'or_featured': 'Featured intuitives near Union Square',
 'feat_h': 'Featured: intuitives you can meet on West 14th Street', 'feat_p': 'Clairvoyants, mediums, astrologers and healers who see clients inside Namaste Bookshop, a short walk from Union Square.',
 'feat_all': 'Meet all featured intuitives', 'feat_other': 'Willing to come into Manhattan? Featured intuitives see clients near Union Square.',
 'btitle': lambda b, n: f'Psychics in {b}: {n} Psychic, Medium & Palm Readers (NYC Guide)',
 'bdesc': lambda b, n, hs: f'Where to get a psychic reading in {b}: {n} psychics, mediums and palm readers in {", ".join(hs[:4])} and nearby, with contact details confirmed on their own sites.',
 'bh1': lambda b: f'Psychic readers in {b}',
 'bintro': {
  'Manhattan': 'Manhattan psychics range from storefront palm and tarot readers in SoHo and the East Village to appointment-only mediums and astrologers uptown. Downtown is the easiest place to find someone the same day.',
  'Brooklyn': 'Brooklyn has storefront psychics in DUMBO and along Flatbush Avenue, and healing centers where intuitive readings sit alongside Reiki and classes.',
  'Queens': 'Queens psychics mostly work from small offices and home studios, with walk-in palm readers in Forest Hills and appointment-based intuitives in Astoria, Flushing and Bayside.',
  'Bronx': 'In the Bronx, readings often happen in botanicas, where a spiritual consultation can include cards, candles and herbal work.',
  'Staten Island': 'On Staten Island you will find storefront psychics with long opening hours, several offering palm, tarot and mediumship under one roof.'},
 'missing': '<b>Do you read in New York and are not here?</b> We add any psychic with a working website describing their practice. <a href="/claim/">Suggest a listing or claim yours</a>.',
 'dtitle': lambda n: f'Psychics in NYC: {n} Psychics, Mediums & Palm Readers by Borough',
 'ddesc': lambda n: f'Looking for a psychic in New York? {n} psychics, mediums, palm readers and intuitive healers across the five boroughs, sorted by the kind of reading and checked against their own websites.',
 'dir_h1': 'Psychics, mediums and intuitive readers in NYC',
 'dir_lead': 'Start with the kind of reading you are after: a medium to connect with someone you lost, a palm reader, an astrologer, or an energy healer. Each listing comes from the practice\'s own website. We do not run ratings, sell reviews or list anyone we could not check.',
 'browse_by': 'Browse by type of reading:',
 'topics': [
  {'slug': 'mediums', 'h1': 'Mediums in NYC', 'title': 'Mediums in NYC: Readers Who Offer Mediumship',
   'desc': lambda n: f'{n} New York psychics and readers who offer mediumship, including featured mediums at Namaste Bookshop.',
   'intro': 'A medium aims to pass on messages from people who have died. If you are grieving, go gently: a good medium never pressures you for more sessions. These readers list mediumship or spirit work on their own pages.',
   'match': lambda x: 'mediumship' in x['offers'], 'fmatch': lambda r: 'Spirit' in r['tags']},
  {'slug': 'palm-readers', 'h1': 'Palm readers in NYC', 'title': 'Palm Readers in NYC: Where to Get Your Palm Read',
   'desc': lambda n: f'{n} places in New York City offering palm readings, from SoHo to Staten Island.', 'intro': 'Palmistry reads the lines, mounts and shape of your hands. It is often quick and is usually offered alongside tarot or psychic readings.',
   'match': lambda x: 'palm' in x['offers']},
  {'slug': 'astrologers', 'h1': 'Astrologers and psychic astrologers in NYC', 'title': 'Astrologers in NYC: Birth Chart & Psychic Astrology Readings',
   'desc': lambda n: f'{n} New York astrologers and psychics who read birth charts, including featured astrologers at Namaste Bookshop.', 'intro': 'An astrologer reads your birth chart: the sky at the moment you were born. Bring your birth date, time and place if you know them.',
   'match': lambda x: 'astrology' in x['offers'], 'fmatch': lambda r: 'Astrology' in r['tags']},
  {'slug': 'energy-healing', 'h1': 'Reiki and energy healing in NYC', 'title': 'Reiki & Energy Healing in NYC: Intuitive Healers',
   'desc': lambda n: f'{n} New York practitioners offering Reiki, chakra and energy work, including healers at Namaste Bookshop.', 'intro': 'Energy work such as Reiki is offered as relaxation and spiritual support, not medical treatment. These practitioners list Reiki, chakra or aura work on their own sites.',
   'match': lambda x: bool(set(x['offers']) & {'reiki', 'energy'}), 'fmatch': lambda r: bool(set(r['tags']) & {'Healing', 'Energy Work', 'Hypnotherapy'})},
  {'slug': 'walk-in-psychics', 'h1': 'Walk-in psychics in NYC', 'title': 'Walk-In Psychics in NYC: Same-Day Readings',
   'desc': lambda n: f'{n} New York psychics that welcome walk-ins for same-day readings.', 'intro': 'Want a reading today? These psychics say on their own sites that walk-ins are welcome. Call ahead if you are traveling far.',
   'match': lambda x: 'walk-in' in x['modes']},
  {'slug': 'downtown-manhattan', 'h1': 'Psychics in downtown Manhattan', 'title': 'Psychics in Downtown Manhattan: SoHo, the Village, Union Square & Chelsea',
   'desc': lambda n: f'{n} psychics and intuitive readers between Midtown South and SoHo, including the featured intuitives on West 14th Street.',
   'intro': 'Below 34th Street is where New York psychics cluster most: storefront readers in SoHo and the East Village, appointment-based astrologers in the West Village, and the featured intuitives at Namaste Bookshop on West 14th Street. Most are within a short subway ride of Union Square.',
   'match': lambda x: x['neighborhood'] in ('Union Square', 'Greenwich Village', 'West Village', 'East Village', 'SoHo', 'Chelsea', 'Midtown South'), 'fmatch': lambda r: True},
 ],
 'claim_title': 'Claim Your Psychic Listing or Add Your Practice', 'claim_desc': 'Psychics, mediums and healers in NYC: claim or correct your free listing, or ask to be added or removed.',
 'claim_h1': 'Claim or add your practice', 'claim_lead': 'Every listing here is free. If one is yours, claim it to fix your details, add hours or a photo, or have it removed. Practicing in New York but missing? Pick "Not listed yet" below.',
 'ad_title': 'Advertise Your Psychic Practice in NYC', 'ad_desc': 'Reach people looking for a psychic, medium or healer in New York City with a labeled featured placement.',
 'ad_h1': 'Reach people looking for a psychic in New York', 'ad_subject': 'Featured placement on NYC Psychic Readers',
 'ad_lead': 'Visitors arrive here ready to book: they are searching for a medium, a palm reader or a psychic in their borough. A featured spot puts your practice first, with your photo and booking link.',
 'ad_feat': 'your photo, the readings you offer, your hours and a booking link, placed above the free listings and labeled Featured.',
 'guide_cta': 'Find a psychic',
 'guides': [
  {'path': '/guide/how-to-find-a-real-psychic/', 'h1': 'How to find a genuine psychic in New York', 'title': 'How to Find a Genuine Psychic in NYC: Signs and Warning Signs',
   'desc': 'How to tell a sincere psychic from a scam in New York: what good practitioners do, the curse-removal trap, and questions to ask before you pay.',
   'html': '''<p class="lead">Most psychics are sincere. A few are not. The difference usually shows up in how they talk about money.</p>
<h2>What sincere psychics tend to do</h2><ul><li>Name the price and length before they start.</li><li>Let you lead with what matters to you.</li><li>Describe impressions as possibilities, not certainties.</li><li>Encourage you to make your own choices.</li><li>Send you to a professional for health, legal or money problems.</li></ul>
<h2>The classic scam</h2><p>The reading turns dark: you have a curse, a hex or "negative energy," and it can be lifted for a large fee, often paid in installments or by "cleansing" your money. Walk away. No genuine reader needs your savings to help you.</p>
<h2>Questions to ask first</h2><ul><li>How long is the session, and what does it cost?</li><li>Do you use cards, palms, astrology, or pure intuition?</li><li>Can I record or take notes?</li></ul>
<h2>Trust your gut</h2><p>If you feel pressured, frightened or rushed, end the session. You can always book someone else.</p>'''},
  {'path': '/guide/psychic-reading-prices/', 'h1': 'How psychic readings are priced in NYC', 'title': 'Psychic Reading Prices in NYC: What Affects the Cost',
   'desc': 'How New York psychics, mediums and palm readers set prices, why mediumship can cost more, and how to avoid upsells.',
   'html': '''<p class="lead">Psychic readings are usually sold by time, but the type of reading matters too.</p>
<h2>Typical pricing patterns</h2><ul><li><b>Palm readings</b> are often the quickest and among the least expensive options.</li><li><b>Psychic and tarot readings</b> are usually priced by the length of the session.</li><li><b>Mediumship and astrology</b> sessions often run longer and may cost more because they take preparation or deeper focus.</li><li><b>Energy work</b> like Reiki is usually priced per session, sometimes in packages.</li></ul>
<h2>Watch out for</h2><ul><li>A very cheap introductory offer that leads to a pitch for expensive "spiritual work."</li><li>Prices that change once the reading has started.</li></ul>
<h2>See published prices</h2><p>The featured intuitives at Namaste Bookshop list session lengths and prices on their profiles here, as published on the shop's website. For other listings, check the practice's own site or call.</p>'''},
  {'path': '/guide/psychic-vs-tarot-reading/', 'h1': 'Psychic, medium or tarot reader: who should you see?', 'title': 'Psychic vs Medium vs Tarot Reader: Which Reading Is Right for You?',
   'desc': 'The difference between a psychic, a medium, a tarot reader, an astrologer and a palm reader, and which to book for your question.',
   'html': '''<p class="lead">They overlap, but each one starts from a different place.</p>
<h2>Psychic</h2><p>Works mainly from intuition, sometimes using a focus such as cards or a crystal. Good for open questions about direction and relationships.</p>
<h2>Medium</h2><p>Aims to connect with people who have passed. Book a medium if you are hoping for contact with a loved one.</p>
<h2>Tarot reader</h2><p>Lays out cards and reads their meanings for your question. Structured and visual; you can see what they see.</p>
<h2>Astrologer</h2><p>Reads your birth chart and the current planetary picture. Good for timing and long-term patterns. Bring your birth time.</p>
<h2>Palm reader</h2><p>Reads the lines and shape of your hands. Usually quick, often offered alongside other readings.</p>
<h2>Energy healer</h2><p>Offers Reiki, chakra or aura work aimed at relaxation and balance rather than predictions.</p>
<p class="small">Readings are for reflection and entertainment and are not a substitute for professional medical, legal or financial advice.</p>'''},
  {'path': '/guide/before-your-first-psychic-reading/', 'h1': 'Before your first psychic reading', 'title': 'First Psychic Reading Tips: How to Prepare and What to Ask',
   'desc': 'How to get the most from a first psychic or medium reading in NYC: preparing questions, how much to share, recording, and what to do afterwards.',
   'html': '''<p class="lead">A first reading can feel strange. A little preparation helps.</p>
<h2>Decide what you want</h2><p>Write down two or three questions or areas. For mediumship, think about who you hope to hear from, but you do not need to tell the medium details up front.</p>
<h2>Share a little, not everything</h2><p>Answer honestly when asked, but let the reader do the work. That way you can judge what comes through.</p>
<h2>Take notes</h2><p>Ask whether you can record or write things down. Messages often make more sense days later.</p>
<h2>Afterwards</h2><p>Treat what you heard as one perspective. Use what resonates, let go of what does not, and never make a major decision on a reading alone.</p>
<p>Want to practice your own intuition? Try an <a href="/shop/oracle-decks/">oracle deck</a> or a <a href="/shop/pendulums-scrying/">pendulum</a>.</p>'''},
 ],
}
def HERO_HTML(S):
    L, F = dirlib.load(T)
    return f'''<section class="dhero"><div class="wrap"><p class="eyebrow">Psychics &middot; Mediums &middot; Palm readers &middot; Healers</p><h1>Psychic readers in New York City</h1>
<p>{len(L) + len(F)} psychics, mediums, astrologers and intuitive healers across the five boroughs. Choose the kind of reading you want, then find someone near you.</p>
<div class="btns"><a class="btn" href="/psychics/">Find a psychic</a><a class="btn ghost" href="/psychics/mediums/">Mediums</a><a class="btn ghost" href="/featured-psychics/">Featured</a></div>
<p class="heroloc">Featured intuitives see clients inside <b>Namaste Bookshop</b>, 2 W 14th St, just west of Fifth Ave near Union Square.</p>
<div class="dstats"><div><b>{len(L) + len(F)}</b>psychics &amp; intuitives</div><div><b>{len(F)}</b>featured on 14th St</div><div><b>{len({x["borough"] for x in L})}</b>boroughs</div></div></div></section>'''
def _types(S):
    L, F = dirlib.load(T)
    tiles = ''.join(f'<a href="/psychics/{g["slug"]}/"><b>{E(g["h1"].replace(" in NYC", ""))}</b><span>{sum(1 for x in L if g["match"](x)) + sum(1 for r in F if g.get("fmatch", lambda r: False)(r))} listed</span></a>' for g in T['topics'])
    return (f'<section class="wrap"><div class="sechead"><h2>What kind of reading?</h2></div><div class="boros">{tiles}</div></section>'
            f'<section class="wrap"><div class="sechead"><h2>Featured intuitives on West 14th Street</h2><a href="/featured-psychics/">See all {len(F)} &rarr;</a></div><p class="intro">{T["feat_p"]}</p>{dirlib.featured_grid(T, F, 6)}'
            f'<div class="btns"><a class="btn" href="{BOOK}" rel="noopener">Reserve a reading at Namaste Bookshop</a></div></section>'
            f'<section class="wrap"><div class="sechead"><h2>Psychics by borough</h2><a href="/psychics/">Full guide &rarr;</a></div>{dirlib.boro_tiles(T, L)}</section>')
def _guides(S):
    return '<section class="wrap"><div class="sechead"><h2>Read this before you pay anyone</h2></div><ul class="whys">' + ''.join(f'<li><b><a href="{g["path"]}">{E(g["h1"])}</a></b><span>{E(g["desc"])}</span></li>' for g in T['guides']) + '</ul></section>'
def _cta(S): return '<section class="wrap"><div class="claim"><b>A psychic, medium or healer in NYC?</b> Your listing is free. <a href="/claim/">Claim or add it</a> &middot; <a href="/advertise/">Featured placement</a></div></section>'
def _oracle(S): return [x for x in S.by_rank(S.leaders) if x['aisle'] == 'oracle' and not x['noimg']][:8]
def _pend(S): return [x for x in S.by_rank(S.leaders) if x['aisle'] == 'tools' and not x['noimg']][:8]
HERO = lambda S: {'eyebrow': '', 'h1': '', 'lede': '', 'shop_cta': ''}
HERO_BASES = ('oracle',)
HOME_SECTIONS = [
 {'type': 'html', 'html': _types},
 {'type': 'html', 'html': _guides},
 {'type': 'grid', 'title': 'Oracle decks for your own intuition', 'select': _oracle, 'href': '/shop/oracle-decks/', 'link': 'All oracle decks'},
 {'type': 'grid', 'title': 'Pendulums and scrying tools', 'select': _pend, 'href': '/shop/pendulums-scrying/', 'link': 'All pendulums'},
 {'type': 'html', 'html': _cta},
 {'type': 'visit'},
]
def HOME_TITLE(S): return 'Psychics in NYC | Psychic Readers, Mediums & Palm Readers in New York'
def HOME_DESC(S):
    L, F = dirlib.load(T)
    return f'Find a psychic in New York City: {len(L) + len(F)} psychics, mediums, palm readers, astrologers and healers by borough and type of reading. Featured intuitives near Union Square, plus oracle decks.'
def HOME_LD(S):
    L, F = dirlib.load(T)
    return [S.store_ld(), {'@context': 'https://schema.org', '@type': 'Organization', 'name': 'Wealth Edge Ventures Inc.', 'brand': S.BRAND, 'url': S.SITE + '/'},
            dirlib.itemlist(S, 'Psychic readers in New York City', [(r['name'], f'/featured-psychics/{r["slug"]}/') for r in F] + [(x['name'], f'/psychics/{x["slug"]}/') for x in L])]
def LLMS_EXTRA(S):
    L, F = dirlib.load(T)
    return (['## Psychic directory', f'- [Psychics in NYC]({S.SITE}/psychics/): {len(L) + len(F)} psychics, mediums, palm readers, astrologers and healers; machine-readable data at {S.SITE}/data/listings.json']
            + [f'- [{g["h1"]}]({S.SITE}/psychics/{g["slug"]}/)' for g in T['topics']] + [f'- [Psychic readers in {b}]({S.SITE}/psychics/{dirlib.slug(b)}/)' for b in dirlib.BORO if any(x["borough"] == b for x in L)]
            + ['', '## Featured intuitives at Namaste Bookshop (2 W 14th St; booking https://namastebookshop.com/pages/book-a-reading)'] + [f'- [{r["name"]}]({S.SITE}/featured-psychics/{r["slug"]}/): {r["specialty"]}' for r in F]
            + ['', '## Guides'] + [f'- [{g["h1"]}]({S.SITE}{g["path"]})' for g in T['guides']] + [''])
def GUIDES(S): return dirlib.pages(T, S)
def SHOP_TITLE(S): return 'Oracle Decks, Pendulums & Psychic Development Books | NYC Psychic Readers'
def SHOP_DESC(S): return f'{S.N:,} oracle decks, pendulums, scrying mirrors and books on intuition. Ships from NYC or pick up at 2 W 14th St.'
SHOP_H1 = 'Tools for your own intuition'
def SHOP_SUB(S): return f'{S.N:,} oracle decks, pendulums and books.'
def AISLE_TITLE(S, k): return f'{AISLES[k][0]} | NYC Psychic Readers'
def AISLE_DESC(S, k): return f'{AISLES[k][3]} {S.cat_count[k]} in stock, shipped from NYC or picked up near Union Square.'
def FOOTER_EXPLORE(S):
    return [('Find a psychic', '/psychics/'), ('Mediums', '/psychics/mediums/'), ('Palm readers', '/psychics/palm-readers/'), ('Featured intuitives', '/featured-psychics/'),
            ('Spotting a real psychic', '/guide/how-to-find-a-real-psychic/'), ('Claim a listing', '/claim/'), ('Oracle decks', '/shop/oracle-decks/')]
FOOT_BLURB = 'An honest guide to psychics, mediums and intuitive healers in New York City. No ratings for sale, no invented listings.'
def LANDINGS(S):
    return [{'path': f'/oracle/{k}/', 'title': f'{n} Oracle Decks | NYC Psychic Readers', 'desc': f'{S.fam_count[k]} {n.lower()} oracle decks and tools in stock.',
             'h1': f'{n} oracle decks', 'sub': f'{S.fam_count[k]} in stock.', 'filter': {'fam': [k]}} for k, n, _ in FAMILIES if S.fam_count[k] >= 4]
def brand_intro(S, k, st): return f'<p>{st["n"]} oracle and intuition titles from {E(S.BRAND_NAME[k])}, from {S.money(st["min"])}.</p>'
def brand_faq(S, k, st): return [(f'Do you carry {S.BRAND_NAME[k]}?', f'Yes, {st["n"]} titles today.')]
def BRAND_H1(S, k): return f'{S.BRAND_NAME[k]} oracle decks'
def BRAND_TITLE(S, k, st): return f'{S.BRAND_NAME[k]} Oracle Decks | NYC Psychic Readers'
def BRAND_DESC(S, k, st): return f'{st["n"]} {S.BRAND_NAME[k]} oracle decks and books from {S.money(st["min"])}.'
def BRANDS_TITLE(S): return 'Oracle Deck Publishers | NYC Psychic Readers'
def BRANDS_DESC(S): return 'Oracle decks by publisher.'
BRANDS_H1 = 'Oracle deck publishers'
def BRANDS_LEAD(S, n): return f'{n} publishers.'
PAIR = {'oracle': ['tools', 'books'], 'tools': ['oracle', 'books'], 'affirm': ['oracle'], 'books': ['oracle', 'tools']}
CART_PAIR_TITLE = 'Add to your practice'
REL_BRAND = 'More from {brand}'
REL_SCENT = 'More {scent}'
REL_PAIR = 'Works well with'
REL_MORE = 'More {aisle}'
def describe(S, x):
    fam = S.FAM_NAME.get(x['family'], '')
    s = [f"{E(x['title'])}, chosen for building your own intuition."]
    s.append({'oracle': 'Oracle decks have no fixed structure like tarot, so each card speaks on its own: easy to start with.', 'tools': 'Pendulums and scrying tools are simple ways to practice yes-and-no questions and quiet focus.',
              'affirm': 'Pull one card a day as a prompt.', 'books': 'A guide for developing your own intuitive skills.'}[x['aisle']])
    if fam: s.append(f'Theme: {E(fam)}.')
    s.append('Curious what a professional sees? <a href="/featured-psychics/">Meet the featured intuitives</a>. Ships from New York City, or pick up at Namaste Bookshop, 2 West 14th Street.')
    return s
def PRODUCT_DESC(S, x, v0): return f"{x['title']}, {S.money(v0['price'])}. Ships from NYC or pick up at 2 W 14th St."
def ABOUT_DESC(S): return 'About NYC Psychic Readers: who runs this guide, how psychics are listed and checked, and what Featured means.'
ABOUT_H1 = 'About NYC Psychic Readers'
def ABOUT(S):
    return f'''<p class="lead">NYC Psychic Readers is an independent-minded guide to psychics, mediums and intuitive healers in New York City.</p>
<h2>Our listing rules</h2><p>A practice is listed only if it has its own working website describing current services in New York. We take the name, neighborhood, address and phone from that site and link to it, with the date checked. We never publish star ratings, copy reviews, or create listings for businesses we could not confirm. Any practice can <a href="/claim/">claim, update or remove</a> its page.</p>
<h2>Who we are</h2><p>{S.LEGAL} The same company owns Namaste Bookshop at {S.STORE_ADDR}. Readers marked <b>Featured</b> see clients at Namaste Bookshop; their details come from namastebookshop.com. Other practices may buy clearly labeled featured placement (<a href="/advertise/">details</a>).</p>
<h2>The shop</h2><p>We also sell oracle decks, pendulums and books on intuition. Orders check out on Shopify via <a href="{S.SHOP}" rel="noopener">namastebookshop.com</a>, ship from New York, or can be picked up at Namaste Bookshop.</p>{S.hours_html()}'''
def FAQ_DESC(S): return 'Common questions about NYC Psychic Readers: how listings work, Featured placements, mediums, prices and booking.'
FAQ_H1 = 'Questions about this guide'
def FAQ(S):
    return [('Do you vouch for the psychics listed?', 'We confirm each practice exists and that its details match its own website. We do not rate readers; use our guide on finding a genuine psychic.'),
            ('Why are some readers Featured?', 'They see clients at Namaste Bookshop, owned by the same company as this guide, or they paid for a labeled placement.'),
            ('Where can I see a medium?', 'See <a href="/psychics/mediums/">mediums in NYC</a>.'),
            ('Can I get a reading today?', 'Try the <a href="/psychics/walk-in-psychics/">walk-in psychics</a>, or call Namaste Bookshop\'s readings line at 212-645-0141.'),
            ('How do I add or remove my practice?', 'Use the free <a href="/claim/">claim form</a>.')]
NOT_FOUND = 'We did not see that one coming'
