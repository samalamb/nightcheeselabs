# nightcheeselabs.co

Public website for Night Cheese Labs LLC. Plain HTML and CSS, no build step. GitHub Pages serves the files as they are.

| File | Page |
| --- | --- |
| `index.html` | Home and products |
| `contact.html` | Support contact |
| `refunds.html` | Refunds & cancellation |
| `privacy.html` | Privacy policy for this site |
| `404.html` | Not-found page (GitHub Pages serves it automatically) |
| `style.css` | All styles |
| `CNAME` | Custom domain for GitHub Pages |
| `favicon.svg`, `favicon-32.png`, `apple-touch-icon.png` | Browser and home-screen icons |
| `og-image.png` | Link preview image (1200×630) |
| `assets/` | Source SVGs for the logo marks and the link preview |
| `_tools/build_marks.py` | Regenerates `assets/`, the icons and `og-image.png` (not published) |

The header and footer are copied into each page. Change them in every file.

## Logo

Two marks, both in the site's ink and cheese colours:

- **Cheese moon:** a cheese crescent with holes. It's the header logo and the favicon. Small sizes use fewer, bigger holes: two at 32px, one at 16px.
- **Seal:** a ring with "NIGHT CHEESE LABS · EST. 2026" around the cheese moon. It's used in the home hero, the footer and the link preview. Don't show it smaller than about 48px, or the ring text stops being readable.

To change them, edit `_tools/build_marks.py` and run `python3 _tools/build_marks.py`. It needs Google Chrome for the PNGs. The pages inline the same SVG markup, so paste any change into the header, hero and footer too.

## Preview locally

```bash
python3 -m http.server 8000
```

Then open http://localhost:8000. Links use root paths (`/style.css`), so open the site through a server, not as `file://`.

## Deploy

The site deploys from the `main` branch root via GitHub Pages.

1. Push to `main`. Pages rebuilds in a minute or two.
2. First-time setup: repo **Settings → Pages**. Set **Source** to "Deploy from a branch", branch `main`, folder `/ (root)`. Set **Custom domain** to `nightcheeselabs.co` (the `CNAME` file sets this too).
3. Once the certificate is issued, tick **Enforce HTTPS**.

## DNS

At the domain registrar, for `nightcheeselabs.co`:

| Type | Host | Value |
| --- | --- | --- |
| A | `@` | `185.199.108.153` |
| A | `@` | `185.199.109.153` |
| A | `@` | `185.199.110.153` |
| A | `@` | `185.199.111.153` |
| CNAME | `www` | `samalamb.github.io` |

Remove any other A, AAAA or CNAME records on `@` and `www` (for example a registrar parking page). DNS can take up to a day to spread. Check with:

```bash
dig nightcheeselabs.co +short
```

GitHub's guide: https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site
