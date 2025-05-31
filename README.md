# E-Commerce Website

A full-stack e-commerce platform built with Django and Next.js, featuring multiple auction types and comprehensive e-commerce functionality.

## Features

- **Multiple Auction Types**
  - English Auctions
  - Sealed Auctions
  - Combinatorial Auctions
- **User Management**
  - Authentication and Authorization
  - User Profiles
- **Shopping Features**
  - Shopping Cart
  - Inventory Management
  - Payment Processing (Stripe & Edahabia)
  - Shipment Tracking
- **Modern Frontend**
  - Built with Next.js
  - Responsive Design
  - TypeScript Support

## Tech Stack

### Backend
- Django 4.2.2
- Django REST Framework
- SQLite Database
- Redis for caching
- JWT Authentication
- Payment Integration
  - Stripe
  - Edahabia

### Frontend
- Next.js
- TypeScript
- Tailwind CSS
- Context API for state management

## Prerequisites

- Python 3.x
- Node.js
- Redis
- Virtual Environment (recommended)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd e-commerce-website
```

2. Set up the backend:
```bash
cd ecommerce
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Set up the frontend:
```bash
cd frontend
npm install
```

4. Configure environment variables:
   - Create `.env` file in the ecommerce directory
   - Create `.env.local` file in the frontend directory
   - Add necessary environment variables (see `.example.env.local` for reference)
   - Configure Stripe and Edahabia API keys

5. Run database migrations:
```bash
cd ecommerce
python manage.py migrate
```

## Running the Application

1. Start the backend server:
```bash
cd ecommerce
python manage.py runserver
```

2. Start the frontend development server:
```bash
cd frontend
npm run dev
```

The application will be available at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000

## Project Structure

```
e-commerce-website/
├── ecommerce/              # Django backend
│   ├── users/             # User management
│   ├── inventory/         # Product management
│   ├── cart/             # Shopping cart
│   ├── payment/          # Payment processing (Stripe & Edahabia)
│   ├── shipment/         # Shipping management
│   └── Auction_*/        # Different auction types
├── frontend/              # Next.js frontend
│   ├── app/              # Pages and routing
│   ├── components/       # Reusable components
│   ├── context/         # State management
│   └── lib/             # Utility functions
└── requirements.txt      # Python dependencies
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request


