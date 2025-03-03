## 📌 **1. `users/` → Authentication & User Management**

Handles everything related to user accounts, authentication, and profile management.

### 📂 **Contains:**

- **`models.py`** → Defines:
  - `User` (Extends Django’s User Model, supports Buyer/Seller/Admin)
  - `Address` (Shipping details for orders)
- **`views.py`** → Handles:
  - User registration (Sign Up)
  - Login / Logout (Token-based)
  - Profile management (Update info, change password)
- **`serializers.py`** → Converts user data for API responses
- **`urls.py`** → Defines API endpoints:
  - `/users/signup/`
  - `/users/login/`
  - `/users/profile/`
- **`admin.py`** → Allows admin to manage users in Django Admin

---

## 📌 **2. `inventory/` → Product & Order Management**

Manages product listings, categories, and order processing.

### 📂 **Contains:**

- **`models.py`** → Defines:
  - `Product` (Title, Description, Price, Seller)
  - `Category` (Hierarchical structure for product categorization)
  - `Order` (Tracks purchases and order status)
- **`views.py`** → Handles:
  - CRUD operations for products (Create, Update, Delete)
  - Order placement & tracking
  - Seller dashboard
- **`serializers.py`** → Converts product & order data for API responses
- **`urls.py`** → Defines API endpoints:
  - `/inventory/products/`
  - `/inventory/orders/{id}/`
- **Admin Role** → Approves product listings

---

## 📌 **3. `cart/` → Cart, Checkout & Payment**

Handles cart functionality, checkout process, and secure payments.

### 📂 **Contains:**

- **`models.py`** → Defines:
  - `Cart` (Stores selected products for a user)
  - `CartItem` (Product, Quantity, Cart reference)
  - `Payment` (Stores payment transactions)
- **`views.py`** → Handles:
  - Add/remove/update products in the cart
  - Checkout process (Order confirmation)
  - Secure online payments
- **`serializers.py`** → Converts cart & payment data for API responses
- **`urls.py`** → Defines API endpoints:
  - `/cart/` (View cart contents)
  - `/cart/checkout/` (Proceed to payment)
  - `/cart/payment/confirm/` (Confirm payment)
- **Payment Gateway** → Supports integrations like PayPal, Stripe, etc.

---

## 📌 **4. `invoices/` → PDF Invoice & Order History**

Handles automatic invoice generation and order tracking.

### 📂 **Contains:**

- **`models.py`** → Defines:
  - `Invoice` (Linked to `Order`, stores PDF file)
- **`views.py`** → Handles:
  - Generate invoices upon order completion
  - Allow users to download invoices
- **`serializers.py`** → Converts invoice data for API responses
- **`urls.py`** → Defines API endpoints:
  - `/invoices/{order_id}/download/` (Download invoice as PDF)

---

## ✅ **Why This Structure?**

- **Modular**: Each app handles a specific part of the eCommerce system.
- **Collaborative**: Each team member can focus on a separate app.
- **Scalable**: New features like reviews, bidding, and promotions can be added easily.

🚀 **Ready to start coding? Let me know if you need model templates!**
