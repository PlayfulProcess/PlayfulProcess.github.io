# Making the home more like a Ghost site

October 2026. A note for deciding, not a plan already under way. No accounts were opened.

## What "a Ghost website" means in practice

A Ghost site is a publication. Its parts:

| Ghost part | What a reader sees |
| --- | --- |
| Posts with a date, tags, a cover and an excerpt | A feed of writing, newest first |
| Tag pages and an archive | "Everything on tarot", "everything from 2026" |
| RSS | Feed readers and other sites can follow |
| Members and newsletter | An email box on every page; each post can go out as an email |
| Per-post social cards | A link to a post shows its own picture and title on Substack, Bluesky, WhatsApp |
| Search, and comments for members | Optional |
| Paid tiers (Stripe) | Optional |
| A theme and an editor | The look, and a writing screen in the browser |

The home today is one hand-made page of links (`index.html`) with no build step. It already
has the Ghost look in spirit: a header, streams, cards with pictures, a footer. What it lacks
is **posts**: pages with dates that pile up over time.

## Route A: Ghost-like on GitHub Pages (static)

Everything above except members, paid tiers and the browser editor can be done with files.

1. **Posts as Markdown.** One file per post in `posts/`, with a short header:
   `title`, `date`, `tags`, `cover`, `excerpt`. You write in any editor (or Claude drafts and
   you edit).
2. **A small generator**, `tools/build.py` (Python, no packages beyond Markdown), that turns
   `posts/*.md` into:
   - `posts/<slug>/index.html` in the home's header, footer and lilac reading layout;
   - `writing/index.html`, the archive by year;
   - `tag/<tag>/index.html`, one page per tag;
   - `feed.xml` (RSS) and `sitemap.xml`;
   - a "Latest" row of three cards on the home, between the intro and the streams.
   The generated pages are committed, the same way the sibling repos commit what their
   generators make, so the GitHub Pages settings stay as they are (served from a branch,
   no Actions deploy to set up).
3. **Why not Jekyll**, which GitHub Pages builds for free? The repo carries `.nojekyll` on
   purpose: with Jekyll on, files and folders starting with `_` stop being served, and that
   has bitten two of your Pages repos before. A small generator avoids turning it back on.
4. **Email sign-up.** Two ways, neither needs a new account today:
   - **Your Substack's own sign-up box** (Substack offers an embed for it). Life Is Process
     stays the newsletter; the home links each post to its Substack edition, or the other way
     round. This is the lightest step.
   - **Buttondown** (or a similar service), if you want the list on your own domain and the
     option of sending a post as an email from its RSS. It has a free tier for a small list;
     check current limits and which tier includes RSS-to-email before choosing.
5. **Per-post social cards.** The generator gives each post an `og:image`: its cover if it
   has one, otherwise a lilac card with the title and the double spiral (made the same way as
   `img/og-card.png`).
6. **Optional later:** search with Pagefind (a static index built alongside the pages),
   comments through Giscus (GitHub Discussions), a custom domain.

What Route A does not give: paid members, a writing screen in the browser, analytics beyond
what GitHub offers. Substack already covers the first two for you.

## Route B: running Ghost itself

**Ghost(Pro), hosted by Ghost.** About $18 a month at the entry tier as of this writing
(check the current price: Ghost has changed its tiers more than once). Nothing to maintain.
The entry tier may limit custom themes and integrations, which matters if you want the
lilac look exactly. Ghost has an importer for Substack, so the Life Is Process archive could
move over.

**Self-hosted on Oracle Cloud's Always Free tier.** No monthly bill for the server, but:
a Linux machine to keep patched, Ghost and MySQL updates, backups (OneDrive does not count
as one), and an email-sending service for newsletters (Ghost uses Mailgun for bulk email,
which is a separate account and, past a small volume, a cost). Free instances can be
reclaimed when idle. This is the most work of the three and the most fragile for a solo
maintainer.

Either way Ghost wants its own domain and becomes a second place your writing lives, next to
recursive.eco and Substack.

## Recommendation

Route A, in two steps, with Substack kept as the email side:

1. Posts, archive, tags, RSS and per-post cards on this site; the Substack sign-up box in the
   footer and under each post.
2. Decide later, with a few posts up, whether the newsletter should move off Substack. If it
   should, compare Buttondown with Ghost(Pro) then; Ghost(Pro) becomes the better choice only
   if you want paid members on your own domain.

## How long

| Work | Sessions |
| --- | --- |
| Generator, post layout, archive, tag pages, RSS, sitemap | 1 |
| "Latest" row on the home, Substack sign-up, per-post social cards, the first two or three posts (you choose which) | 1 |
| Optional: search, comments, custom domain | 0.5 to 1 |
| **Route A in all** | **2 to 3** |
| Route B with Ghost(Pro): set up, a lilac theme, Substack import | 1 to 2, plus the monthly fee |
| Route B self-hosted on Oracle | 2 to 3, plus upkeep every month |

Your call on all of it, including whether to open any email account.
