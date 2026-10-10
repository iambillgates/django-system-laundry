# Laundry Service Application Documentation

## Overview
This is a Django-based web application for a laundry service that allows customers to place laundry orders, track their orders, and enables staff to manage orders through an admin dashboard.

## Features
- **Order Placement:** Customers can fill out a form to place laundry orders specifying details like laundry type, estimated weight, pickup date/time, and payment method.
- **Order Tracking:** Customers can track the status of their laundry orders using a unique electronic invoice number.
- **Staff Authentication:** Staff members can log in to access the dashboard.
- **Dashboard:** Staff can view all orders, search by invoice number, update order status, and delete orders.
- **Admin Interface:** Integration with Django admin for managing laundry orders.
- **Payment Tracking:** Basic payment method selection and payment status tracking (manual updates).

## Architecture
- **Django Project:** `laundry_project` contains project-level settings, URL routing, and WSGI/ASGI configurations.
- **Django App:** `laundry_app` contains the core application logic including:
  - `models.py`: Defines the `LaundryOrder` model with fields for customer info, laundry details, payment, and status.
  - `views.py`: Handles HTTP requests for order placement, tracking, staff login/logout, and dashboard operations.
  - `forms.py`: Defines forms for order placement and tracking with validation.
  - `urls.py`: Maps URLs to views.
  - `templates/laundry_app/`: Contains HTML templates for frontend pages.
  - `admin.py`: Configures Django admin interface for laundry orders.
  - `migrations/`: Database schema migrations.
- **Database:** SQLite3 used for data storage (`db.sqlite3`).

## Technologies and Tools
- **Backend:** Python, Django 5.2
- **Frontend:** Django Templates, HTML, Tailwind CSS (via CDN), Font Awesome, Phosphor Icons
- **Database:** SQLite3
- **Testing:** No automated tests currently implemented; input validation via Django forms.

## Running the Application Locally

### Prerequisites
- Python 3.x installed
- Virtual environment (recommended)

### Setup Steps
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd laundry-management-system-main
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install django
   ```

4. Apply database migrations:
   ```bash
   python manage.py migrate
   ```

5. Create a superuser for admin access:
   ```bash
   python manage.py createsuperuser
   ```

6. Run the development server:
   ```bash
   python manage.py runserver
   ```

7. Access the application:
   - Open your browser and go to `http://localhost:8000/` for the customer-facing site.
   - Access the admin dashboard at `http://localhost:8000/admin/`.

## Detailed Explanations from Previous Questions

### Laundry Order Process Flow
- User fills the laundry order form (`LaundryOrderForm` in `forms.py`) on the home page.
- On form submission, the `home` view (`views.py`) validates the form, calculates estimated cost based on laundry type and weight, and saves the order.
- The `LaundryOrder` model (`models.py`) generates a unique electronic invoice number on save.
- The order data is stored in the SQLite database.
- The user receives a success message with their invoice number.

### Main User Interface Components
- Built using Django templates with Tailwind CSS for styling.
- Includes navbar, hero section, services section, reservation form, tracking form, and footer.
- Forms are rendered using Django form fields with Tailwind CSS classes.
- Data is sent from frontend to backend via HTTP POST requests with CSRF protection.
- Minimal JavaScript is used for UI interactions like mobile menu toggling.

### Payment Feature
- Payment method and status are stored as fields in the `LaundryOrder` model.
- Users select payment method in the order form.
- Payment status defaults to 'pending' and can be updated manually by staff.
- No external payment gateway or automated payment validation is integrated.
- Payment data flows from client form submission to backend model storage.

### Testing and Validation
- No unit tests or automated tests are currently implemented (`tests.py` is empty).
- Input validation is handled by Django forms (`LaundryOrderForm` and `TrackOrderForm`).
- Forms validate and sanitize user inputs on the server side, providing error messages on invalid data.
- Adding automated tests is recommended for production readiness.
