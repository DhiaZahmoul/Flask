# 🍔 OmBurger Web Application

**OmBurger** is a full-stack Flask web application for a fictional burger restaurant. It includes user authentication, order tracking, email notifications, and a simple frontend interface — all built using Python, Flask, SQLite, and Flask-Mail.

---

## 📌 Features

### 🔐 Authentication
- User signup with form validation
- Secure login system with session management
- Role-independent access (default: general user)

### 🧾 Order Management
- Users can place custom orders through a form
- Orders include item quantities, payment method, and estimated delivery time
- Order data is saved in an SQLite database and tied to the logged-in user

### 📧 Email Notifications
- Welcome email on account creation
- Order confirmation email with itemized breakdown and estimated delivery time
- Email notifications sent using Flask-Mail and Gmail SMTP

### 🗃️ Database
- **SQLite** used for data persistence
- Two main tables:
  - `users`: Stores personal and login info
  - `orders`: Stores order details and links to users via foreign key
- Foreign key constraints enabled (`ON DELETE CASCADE`)

### 🌐 Frontend (SSR)
- HTML templates rendered using Jinja2
- Separate pages for:
  - Signup (`/signup`)
  - Login (`/login`)
  - Home/feedback (`/`)
  - Order summary (`/order`)
- Basic Bootstrap styling and structured forms

---

## 🛠 Technologies Used

- **Python 3**
- **Flask**
- **Flask-Mail**
- **SQLite3**
- **Jinja2** templating
- **HTML/CSS**
- **Gmail SMTP** for email delivery

---

