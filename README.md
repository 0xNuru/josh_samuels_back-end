# Josh Samuels E-commerce Platform (Backend)

## Project Overview

The **Josh Samuels E-commerce Platform** backend is a robust and scalable application that powers a seamless bespoke menswear experience. It manages everything from user authentication, product listings, dynamic shopping carts, payment processing, and virtual consultations, to bespoke garment creation. Built with modern web technologies, this backend ensures the secure and efficient handling of all business processes, integrating advanced features like automated webhook handling for payments and S3 for image storage.

## Features

### 1. **User Authentication**

- Securely authenticate users during key actions, such as checkout and wishlist management.
- Employ JWT tokens to manage sessions and protect sensitive endpoints.

### 2. **Order Management**

- Handle orders efficiently by generating unique reference numbers for each transaction.
- Integrate Paystack for payment processing and automate order status updates via webhooks.

### 3. **Product and Fabric Management**

- Manage products and associated fabrics, allowing for dynamic pricing based on product categories.
- Use categories like `2P Suit`, `3P Suit`, etc., to associate fabric prices and streamline the pricing model.

### 4. **Custom Measurements and Style Configuration**

- Allow users to input measurements and customize styles, such as lapels, buttons, and pockets, using a flexible database structure.
- Provide real-time validation to ensure accurate measurement input.

### 5. **Payment Integration with Paystack**

- Initialize transactions with Paystack, handle payment verifications, and process webhook data to update order statuses.
- Secure webhook endpoints with HMAC signature verification to ensure data integrity.

### 6. **Webhook Management**

- Implement webhooks to receive real-time payment updates from Paystack and automatically update order statuses.
- Validate and handle payment events like `charge.success` to ensure seamless transaction processing.

### 7. **Dynamic Shopping Cart**

- Manage a shopping cart that updates in real time as users add, remove, or modify items.
- Ensure data persistence across sessions, enhancing the user shopping experience.

### 8. **AWS S3 Integration for Image Storage**

- Store product and user-uploaded images securely in AWS S3.
- Generate unique file names and manage access to ensure images are stored and retrieved efficiently.

## Technologies Used

- **Python**: The main programming language used for backend development.
- **FastAPI**: A modern, fast (high-performance) web framework for building APIs with Python 3.7+.
- **SQLAlchemy**: SQL toolkit and Object-Relational Mapping (ORM) library for Python, used for database interactions.
- **PostgreSQL**: A powerful, open-source object-relational database system.
- **Pydantic**: Data validation and settings management using Python type annotations.
- **Paystack**: Payment gateway used for processing transactions.
- **Boto3**: AWS SDK for Python, used for interacting with AWS services like S3.
- **Jinja2**: Templating engine for rendering HTML templates.
- **Gunicorn**: Python WSGI HTTP Server for Unix, used to serve the FastAPI application.
- **Requests**: A simple, yet elegant, HTTP library for Python, used for making API calls to external services.
- **Itsdangerous**: Used for generating random secure tokens.
- **Passlib**: Password hashing library used for secure user authentication.
- **FastAPI-Mail**: For sending emails through SMTP.
- **Pydantic Settings**: For managing environment configuration settings.

## Installation and Setup

### Prerequisites

- Python 3.7 or higher
- PostgreSQL database
- AWS account (for S3 bucket setup)
- Paystack account for payment integration

### Environment Variables Configuration

To run the backend application, you need to set up a `.env` file in the root directory of your project. This file contains critical configuration settings for connecting to services like your database, AWS, and Paystack. Below is the format for the `.env` file:

```env
# Example Database Configuration
DB_USER="postgres"
DB_PASSWORD="josh_samuels_Password00!"
DB_NAME="josh_samuels"
DB_HOST="host"
DB_PORT=5432
DB_URL="postgresql://${DB_USER}:${DB_PASSWORD}@${DB_HOST}:${DB_PORT}/${DB_NAME}"


# Token Settings
JWT_SECRET_KEY=""  # Replace with your secret key for JWT
JWT_ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30000
REFRESH_TOKEN_EXPIRE_MINUTES=300

# Email Server Settings
EMAIL_HOST=
EMAIL_PORT=587
EMAIL_USERNAME=
EMAIL_PASSWORD=""  # Replace with your email password
EMAIL_FROM=@.tech

# AWS S3 Configuration
S3_BUCKET_NAME="josh-photos"
S3_REGION="eu-north-1"
S3_ACCESS_KEY=""
S3_SECRET_KEY=""

# Paystack Configuration
PAYSTACK_SECRET_KEY=""
```
