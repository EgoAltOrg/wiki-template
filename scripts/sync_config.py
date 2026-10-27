#!/usr/bin/env python3
"""
Per-wiki sync configuration. THIS is the only file each wiki created from the
template edits to wire up its own pages; sync-from-ontos.py is the shared
engine and stays untouched.

Fill in the six things below for your wiki:

  ONTOS_SETTING       where this wiki's source pages live in the Ontos vault
  TITLES              source filename -> published display title
  PAGE_MAP            source filename -> destination path under content/
  RENAMES             forever-redirects for pages that have moved (optional)
  NOT_YET_PUBLIC      source pages held back (all gm-only, nothing to publish)
  CONTENT_ONLY        pages hand-maintained in content/, never synced
  INFOBOX_KIND_FIELDS the typed-infobox schema for this wiki's page kinds

Everything here is plain Python data, so keep the comments that explain a
decision next to it. The shared engine reads these names; do not rename them.

This file sits in scripts/ by default. If its tables or comments would name
secrets (a held-back page, why a link is withheld), keep it and the two
allowlist JSONs outside the public repo, and run every script with
WIKI_CONFIG_DIR set to that folder.
"""
import os
from pathlib import Path

# Where this wiki's player-facing source pages live in the Ontos vault.
# Override at run time with WIKI_ONTOS_SETTING_DIR (used to preview a branch
# worktree before it merges). Point the default at your wiki's setting/ folder.
ONTOS_SETTING = Path(
    os.environ.get(
        "WIKI_ONTOS_SETTING_DIR",
        str(Path.home() / "Desktop/Ontos/Projects/CHANGE-ME/setting"),
    )
)

# Display title per source page. Explicit (not derived from the filename) so it
# always matches your own naming exactly, including casing and punctuation.
# Example: "the-rekindling.md": "The Rekindling",
TITLES = {
    "index.md": "Home",
}

# source filename (in ONTOS_SETTING) -> destination path (relative to content/).
# A page absent here is never synced (it is either NOT_YET_PUBLIC, CONTENT_ONLY,
# or simply not part of this wiki). Use folders that match your content/ layout.
# Example: "the-rekindling.md": "world/the-rekindling.md",
PAGE_MAP = {
    "index.md": "index.md",
}

# Old-URL -> forever-redirect table, keyed by CURRENT destination (the PAGE_MAP
# value); values are the old destination slugs (root-relative, no leading slash,
# no .md). Append when a page moves, never remove: readers' bookmarks don't
# expire. Also used by the engine to carry an image:/marker: block across a
# rename. Leave empty until a page actually moves.
RENAMES = {}

# Source pages that exist in Ontos but produce no public page: everything on
# them is wrapped [!gm-only]/[!gm-notes], so nothing survives the strip. Listed
# here so a skip is a visible decision, not a silent gap. To publish one, unwrap
# its gm-only material in the source and add it to PAGE_MAP + TITLES.
NOT_YET_PUBLIC = set()

# Pages hand-maintained directly in content/ and DELIBERATELY never synced:
# interactive pages whose embedded HTML/JS the sync would strip or mangle (the
# Leaflet map is the standard one). Edited in content/ directly (the rule-26
# exception that content/changelog.md also relies on).
CONTENT_ONLY = {
    "map.md",
}

# Extra wikilink rewrites for CONTENT_ONLY stub targets. BILINGUAL WIKIS ONLY;
# leave empty for a monolingual wiki. PAGE_MAP already tells the engine every
# synced page's source-basename -> slug, and it rewrites `[[gazetteer.en]]` ->
# `[[gazetteer]]` from that automatically. But a content-only page (the Leaflet
# map) has no PAGE_MAP entry, so the engine can't know its slug. If your source
# pages link it by a local .en/.pt convention (`[[map.en]]`) so the link resolves
# against a vault pointer stub, map those basenames to the published slug here.
# Keyed by source basename, value is the content/ slug (no .md). Example:
#   LINK_REWRITE = {"map.en": "map", "map.pt": "pt/map"}
LINK_REWRITE = {}

# Optional knobs, read only when present. Leave them out until your wiki needs
# one.
#
# PORTRAIT_DIR: a folder of portrait images. A brand-new page whose source opens
# with a portrait embed (`![[name.jpg|320]]`) publishes with `image: name.jpg`,
# and the file is copied into content/assets/. Without it, images are placed by
# hand.
#   PORTRAIT_DIR = ONTOS_SETTING.parent / "raw" / "character-art"
#
# EXTRA_TITLE_FORMS: extra surface forms check-related-pages-grounding.py also
# flags for a secret title, keyed by the lowercased title. Only for a word
# archaic enough never to turn up in public prose by accident.
#   EXTRA_TITLE_FORMS = {"the threnodies": ["threnody"]}
#
# COMMON_NOUN_SLUGS: pages whose title is an ordinary common noun ("elves"), so
# check-title-casing.py lets a mid-sentence link to them stay lowercase.
#   COMMON_NOUN_SLUGS = {"elves"}

# The public-fields contract for the typed infobox: the ONLY frontmatter keys,
# besides `title:` and the carried-forward marker:/submap:/image: blocks, that
# may pass from the source through to the published site. Keys pass only for the
# page's own declared `kind:` (no kind, nothing passes), so any field not listed
# here is private by default. Kept in step with quartz/components/Infobox.tsx and
# scripts/check-infobox-fields.py. This ships as a genre-generic default; retune
# the field lists (and add/remove kinds) for your wiki.
INFOBOX_KIND_FIELDS = {
    "person": ("role", "ancestry", "culture", "pronouns", "house", "nation", "allegiance", "born", "died"),
    "nation": ("capital", "ruler", "government", "founded"),
    "location": ("category", "nation", "region", "ruler", "population", "faith"),
    "organization": ("category", "leader", "seat", "region", "allegiance", "office", "heir", "words", "relic", "founded"),
    "magic-system": ("source", "practitioners"),
    "being": ("nature", "domain", "fate"),
    "artifact": ("category", "origin", "wielder"),
    "event": ("category", "when", "place", "parties", "commanders", "strength", "casualties", "outcome", "part-of"),
    "ancestry": ("homeland", "standing"),
}
