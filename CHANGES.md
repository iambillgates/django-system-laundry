# Phase-1 SECURITY cleanup — django-system-laundry

Branch target: `master` (PUBLIC repo — visibility stays as-is, do NOT make private repos public; this one is already public).

Status: files prepared locally in `repo-work/django-system-laundry/`, **NOT pushed yet**. Nothing was deleted from the repo in this phase (the GitHub snapshot-push flow cannot delete tracked files).

## Files changed

### 1. `laundry_project/settings.py` (modified)
- **SECRET_KEY** — was a hardcoded `django-insecure-...` literal committed to the repo. Now `os.environ["SECRET_KEY"]` (required: Django fails loudly with `KeyError` if the variable is missing, so a deploy can never silently run with a dev key). `import os` added at the top.
- **DEBUG** — was hardcoded `True`. Now `os.environ.get("DEBUG", "False")` parsed as boolean, default **False** (safe default for production).
- **ALLOWED_HOSTS** — was a hardcoded list containing a leftover CodeSandbox preview host. Now read from a comma-separated env var, default `"localhost,127.0.0.1"`; the CodeSandbox host is removed from every default (it no longer appears anywhere in the file).
- **LANGUAGE_CODE** — `"en-us"` → `"id"` (the UI is Indonesian).
- **TIME_ZONE** — `"UTC"` → `"Asia/Jakarta"` (the shop operates in WIB).
- Everything else (INSTALLED_APPS, MIDDLEWARE, DATABASES, validators, templates, static) is byte-identical to the original.

Verified: `python3 -m py_compile` passes; `django.setup()` with Django 5.2.3 loads the settings correctly with env vars set (DEBUG=True, ALLOWED_HOSTS=['localhost','127.0.0.1'], LANGUAGE_CODE=id, TIME_ZONE=Asia/Jakarta, SECRET_KEY read from env); setup fails without SECRET_KEY, as intended.

### 2. `.env.example` (NEW, repo root)
- Documents the 3 env vars the app now needs: `SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS`, with placeholder values and comments (including how to generate a fresh secret key with `get_random_secret_key()`). Contains **no real values**.

### 3. `.gitignore` (NEW, repo root)
- Python/Django standard: `__pycache__/`, `*.py[cod]`, `db.sqlite3`, `media/`, `venv/`/`.venv/`, `.env`, `*.zip`, editor/OS files. Prevents the sensitive files below from being committed again.

## Needs akbar (cannot be done by the agent)

1. **Rotate the committed SECRET_KEY.** The old `django-insecure-...` key is in git history forever — changing `settings.py` does NOT un-expose it. Generate a new key, put it in the deployment `.env`, and treat the old key as compromised.
2. **Delete sensitive files from tracking AND purge git history** — the snapshot-push flow cannot delete tracked files, and deleting them in a new commit leaves them in history. The files:
   - `db.sqlite3` (~147 KB) — likely contains **real customer data** (names, addresses, WhatsApp numbers). Must be purged from history (e.g. `git filter-repo --path db.sqlite3 --invert-paths`) or the repo re-created; after the purge, treat the data as exposed.
   - `laundry_app.zip` (~51 KB) — redundant zip of the app, probably also containing the DB.
   - `__pycache__/` directories (several, incl. `laundry_app/__pycache__`, `laundry_project/__pycache__`, `laundry_app/migrations/__pycache__`).
   - `laundry_app/templates/laundry_app/dashboard_old.html` — dead template superseded by the current dashboard.
3. After the purge, force-push the rewritten history (coordinate: anyone with a clone must re-clone).

## Not in this phase
- README rewrite (still literally "ash"), `requirements.txt`, LICENSE, bug fixes (dashboard search, price calc, tests) — those come in the build/packaging phases.
