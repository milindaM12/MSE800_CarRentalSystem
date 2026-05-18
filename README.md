# Car Rental System — README

**Version:** 1.1.0  
**Developer:** Yasas Milinda Manamperi  
**Course:** MSE800 Professional Software Engineering  
**Institution:** Yoobee College of Creative Innovation  

---

## Table of Contents

1. [Overview](#overview)
2. [Features](#features)
3. [Innovative Feature — Loyalty Points System](#innovative-feature)
4. [File Structure](#file-structure)
5. [Installation & Configuration](#installation--configuration)
6. [How to Run](#how-to-run)
7. [User Guide](#user-guide)
8. [Known Issues](#known-issues)
9. [License](#license)
10. [Credits](#credits)

---

## Overview

The Car Rental System is a command-line application built in Python 3 that automates the rental process for a car rental company. It replaces manual paperwork with a digital system supporting two user roles: **Admin** and **Customer**.

The system uses object-oriented programming principles (inheritance, encapsulation, polymorphism, abstraction), a SQLite database for persistence, and a layered architecture (Model → Service → UI).

---

## Features

### User Management
- Register a new account as `admin` or `customer`
- Login with username and password

### Car Management (Admin)
- Add a new car to the inventory
- View all cars with details (ID, brand, model, year, mileage, price, availability)
- Update an existing car's details
- Delete a car from inventory

### Booking Management
- **Customer**: Browse available cars, book a car by specifying days and start date, view personal booking history
- **Admin**: View all bookings, approve or reject bookings (rejected bookings automatically restore car availability)

### Fee Calculation
- Total fee is calculated as `price_per_day × days`
- Validated against the car's minimum and maximum rental period

---

## Innovative Feature

### Loyalty Points System

Customers earn **10 loyalty points per approved rental day**. Points are displayed on every login and can be redeemed at booking time:

- **100 points = $5 discount**
- Redeemable in multiples of 100 points
- Discount cannot exceed the total rental fee

This feature sets the system apart from basic car rental systems by rewarding repeat customers and encouraging loyalty — directly addressing a key industry requirement for customer retention.

---

## File Structure

```
car_rental_system/
│
├── main.py                  # Entry point; CLI menu and application logic
│
├── models/                  # Domain model classes (OOP layer)
│   ├── __init__.py
│   ├── vehicle.py           # Abstract base class for all vehicles
│   ├── car.py               # Car class, extends Vehicle
│   ├── user.py              # User class (admin / customer)
│   └── booking.py           # Booking class with status management
│
├── services/                # Business logic / service layer
│   ├── __init__.py
│   ├── car_service.py       # CRUD operations for cars
│   ├── user_service.py      # Registration and login logic
│   └── booking_service.py   # Booking creation, approval, rejection
│
└── data/                    # Data access layer
    ├── __init__.py
    ├── db.py                # SQLite connection factory
    └── init_db.py           # Database schema initialisation
```

### Purpose of Each File

| File | Purpose |
|---|---|
| `main.py` | Entry point; drives the CLI menus for Admin and Customer |
| `vehicle.py` | Abstract base defining shared vehicle attributes and interface |
| `car.py` | Concrete vehicle with rental-specific logic (availability, min/max days) |
| `user.py` | Encapsulates user credentials and role |
| `booking.py` | Models a rental booking including dates and approval status |
| `car_service.py` | All car database operations (add, read, update, delete) |
| `user_service.py` | User registration and authentication |
| `booking_service.py` | Booking lifecycle management including status updates |
| `db.py` | Central SQLite connection factory (Factory pattern) |
| `init_db.py` | Creates tables on first run; idempotent |

---

## Installation & Configuration

### Prerequisites

- Python **3.10 or higher** (required for `X | None` type hint syntax)
- No external packages required — uses Python standard library only (`sqlite3`, `datetime`)

### Steps

1. **Clone or download** the project folder.
2. **Verify Python version**:
   ```bash
   python --version
   ```
3. **No configuration needed** — the SQLite database file (`car_rental.db`) is created automatically in the project root on first run.

---

## How to Run

# 1. Unzip and enter the folder (run from the project root directory)
cd CAR RENTAL SYSTEM

# 2. Create virtual environment
python -m venv venv

# 3. Activate it
venv\Scripts\activate       ← Windows
source venv/bin/activate    ← macOS/Linux

# 4. Install dependencies
pip install -r requirements.txt

# 5. Run
python main.py

---
The application will initialise the database and present the main menu.


## User Guide

### First-Time Setup

On first run, register an admin account:
```
Choice: 1 (Register)
Username: yasas
Password: 1234
Role: admin
```

Then register a customer:
```
Choice: 1 (Register)
Username: sam
Password: 1234
Role: customer
```

### Admin Workflow

1. Login as admin
2. **Add Car** → enter brand, model, year, mileage, price/day, min and max rental days
3. **View Cars** → see all inventory with IDs
4. **Update Car** → enter Car ID; press Enter to keep existing values
5. **Delete Car** → enter Car ID
6. **View Bookings** → see all pending/approved/rejected bookings
7. **Approve Booking** → enter Booking ID
8. **Reject Booking** → enter Booking ID (car becomes available again automatically)

### Customer Workflow

1. Login as customer → loyalty points balance is shown
2. **View Cars** → browse available cars and their IDs
3. **Book a Car** → enter Car ID → enter number of days → enter start date (or press Enter for today) → optionally redeem loyalty points → confirm
4. **View My Bookings** → see booking history and statuses

---

## Known Issues

- Passwords are stored in plain text. In a production system, passwords should be hashed using `bcrypt` or `argon2`.
- Car ID generation uses a sequential count; if cars are deleted, IDs may not be contiguous.
- No input validation for date format — entering an invalid date string is stored as-is.
- The loyalty points balance is recalculated from the database on each login (correct but not cached).

---

## License

This project is released for **educational purposes only** under the MIT License.

```
MIT License

Copyright (c) 2026 Yasas Milinda Manamperi

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
```

---

## Credits

**Developer:** Yasas Milinda Manamperi 
**Student ID:** 270753596  
**Programme:** Master of Software Engineering  
**Course:** MSE800 Professional Software Engineering  
**Institution:** Yoobee College of Creative Innovation  
**Submission Year:** 2026