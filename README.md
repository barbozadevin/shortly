# URL Shortener — Design Log

A URL shortener built in stages. Each version documents
what changed and why.

## v0 — 12 Sep 2026

**Goal:** POST a long URL, get a slug, hit the slug, land
on the original. Nothing else.

**Decisions**
- Slug = auto-increment id. Deliberately naive; base62 in v1.
- 302 over 301. A 301 is cached by the browser, so later
  clicks never reach the server — fast, but analytics go
  blind. 302 costs a server hit per redirect and keeps v3
  possible.
- Sync SQLAlchemy. Async adds session and driver complexity
  for no v0 benefit. Revisit at v3.

**Known limits**
- Sequential slugs are enumerable
- No cache; DB read on every redirect
- No rate limiting