# nycpsychicreaders.com

NYC Psychic Readers: static site built daily from the public namastebookshop.com catalog and deployed to GitHub Pages.
NYC Psychic Readers is a brand of Wealth Edge Ventures Inc., which also owns Namaste Bookshop (2 W 14th St, New York).

- `site/config.json`: site settings (`REVIEW_URL`, `GOOGLE_SITE_VERIFICATION` stay hidden while empty).
- `site/sitecopy.py`: product mix rules, pages and all copy for this site.
- `scripts/p2site.py`: find-us, sales and link-preview copy.
- `site/theme.css`, `site/favicon.svg`, `src/static/og.jpg`: design and link preview.
- Checkout: cart permalinks to namastebookshop.com tagged with `attributes[Storefront]=NYC Psychic Readers`.
- Directory: `site/listings.json` holds verified listings (each with `source_url` and `verified_on`); `site/featured.json` holds Namaste Bookshop readers taken from namastebookshop.com. `site/dirlib.py` renders listing, borough, topic, claim and advertise pages and writes `dist/data/listings.json`. Add or correct a listing only after checking the business's own website.
