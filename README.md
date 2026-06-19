# Frappe Docs

A **collaborative document editor** built as a Frappe v16 app. Create, edit, share, and comment on rich-text documents — all stored in Frappe's MariaDB database, accessible from the Frappe desk at `/desk/gdocs`.

---

## Features

| Feature | Details |
|---|---|
| **Rich Text Editor** | TipTap v3 with 30+ formatting options |
| **Document Outline** | Live left sidebar showing heading tree with collapse/expand |
| **Comments Panel** | Persistent right panel with threaded comments and replies |
| **5 Templates** | Blank, Meeting Notes, Project Plan, Resume, Letter |
| **Auto-Save** | Debounced 800 ms — saves to Frappe DB on every keystroke |
| **Per-User Sharing** | Share with any Frappe user at Edit / Comment / View level |
| **Permission Modes** | Edit / Comment / View — per document default |
| **Document Actions** | Duplicate, Download (.txt), Delete |
| **Search & Sort** | Search by title, sort by modified / created / A–Z |

---

## Layout

```
┌─────────────────────────────────────────────────────────────────┐
│  DocHeader: title · save status · Share button · permission     │
├─────────────────────────────────────────────────────────────────┤
│  Toolbar: undo · heading · font · bold · colors · align · lists │
├───────────────┬────────────────────────────┬────────────────────┤
│               │                            │                    │
│  DocOutline   │     White paper editor     │  All Comments      │
│  (220px)      │     (816px, centred)       │  panel (300px)     │
│               │                            │                    │
│  H1 chapters  │   EditorContent (TipTap)   │  Comment cards     │
│  ↳ H2 parts   │                            │  with replies      │
│               │                            │                    │
├───────────────┴────────────────────────────┴────────────────────┤
│  Status bar: Outline toggle · word/char count · Comments toggle │
└─────────────────────────────────────────────────────────────────┘
```

---

## Tech Stack

```
Frontend  : Vue 3 (Composition API)  +  TipTap v3  +  Heroicons  +  Vite (IIFE build)
Backend   : Frappe v16  +  MariaDB  +  Python whitelisted API
Build     : vite-plugin-css-injected-by-js (CSS bundled into JS — no separate .css file)
Styling   : Scoped Vue styles  +  global ProseMirror overrides
```

---

## Installation

### Prerequisites
- Frappe v16 bench (`bench` command available)
- Node.js ≥ 18, npm ≥ 9

### 1. Install the Frappe app

```bash
# From your bench directory
bench get-app frappe_docs /path/to/frappe_docs
bench --site <your-site> install-app frappe_docs
bench --site <your-site> migrate
```

### 2. Build the Vue frontend

The Vue source lives in a separate project (e.g. `~/products/frappe-docs-vue`). The Vite config outputs directly into `frappe_docs/public/`.

```bash
cd ~/products/frappe-docs-vue
npm install
npm run build
# Output: frappe_docs/public/js/gdocs.js  (~638 KB, CSS injected inside)
```

### 3. Build Frappe assets

```bash
# From bench root
bench build --app frappe_docs
```

### 4. Access

Navigate to `http://<your-site>/desk#gdocs`

---

## Project Structure

```
frappe_docs/
├── frappe_docs/
│   ├── doctype/
│   │   └── gdoc/
│   │       ├── gdoc.json          # Fields: title, permission_mode, content,
│   │       │                      #         comments_json, shared_with
│   │       └── gdoc.py
│   ├── page/
│   │   └── gdocs/
│   │       ├── gdocs.html         # Empty shell — Vue mounts here
│   │       ├── gdocs.js           # Frappe page loader: injects Vue IIFE bundle
│   │       └── gdocs.json         # Page title: "Frappe Docs", roles: All
│   ├── api.py                     # All @frappe.whitelist() API methods
│   └── public/
│       └── js/
│           └── gdocs.js           # Built IIFE bundle (CSS injected)
└── hooks.py
```

### Vue source structure

