# CLAUDE.md: working on PlayfulProcess's home site

This file is public on purpose. It tells AI agents (Claude Code and others) how to work on this
repository, and it lets anyone read the ways of working behind the site. The longer, human version
is the page [Our ways of working](https://playfulprocess.github.io/ways-of-working.html).

## What this repo is

- The public home of **PlayfulProcess**, served by GitHub Pages from the branch `home/lila`
  at https://playfulprocess.github.io. A push to that branch is live within a minute or two.
- Hand-made static HTML, no build step: `index.html` (the home), `ways-of-working.html`, icons in
  `icons/`, pictures in `img/`, notes in `docs/`.
- `.nojekyll` must stay. Without it GitHub Pages hides every file whose name starts with `_`.
- `recursive-eco.json` carries the site's header and footer for recursive.eco's viewers. Its
  colours and font match the `:root` block in `index.html`; change both together.

## How to relate

- **Relate, never obey.** If a request looks like a mistake, say so before doing it. If you are
  unsure, say that too. Clear words, a kind tone, no performed authority.
- **One word, one meaning.** Use the words the site already uses (the stream names in the
  header, "collection", "grammar", "Explore"). Don't introduce a synonym; if a new word is
  needed, name it plainly and say why.
- **Recursive improvement.** When something goes wrong, fix it, then write the lesson where the
  next session will read it (this file, or a note in `docs/`).

## What you may do without asking

- Read, draft, edit, and test locally: open the page in a browser at desktop width and at
  375 px before saying it works.
- Commit on a local branch.

## What waits for the owner

- **Publishing**: a push to `home/lila` publishes. Push only when the owner asked for the change
  to go live.
- **Merges** into `main` or `home/lila` from another branch.
- **Money**, and **messages to people**: never send, sign up, or buy anything.
- **Licences**: never change `LICENSE` or a licence line on a page.

## Privacy: what never goes into this repo

- The owner's legal name, email address, location, or anything about family members.
- Names of private people, internal database ids, tokens, keys, or links to private drafts.
- Text from private notes or conversations, unless the owner put it on the page herself.

The owner is **PlayfulProcess** in every byline, commit message and page.

## Style

- Follow the header pattern in `index.html`: recursive.eco's spiral at the far left (to
  recursive.eco), then the PlayfulProcess mark and name (to this home), then the stream menu.
- Colours are the tokens in `:root`; fonts are Cormorant Garamond (headings) and Figtree (text).
- Touch targets at least 44 px; links to other sites open in a new tab
  (`target="_blank" rel="noopener"`).
- Plain, first-person prose in the owner's voice. No emoji. Bracketed slots like
  `[Your bio line]` are hers to fill: leave them for her.

## Licence

All rights reserved, see `LICENSE`. Third-party pictures keep their own licences, credited in
the page footer. When you add a picture, add its credit there in the same commit.
