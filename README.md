# Laundry Asaka

A Django web app for a small Indonesian laundry shop. Customers place an
order and get an **e-invoice number**, then track the order by that number
without logging in. Staff log in to a dashboard to manage orders.

> Bahasa antarmuka aplikasi: Indonesia. Harga dalam Rupiah (IDR).

## Features

**For customers (no login needed)**

- Place a laundry order: name, address, WhatsApp number, laundry type,
  estimated weight/quantity, payment method, pickup date & time.
- Get an **e-invoice number** (format `MMDDHHMMSS`, with a counter suffix
  if two orders land in the same second) right after ordering.
- **Track an order** by e-invoice number — no account required.

**For staff (`/staff/login/`, account must be `is_staff`)**

- Dashboard listing all orders, newest first.
- Search orders by e-invoice number.
- Update order status: `pending` → `approve` → `proses` → `complete`.
- Delete orders.

**For admins (`/admin/`)**

- Django admin for orders: list, filter by status / laundry type /
  pickup date, search by e-invoice number, name, or WhatsApp.

**Pricing** — an estimated cost (`biaya`) is calculated when an order is
placed: the midpoint of the service's price range × quantity. The quantity
is weight in kg for kiloan services; for the other services the form's
quantity field is treated as item count (or m² for karpet/gorden). The
estimate is only a guide — the final price is agreed with the customer.

| Service | Price range (IDR) | Per |
| --- | --- | --- |
| Daily Kiloan | 7.000 – 10.000 | kg |
| Cuci & Setrika | 10.000 – 15.000 | kg |
| Dry Cleaning | 25.000 – 50.000 | pcs |
| Green Dry Cleaning | 30.000 – 60.000 | pcs |
| Laundry Sepatu | 25.000 – 50.000 | pasang |
| Laundry Tas | 30.000 – 100.000 | pcs |
| Laundry Karpet | 15.000 – 30.000 | m² |
| Laundry Gorden | 20.000 – 40.000 | m² |
| Laundry Kulit | 50.000 – 150.000 | pcs |
| Lainnya | negotiable | — |

Payment method is recorded as online/offline and payment status
(pending/paid/unpaid) is updated manually by staff — there is no payment
gateway integration.

## Tech stack

- **Backend:** Python 3.13, Django 5.2.3, SQLite
- **Frontend:** Django templates, Tailwind CSS via CDN, Font Awesome,
  Phosphor Icons
- **Database:** SQLite (`db.sqlite3`, created locally on first migrate)

## Quick start

```bash
git clone https://github.com/iambillgates/django-system-laundry.git
cd django-system-laundry

python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

pip install -r requirements.txt

cp .env.example .env            # then fill in SECRET_KEY (required —
                                # the app refuses to start without it)

python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open http://localhost:8000/ for the customer site.

- Staff login: http://localhost:8000/staff/login/ — use a staff account
  (a superuser from `createsuperuser` works; other staff accounts need
  `is_staff` set in Django admin).
- Django admin: http://localhost:8000/admin/

## Environment variables

See `.env.example`. Only three are used:

| Variable | Meaning |
| --- | --- |
| `SECRET_KEY` | Django secret key. **Required.** Generate a fresh one with `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`. Never reuse the key that was previously committed to this repo. |
| `DEBUG` | `True`/`False`, default `False`. Set `True` only for local development. |
| `ALLOWED_HOSTS` | Comma-separated hosts, default `localhost,127.0.0.1`. |

## Project structure

```
django-system-laundry/
├── laundry_project/        # Django project: settings, URLs, WSGI/ASGI
├── laundry_app/            # The app: models, views, forms, templates
│   ├── models.py           # LaundryOrder + e-invoice generation
│   ├── views.py            # Home/order, tracking, staff dashboard
│   ├── forms.py            # Order form + tracking form
│   ├── admin.py            # Django admin config
│   └── templates/          # Tailwind templates (home, dashboard, login, ...)
├── manage.py
├── requirements.txt
├── .env.example
└── DOCUMENTATION.md        # Longer write-up: architecture, order flow, payment
```

## Notes & limitations

- **Styling needs internet:** Tailwind, Font Awesome, and Phosphor Icons
  load from CDNs, so the UI is unstyled offline.
- **No automated tests yet** (`laundry_app/tests.py` is the Django stub).
- **The price estimate is approximate** — per-item services use a single
  quantity field labelled "weight (kg)" in the form, so the estimate for
  those is for one piece/unit at the range midpoint unless the quantity
  is adjusted. A proper item-count / area field is a future improvement.
- **Do not commit your data:** `db.sqlite3` and `.env` are git-ignored.
  The database file previously committed to this repo may contain real
  customer data — it should be purged from git history (see
  `CHANGES.md`), not just deleted.

## License

MIT — see [LICENSE](LICENSE).
