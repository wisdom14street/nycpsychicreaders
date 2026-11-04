# nycpsychicreaders.com

NYC Psychic Readers: static site built daily from the public namastebookshop.com catalog and deployed to GitHub Pages.
NYC Psychic Readers is a brand of Wealth Edge Ventures Inc., which also owns Namaste Bookshop (2 W 14th St, New York).

- `site/config.json`: site settings (`REVIEW_URL`, `GOOGLE_SITE_VERIFICATION` stay hidden while empty).
- `site/sitecopy.py`: product mix rules, pages and all copy for this site.
- `scripts/p2site.py`: find-us, sales and link-preview copy.
- `site/theme.css`, `site/favicon.svg`, `src/static/og.jpg`: design and link preview.
- Checkout: cart permalinks to namastebookshop.com tagged with `attributes[Storefront]=NYC Psychic Readers`.
- Directory: `site/listings.json` holds verified listings (each with `source_url` and `verified_on`); `site/featured.json` holds Namaste Bookshop readers taken from namastebookshop.com. `site/dirlib.py` renders listing, borough, topic, claim and advertise pages and writes `dist/data/listings.json`. Add or correct a listing only after checking the business's own website.

Referral links to Namaste include `utm_source=nycpsychicreaders.com`, `utm_medium=referral`, and `utm_campaign=namaste_network`. Checkout also preserves the existing Storefront and Site attributes, order note, and referral code. These markers identify a handoff; paid orders must be counted from confirmed Shopify transactions. Square links retain their original destinations. Click tracking cannot verify a completed or paid appointment.

GA4 `G-Y7R5K9NMW0` remains configured. Contact and booking interactions use explicit `*_click` events instead of `generate_lead`. See [the review and measurement notes](docs/review-2026-11-04.md) for event meanings, verification evidence, and remaining access requirements.

Run the offline regression suite with Python 3.12, Pillow, Playwright, and Chromium installed:

```sh
python3 -m unittest discover -s tests -v
```

Set `CHROMIUM_PATH` if Chromium is not at `/usr/bin/chromium`. Tests build synthetic catalog fixtures in a temporary copy and intercept external browser requests; they never submit orders or appointments. The existing daily production workflow still fetches the real public Namaste catalog. Reader profiles are maintained separately: recheck their source pages and the main reader roster, and remove an `availability_note` only after confirming the reader's current status.
