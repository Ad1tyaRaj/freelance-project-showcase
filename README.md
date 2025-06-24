# 💼 Freelance Web App Showcase

This repository presents a collection of **freelance-style demo web applications**, built to simulate real-world client projects. Each application demonstrates the use of modern web technologies and follows **RESTful API architecture**, combining clean frontend UI with robust backend logic.

> These projects showcase practical use-cases like e-commerce, reward systems, dashboard analytics, and productivity tools — perfect for portfolio or freelance demonstration.

---

## 🧑‍💻 Maintained by
**Aditya Raj**  
🔗 GitHub: [@Ad1tyaRaj](https://github.com/Ad1tyaRaj)  
🌐 Portfolio: [ad1tyaraj.github.io/Portfolio](https://ad1tyaraj.github.io/Portfolio)

---

## 📁 Project Overview

| Project | Description | Tech Stack | REST API |
|--------|-------------|------------|----------|
| [Android Rewards App](./Android_rewards_) | Digital reward system with QR scanning and reward redemption | Django, DRF | ✅ |
| [Ecommerce Web App](./Ecommerce%20Project) | Product catalog, cart, and order simulation | Django, DRF, JS | ✅ |
| [Notes App](./Notes-app) | Lightweight note manager with CRUD functionality | django, django-RESTful | ✅ |
| [Social Media Dashboard](./Social%20Media%20Dashboard) | Admin dashboard with API data charts | Django, DRF, Chart.js | ✅ |

---

## 🚀 Technologies Used

- **Backend**: Django, Django REST Framework, Flask, Flask-RESTful
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla), Chart.js, Bootstrap
- **Databases**: SQLite
- **API Tools**: Django REST Framework, Flask APIs
- **Version Control**: Git & GitHub

---

## 🔍 Detailed Project Descriptions

### 📱 [Android Rewards Web App](./Android_rewards_)

A loyalty rewards platform where users can scan QR codes to redeem rewards. Built to mimic a mobile-integrated business tool.

- **Features**:
  - QR-based reward flow
  - User session management
  - Reward redemption APIs
- **Key APIs**:
  - `GET /api/rewards/`
  - `POST /api/redeem/`

---

### 🛒 [Ecommerce Web App](./Ecommerce%20Project)

A complete e-commerce simulation frontend with REST-driven backend. Users can browse products, add items to cart, and simulate checkout.

- **Features**:
  - Product list, cart, and order summary
  - RESTful interaction between frontend and backend
- **Key APIs**:
  - `GET /api/products/`
  - `POST /api/cart/add/`
  - `POST /api/order/`

---

### 🗒️ [Notes App](./Notes-app)

A responsive web notes manager with full CRUD operations via Flask REST API. Simple and effective tool to demonstrate user data interaction.

- **Features**:
  - Add / Delete / Update notes
- **Key APIs**:
  - `GET /api/notes/`
  - `POST /api/notes/`
  - `DELETE /api/notes/<id>/`

---

### 📊 [Social Media Dashboard](./Social%20Media%20Dashboard)

An admin-style dashboard that fetches real-time data through REST APIs and displays analytics using Chart.js.

- **Features**:
  - Dynamic data visualization
  - Responsive analytics cards
- **Key APIs**:
  - `GET /api/analytics/facebook/`
  - `GET /api/analytics/twitter/`
  - `GET /api/analytics/instagram/`

---

## 🧪 Running the Projects

Sure, Adi! Here's a **professional and reusable `Setup Instructions` section** you can add to each individual project’s `README.md` — especially since all your projects are **web apps with REST APIs** using Django or Flask.

You can tweak it slightly per project based on its framework. I’ll give you two templates: one for **Django + DRF**, and one for **Flask + Flask-RESTful**.

---

## ✅ Setup Instructions (for Django + Django REST Framework)


## ⚙️ Setup Instructions

Follow the steps below to set up and run the project locally.

### 1. Clone the Repository
```bash
git clone https://github.com/Ad1tyaRaj/freelance-project-showcase.git
cd freelance-project-showcase/<project-folder-name>
````

### 2. Create and Activate Virtual Environment

```bash
# For Windows
python -m venv venv
venv\Scripts\activate

# For macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Apply Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Run the Development Server

```bash
python manage.py runserver
```

### 6. API Endpoints

Visit `http://127.0.0.1:8000/api/` in your browser or use Postman to test endpoints.

````
---

## 📄 License

This repository is licensed under the [MIT License](LICENSE).

---

## 📬 Contact

If you'd like to discuss freelance opportunities, collaborations, or backend/frontend work:

- 📧 Email: `code.adityaraj@gmail.com`
- 💻 GitHub: [@Ad1tyaRaj](https://github.com/Ad1tyaRaj)
- 🌐 Portfolio: [ad1tyaraj.github.io/Portfolio](https://ad1tyaraj.github.io/Portfolio)

---

> ⭐ Don't forget to star the repo if you find this useful or want to bookmark it for reference!
