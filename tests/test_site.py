"""Offline regression checks. Synthetic products are built only in a temporary copy.

Run: python3 -m unittest discover -s tests -v
Browser checks need playwright and Chromium; all external requests are intercepted.
"""
import functools
import http.server
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import threading
import unittest
from html.parser import HTMLParser
from urllib.parse import parse_qs, urlsplit
from xml.etree import ElementTree

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from attribution import tag_shop_links, tag_shop_url


class Document(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.tags = []
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        self.tags.append((tag, dict(attrs)))


class AttributionTests(unittest.TestCase):
    def test_cart_parameters_and_existing_campaign_survive(self):
        url = tag_shop_url('https://namastebookshop.com/cart/101:2?attributes%5BStorefront%5D=NYC+Psychic+Readers&note=hello&ref=nycpsychicreaders&utm_source=existing#top', 'nycpsychicreaders.com', '/shop/')
        parts = urlsplit(url)
        self.assertEqual(parts.path, '/cart/101:2')
        self.assertEqual(parts.fragment, 'top')
        query = parse_qs(parts.query)
        self.assertEqual(query['attributes[Storefront]'], ['NYC Psychic Readers'])
        self.assertEqual(query['note'], ['hello'])
        self.assertEqual(query['ref'], ['nycpsychicreaders'])
        self.assertEqual(query['utm_source'], ['existing'])
        self.assertEqual(query['utm_medium'], ['referral'])
        self.assertEqual(tag_shop_url(url, 'ignored', '/ignored/'), url)

    def test_only_exact_shop_hosts_are_tagged(self):
        for url in ('https://book.squareup.com/appointments/test', '/shop/', 'tel:+12126450141',
                    'https://namastebookshop.com.example.org/', 'https://example.org/?next=namastebookshop.com'):
            self.assertEqual(tag_shop_url(url, 'nycpsychicreaders.com', '/'), url)

    def test_static_links_work_without_javascript(self):
        html = '<a href="https://namastebookshop.com/pages/book-a-reading?x=1&amp;y=2">Book</a><link rel="canonical" href="https://namastebookshop.com/">'
        tagged = tag_shop_links(html, 'nycpsychicreaders.com', '/featured-psychics/catherine-marks/')
        tags = Document(tagged).tags
        query = parse_qs(urlsplit(tags[0][1]['href']).query)
        self.assertEqual(query['utm_source'], ['nycpsychicreaders.com'])
        self.assertEqual(query['x'], ['1'])
        self.assertEqual(query['y'], ['2'])
        self.assertEqual(tags[1][1]['href'], 'https://namastebookshop.com/')


def fixture_products():
    specs = [('Angel Oracle Test', 'Oracle Cards'), ('Moon Oracle Test', 'Oracle Cards'),
             ('Goddess Oracle Test', 'Oracle Cards'), ('Animal Oracle Test', 'Oracle Cards'),
             ('Pendulum Test', 'Pendulum'), ('Affirmation Test', 'Affirmation Cards'),
             ('Psychic Development Test', 'Book')]
    products = []
    for index, (title, kind) in enumerate(specs, 1):
        products.append({'id': index, 'title': title, 'handle': f'fixture-{index}', 'product_type': kind,
                         'vendor': 'Test publisher', 'created_at': '2026-01-01T00:00:00Z',
                         'images': [{'src': f'https://cdn.shopify.com/fixture-{index}.jpg'}],
                         'variants': [{'id': index * 100 + 1, 'title': 'Standard', 'price': '20.00', 'available': True, 'sku': f'TEST-{index}'},
                                      {'id': index * 100 + 2, 'title': 'Large', 'price': '30.00', 'available': True, 'sku': f'TEST-{index}-L'},
                                      {'id': index * 100 + 3, 'title': 'Sold out', 'price': '40.00', 'available': False, 'sku': f'TEST-{index}-X'}]})
    return products


class SiteFixture:
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory(prefix='nycpsychicreaders-test-')
        cls.root = Path(cls.temp.name)
        for name in ('scripts', 'site', 'src'):
            shutil.copytree(ROOT / name, cls.root / name, ignore=shutil.ignore_patterns('__pycache__'))
        (cls.root / 'data').mkdir()
        (cls.root / 'data/all_products.json').write_text(json.dumps(fixture_products()))
        cls.build_output = subprocess.check_output([sys.executable, 'scripts/build.py'], cwd=cls.root, text=True)
        cls.dist = cls.root / 'dist'

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()


class BuildTests(SiteFixture, unittest.TestCase):
    def test_metadata_and_sitemap(self):
        urls = ElementTree.parse(self.dist / 'sitemap.xml').getroot()
        locations = [node.find('{*}loc').text for node in urls]
        self.assertEqual(len(locations), len(set(locations)))
        self.assertFalse(any(node.find('{*}lastmod') is not None for node in urls))
        for url in locations:
            path = urlsplit(url).path
            page = self.dist / path.lstrip('/') / 'index.html'
            self.assertTrue(page.exists(), url)
            tags = Document(page.read_text()).tags
            canonical = [attrs['href'] for tag, attrs in tags if tag == 'link' and attrs.get('rel') == 'canonical']
            self.assertEqual(canonical, [url])
            for key in ('og:image:alt', 'og:image:width', 'twitter:image:alt'):
                self.assertLessEqual(sum(attrs.get('property', attrs.get('name')) == key for _, attrs in tags), 1, (url, key))
        self.assertNotIn('https://nycpsychicreaders.com/cart/', locations)
        self.assertNotIn('https://nycpsychicreaders.com/404.html', locations)
        for path in ('cart/index.html', '404.html'):
            self.assertIn('content="noindex"', (self.dist / path).read_text())
        self.assertIn('Sitemap: https://nycpsychicreaders.com/sitemap.xml', (self.dist / 'robots.txt').read_text())

    def test_prices_ids_and_direct_booking_urls_are_preserved(self):
        page = (self.dist / 'products/fixture-1/index.html').read_text()
        self.assertIn('data-v="101"', page)
        self.assertIn('data-p="20.00"', page)
        self.assertIn('"price": "30.00"', page)
        self.assertIn('G-Y7R5K9NMW0', page)
        self.assertIn('/assets/ga.js', page)
        self.assertIn('<noscript>', page)
        readers = json.loads((ROOT / 'site/featured.json').read_text())
        for reader in readers:
            profile = self.dist / 'featured-psychics' / reader['slug'] / 'index.html'
            if not profile.exists():
                continue  # This site's topic filter intentionally includes a subset of Namaste readers.
            text = profile.read_text()
            tags = Document(text).tags
            links = [attrs.get('href', '') for tag, attrs in tags if tag == 'a']
            self.assertIn(reader['book_direct'], links)
            self.assertIn('Choose an available time and confirm your appointment on Square', text)
            for _, price in reader['services']:
                self.assertIn(price, text)
            self.assertNotIn('"makesOffer"', text)

    def test_referral_markers_on_shop_handoffs(self):
        for page in self.dist.rglob('*.html'):
            for tag, attrs in Document(page.read_text()).tags:
                if tag != 'a':
                    continue
                url = urlsplit(attrs.get('href', ''))
                if url.hostname == 'namastebookshop.com':
                    self.assertEqual(parse_qs(url.query).get('utm_source'), ['nycpsychicreaders.com'], str(page))

    def test_uncertain_roster_entries_dont_promise_a_schedule(self):
        for slug in ('alyssa-witte', 'karla-vera', 'melissa'):
            page = (self.dist / f'featured-psychics/{slug}/index.html').read_text()
            self.assertIn('confirm current availability', page)
            self.assertNotIn('Usual schedule (New York time)', page)
            self.assertNotIn('"worksFor"', page)

    def test_preview_disables_analytics_and_indexing(self):
        subprocess.check_output([sys.executable, 'scripts/build.py', '--preview'], cwd=self.root, text=True)
        try:
            page = (self.dist / 'index.html').read_text()
            self.assertNotIn('googletagmanager.com', page)
            self.assertNotIn('/assets/ga.js', page)
            self.assertIn('noindex,nofollow', page)
            self.assertIn('Disallow: /', (self.dist / 'robots.txt').read_text())
        finally:
            subprocess.check_output([sys.executable, 'scripts/build.py'], cwd=self.root, text=True)


class BrowserTests(SiteFixture, unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from playwright.sync_api import sync_playwright
        super().setUpClass()
        class QuietHandler(http.server.SimpleHTTPRequestHandler):
            def log_message(self, *_):
                pass
        cls.server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), functools.partial(QuietHandler, directory=str(cls.dist)))
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls.base = f'http://127.0.0.1:{cls.server.server_port}'
        cls.pw = sync_playwright().start()
        cls.browser = cls.pw.chromium.launch(executable_path=os.environ.get('CHROMIUM_PATH', '/usr/bin/chromium'), headless=True, args=['--no-sandbox'])

    @classmethod
    def tearDownClass(cls):
        cls.browser.close()
        cls.pw.stop()
        cls.server.shutdown()
        cls.server.server_close()
        super().tearDownClass()

    def setUp(self):
        self.context = self.browser.new_context()
        self.context.add_init_script('window.__events=[]; window.dataLayer={push:function(args){window.__events.push(Array.from(args))}};')
        self.mode = 'ok'
        self.max_quantity = 2
        self.context.route('**/*', self.route)
        self.page = self.context.new_page()

    def tearDown(self):
        self.context.close()

    def route(self, route):
        url = urlsplit(route.request.url)
        if url.hostname == '127.0.0.1':
            return route.continue_()
        if url.hostname == 'namastebookshop.com' and url.path.endswith('.js'):
            if self.mode == 'offline':
                return route.abort()
            if self.mode == 'missing_product':
                return route.fulfill(status=404, body='Not found')
            variants = [{'id': 101, 'title': 'Standard', 'price': 2000, 'available': self.mode != 'sold_out', 'quantity_rule': {'max': self.max_quantity}},
                        {'id': 102, 'title': 'Large', 'price': 3000, 'available': True, 'quantity_rule': {'max': self.max_quantity}}]
            if self.mode == 'missing_variant':
                variants = variants[1:]
            return route.fulfill(json={'variants': variants}, headers={'Access-Control-Allow-Origin': '*'})
        # Do not contact Google Analytics, Shopify checkout, Square, images, maps or fonts.
        return route.abort()

    def events(self, name):
        return self.page.evaluate('(name)=>window.__events.filter(e=>e[0]==="event"&&e[1]===name).map(e=>e[2])', name)

    def test_cart_checkout_markers_and_quantity_events(self):
        self.page.goto(self.base + '/products/fixture-1/')
        self.page.wait_for_function('document.querySelector("#buy").dataset.max === "2"')
        for count in (1, 2, 3):
            self.page.locator('#buy').click()
            if count < 3:
                self.page.keyboard.press('Escape')
                self.page.wait_for_function('document.querySelector("#cart").hidden')
        self.assertEqual(len(self.events('add_to_cart')), 2)
        self.assertEqual([e['items'][0]['quantity'] for e in self.events('add_to_cart')], [1, 1])
        checkout = urlsplit(self.page.evaluate('window.NI_CART_URL()'))
        self.assertEqual(checkout.hostname, 'namastebookshop.com')
        self.assertEqual(checkout.path, '/cart/101:2')
        query = parse_qs(checkout.query)
        for key, value in {'attributes[Storefront]': 'NYC Psychic Readers', 'attributes[Site]': 'nycpsychicreaders.com',
                           'ref': 'nycpsychicreaders', 'utm_source': 'nycpsychicreaders.com', 'utm_medium': 'referral',
                           'utm_campaign': 'namaste_network', 'utm_content': 'checkout'}.items():
            self.assertEqual(query[key], [value])
        self.page.evaluate('document.addEventListener("click",e=>{if(e.target.closest("[data-checkout]"))e.preventDefault()})')
        self.page.locator('[data-checkout]').click()
        self.assertEqual(len(self.events('begin_checkout')), 1)
        self.assertEqual(self.events('begin_checkout')[0]['value'], 40)
        self.assertFalse(self.events('purchase'))
        self.assertFalse(self.events('generate_lead'))
        self.assertFalse(self.events('shop_click'))

    def test_booking_contact_and_directions_clicks_are_not_conversions(self):
        self.page.goto(self.base + '/featured-psychics/catherine-marks/')
        self.page.evaluate('document.addEventListener("click",e=>e.preventDefault());')
        for url, expected in [('https://namastebookshop.com/pages/book-a-reading?email=private@example.com', 'booking_click'),
                              ('https://book.squareup.com/appointments/test?secret=hidden', 'booking_click'),
                              ('tel:+12126450141', 'phone_click'), ('mailto:claim@namastebookshop.com?body=private', 'claim_click'),
                              ('mailto:info@namastebookshop.com?subject=private', 'email_click'),
                              ('https://www.google.com/maps/dir/?api=1&destination=Shop', 'directions_click')]:
            self.page.evaluate('(href)=>{const a=document.createElement("a");a.href=href;a.textContent="Contact";document.body.append(a);a.click();a.remove()}', url)
            event = self.events(expected)[-1]
            self.assertNotIn('private', json.dumps(event))
            self.assertNotIn('hidden', json.dumps(event))
            self.assertNotIn('?', event['link_url'])
        self.assertFalse(self.events('generate_lead'))
        self.assertFalse(self.events('purchase'))

    def test_offline_variant_change_preserves_price_and_checkout_option(self):
        self.mode = 'offline'
        self.page.goto(self.base + '/products/fixture-1/')
        self.page.select_option('#variant', '102')
        self.assertEqual(self.page.locator('#price').inner_text(), '$30.00')
        self.assertIn('Confirm current availability', self.page.locator('#stock').inner_text())
        self.page.locator('#buy').click()
        self.assertIn('/cart/102:1?', self.page.evaluate('window.NI_CART_URL()'))
        self.assertEqual(self.events('add_to_cart')[0]['items'][0]['price'], 30)

    def test_unavailable_products_cannot_be_added(self):
        for mode in ('sold_out', 'missing_variant', 'missing_product'):
            self.mode = mode
            self.page.goto(self.base + '/products/fixture-1/')
            self.page.wait_for_function('document.querySelector("#buy").disabled')
            self.assertFalse(self.events('add_to_cart'))

    def test_missing_analytics_does_not_break_cart(self):
        self.page.goto(self.base + '/products/fixture-1/')
        self.page.evaluate('window.gtag=undefined')
        self.page.locator('#buy').click()
        self.assertIn('/cart/101:1?', self.page.evaluate('window.NI_CART_URL()'))

    def test_mobile_reader_page_and_cart_are_usable(self):
        self.page.set_viewport_size({'width': 390, 'height': 844})
        self.page.goto(self.base + '/featured-psychics/catherine-marks/')
        self.assertLessEqual(self.page.evaluate('document.documentElement.scrollWidth'), 390)
        self.page.locator('.menu').click()
        self.assertEqual(self.page.locator('.menu').get_attribute('aria-expanded'), 'true')
        self.page.goto(self.base + '/products/fixture-1/')
        self.page.locator('#buy').click()
        self.assertTrue(self.page.locator('#cart').is_visible())
        self.page.keyboard.press('Escape')
        self.page.wait_for_function('document.querySelector("#cart").hidden')
        self.assertEqual(self.page.locator('#buy').evaluate('(e)=>e===document.activeElement'), True)


if __name__ == '__main__':
    unittest.main()