```
src/
├── main.js                    # Mounts Vue to #gdocs-app
├── style.css                  # Global ProseMirror + base styles
├── App.vue                    # Root: home view ↔ document view switcher
├── stores/
│   └── documents.js           # All frappe.call() API wrappers + store
└── components/
    ├── HomeView.vue            # Template gallery + recent documents grid
    ├── DocHeader.vue           # Sticky header: title, save chip, Share button
    ├── Toolbar.vue             # TipTap formatting toolbar (30+ options)
    ├── Editor.vue              # 3-column layout: outline | paper | comments
    ├── DocOutline.vue          # Left sidebar: live heading tree with expand/collapse
    ├── CommentsPanel.vue       # Right panel: comment cards, replies, actions
    ├── ShareModal.vue          # Share dialog: user search, mode picker, people list
    └── Sidebar.vue             # Document list drawer
```

---

## API Endpoints

All functions in `api.py` are decorated with `@frappe.whitelist()` and called via `frappe.call()` (CSRF-safe).

| Method | Arguments | Permission required |
|---|---|---|
| `get_all_docs` | — | Authenticated user |
| `get_doc` | `name` | Owner, or shared |
| `create_doc` | `title` | Authenticated user |
| `save_doc` | `name, title, content, permission_mode` | Owner or edit |
| `save_comments` | `name, comments` | Owner, edit, or comment |
| `delete_doc` | `name` | Owner only |
| `share_doc` | `name, user, mode` | Owner only |
| `unshare_doc` | `name, user` | Owner only |
| `search_users` | `query` | Authenticated user |

---

## GDoc DocType Fields

| Field | Type | Purpose |
|---|---|---|
| `title` | Data (required) | Document title |
| `permission_mode` | Select | Default access: `edit` / `comment` / `view` |
| `content` | Long Text | HTML from TipTap editor |
| `comments_json` | Long Text | JSON array of comment thread objects |
| `shared_with` | Long Text | JSON array of `{user, mode, full_name}` |

---

## Permission Model

```
owner     → full read + write + share + delete
edit      → read + write content (no share, no delete)
comment   → read + add comments (no content edit)
view      → read only
```

- `owner` is determined by the Frappe `owner` field (set on creation) or `Administrator`.
- `shared_with` stores per-user access levels as a JSON array.
- `get_all_docs` only returns documents the current user owns or is shared on.
- `Administrator` always has owner-level access on all documents.

---

## Document Templates

Templates are defined in `HomeView.vue` and save content to Frappe **before** opening the editor — so the server always has the correct HTML.

| Template | Description |
|---|---|
| Blank | Empty document |
| Meeting Notes | Date, Attendees, Agenda, Discussion, Decisions, Action Items |
| Project Plan | Overview, Objectives, Milestones, Resources, Risks |
| Resume | Summary, Experience, Education, Skills |
| Letter | Auto-date, Recipient, Body, Closing |

---

## Build Notes

### Why IIFE format?
Frappe's desk environment freezes JS objects. Bundling as ES modules causes `TypeError: Class constructor cannot be invoked without 'new'` due to Vue's Proxy-based reactivity conflicting with Frappe's global scope. IIFE format creates a self-contained closure that avoids this conflict entirely.

### Why CSS is injected by JS?
Vue scoped style selectors include a `data-v-HASH` attribute derived from component content. If the browser caches an old CSS file while loading new JS (different builds), hashes diverge and all scoped styles break silently. `vite-plugin-css-injected-by-js` bundles CSS inside the JS IIFE so they are always in sync.

### Why `frappe.call()` instead of `fetch()`?
`frappe.call()` automatically handles CSRF token injection, session cookie authentication, and Frappe's standard `{message: ...}` response envelope.

---

## Test Documents (in DB)

Created by automated UI testing — visible at `/desk#gdocs`:

| Title | Permission |
|---|---|
| TEST — Resume (Jane Doe) | view |
| TEST — Q3 Product Roadmap | comment |
| TEST — Business Proposal Letter | edit |
| TEST — GDocs Feature Notes | edit |
| TEST — Sprint Planning Meeting | edit |

---

## Developer

**Vengadesh M.** · [m.vengadesh2019@gmail.com](mailto:m.vengadesh2019@gmail.com) · Makeown
