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

The header and footer are copied into each page. Change them in every file.

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
