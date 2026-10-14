# 💊 Pharmacy Management System

A web-based pharmacy operations dashboard built with **Python, Flask, SQLite, and machine-learning tools**. The application brings medicine inventory, sales recording, reporting, analytics, and basic sales-demand forecasting into one interface.

> **Project status:** Educational/demo project. Review the security notes below before using it with real pharmacy operations or sensitive data.

## ✨ Features

- **User accounts** — registration, login, logout, and session-based access using Flask-Login.
- **Dashboard** — summary cards for medicine count, total stock, recorded sales, and revenue, plus top-selling medicines.
- **Medicine inventory** — add medicines with category, quantity, price, description, and usage information; view current stock.
- **Sales recording** — record a medicine sale and automatically reduce stock when sufficient quantity is available.
- **Reports** — review recorded sales and medicine information.
- **Analytics** — visualize sales by category and stock composition using Chart.js.
- **Demand forecasting** — fit a simple scikit-learn Linear Regression model to historical daily sales and estimate quantities for a selected future window.
- **Responsive interface** — shared page layout, styling, theme toggle, and form feedback.

## 🧰 Tech Stack

| Area | Technologies |
| --- | --- |
| Backend | Python, Flask |
| Authentication | Flask-Login, Werkzeug password hashing |
| Forms and validation | Flask-WTF, WTForms |
| Database / ORM | SQLite, Flask-SQLAlchemy, SQLAlchemy |
| Data processing | pandas |
| Forecasting | scikit-learn Linear Regression |
| Frontend | HTML, CSS, JavaScript, Jinja templates |
| Charts | Chart.js |

## 📸 Screenshots

No standalone application screenshots are currently stored in this repository. To keep this README accurate, screenshots have not been fabricated.

To add genuine screenshots, create a `docs/screenshots/` folder and save captures from the running application, for example:

- `docs/screenshots/login.png`
- `docs/screenshots/dashboard.png`
- `docs/screenshots/inventory.png`
- `docs/screenshots/analytics.png`
- `docs/screenshots/forecast.png`

Then embed them here using relative Markdown image paths, such as `![Dashboard](docs/screenshots/dashboard.png)`.

## 🗂️ Project Structure

```text
PHARMACY-MANAGEMENT/
├── app.py                 # Flask app, models, routes, and forecast logic
├── init_db.py             # Database initialization helper
├── requirements.txt       # Python dependencies
├── instance/
│   └── pharmacy.db        # SQLite database file currently in the repository
├── templates/
│   ├── base.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── inventory.html
│   ├── sales.html
│   ├── reports.html
│   ├── analytics.html
│   ├── forecast.html
│   └── profile.html
└── static/
    ├── css/style.css
    └── js/main.js
```

## ⚙️ Requirements

- Python 3.10 or a compatible Python version
- pip
- A modern web browser

## 🚀 Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/PreciousBharath/PHARMACY-MANAGEMENT.git
cd PHARMACY-MANAGEMENT
```

### 2. Create and activate a virtual environment

**Windows PowerShell**

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

**macOS / Linux**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Initialize the database and launch the app

```bash
python app.py
```

The application initializes its database and sample records when started directly. Then open:

```text
http://127.0.0.1:5000
```

Alternatively, initialize the database explicitly with `python init_db.py` before starting the app.

## 🧭 Main Pages

| Page | Purpose |
| --- | --- |
| Dashboard | Overview of stock, sales, revenue, and top medicines |
| Inventory | Add and view medicine records |
| Sales | Record sales and inspect recent transactions |
| Reports | Review sales and medicine records |
| Analytics | Compare category sales and stock distribution |
| Forecast | Generate a basic forecast from available sales history |
| Profile | View the current user's profile page |

## 📈 Forecasting Notes

The forecasting page groups recorded sale quantities by date, assigns an index to each date with sales, and fits a **Linear Regression** model. It then predicts values for the requested forecast window.

- At least five recorded sale entries are required by the current implementation.
- Predictions are estimates from a simple baseline model, not medical or business advice.
- Forecast quality depends on the quantity and quality of recorded sales data; it should not be treated as a reliable production demand-planning system without further validation.

## 🔐 Security and Data Notes

This repository is currently best treated as a learning/demo project, not a production pharmacy system.

- The Flask secret key is hard-coded in `app.py`. Replace it with a strong environment-provided secret before any deployment, and do not commit secrets.
- The app is started with Flask debug mode enabled. Disable debug mode in any deployed environment.
- The application seeds a demo administrator account. Change or remove default credentials before use; never rely on a published default password.
- The SQLite database file is tracked in the repository. Do not store real patient, customer, or pharmacy business data in a committed database file.
- Before production use, review authorization, CSRF protection, safe HTTP methods for destructive actions, input validation, backups, audit logging, and deployment configuration.

## 🛣️ Possible Improvements

- Add medicine expiry dates, batch numbers, supplier and purchase management.
- Add low-stock and expiry notifications.
- Add pagination, search, and filters for large inventories.
- Improve forecast evaluation with time-based validation and stronger baseline comparisons.
- Add automated tests and deployment configuration.
- Move secrets and environment-specific settings to configuration variables; remove generated files and sensitive data from version control.

## 👤 Author

**Bharath**  
GitHub: [@PreciousBharath](https://github.com/PreciousBharath)

---

If you explore the project, feedback and suggestions are welcome.
