# 🧘‍♀️ Fitness Studio Booking API

This is a simple Django REST API for a fictional fitness studio. It allows users to view available classes, book spots, and view their bookings by email. Timezone-aware datetime handling is also included.

---

## 📦 Features

- View upcoming classes
- Book a spot in a class
- See your own bookings
- Timezone management (switch timezones without altering time)

---

## 🚀 Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/fitness-booking-api.git
cd fitness-booking-api

python -m venv venv
source venv/bin/activate  # on Windows: venv\Scripts\activate

pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py seed
python manage.py runserver

python manage.py test

### 1. postman link

https://api-team-2891.postman.co/workspace/api-team-Workspace~359a76be-19b7-4be6-86c3-ce4feb78a0b1/collection/32061364-70d03f1a-d29b-422b-a882-20dde17bdf49?action=share&source=copy-link&creator=32061364

One by One 

Booked details list 
http://127.0.0.1:8000/api/home/home/bookings-listing/

Fitness Class details list 
http://127.0.0.1:8000/api/home/home/list-classes/?search_param=hiit

booking process
http://127.0.0.1:8000/api/home/home/booking-process/
sample data

{
  "class_id": 2,
  "client_name": "babu",
  "client_email": "babu@gmail.com"
}

time zone change api 
http://127.0.0.1:8000/api/home/home/switch-timezone/
sample data

{
  "timezone": "America/New_York"
}



