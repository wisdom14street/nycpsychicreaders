"""Tag referrals to our shop without changing destination paths or existing parameters."""
import re
from html import escape, unescape
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit


def tag_shop_url(url, source, content):
    parts = urlsplit(url)
    if parts.scheme != 'https' or parts.netloc.lower() not in ('namastebookshop.com', 'www.namastebookshop.com'):
        return url
    query = parse_qsl(parts.query, keep_blank_values=True)
    present = {key for key, _ in query}
    for key, value in (('utm_source', source), ('utm_medium', 'referral'),
                       ('utm_campaign', 'namaste_network'), ('utm_content', content)):
        if key not in present:
            query.append((key, value))
    return urlunsplit(parts._replace(query=urlencode(query)))


def tag_shop_links(document, source, path):
    # Only anchor hrefs; canonical, schema, scripts, images and Square URLs stay intact.
    def replace(match):
        prefix, quote, href = match.groups()
        tagged = tag_shop_url(unescape(href), source, path)
        return prefix + quote + escape(tagged, quote=True) + quote
    return re.sub(r'(<a\b[^>]*?\shref=)([\"\'])(.*?)\2', replace, document, flags=re.I)
