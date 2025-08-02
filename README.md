# 🎟️ Event Management System API

A mini yet powerful Event Management REST API built using **Django** and **Django REST Framework**. This system allows you to create events, register attendees, and view paginated attendee lists with proper time management and data integrity.

---

## 📚 Table of Contents

- [Features](#features)
- [Assumptions](#assumptions)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Setup Instructions](#setup-instructions)
- [Running the Server](#running-the-server)
- [API Endpoints](#api-endpoints)
- [Sample cURL Requests](#sample-curl-requests)
- [Running Tests](#running-tests)
- [Swagger Documentation](#swagger-documentation)
- [License](#license)

---

## ✅ Features

- Create and list events with date, time, and capacity.
- Register attendees for a specific event.
- Enforce unique constraint on events using name, location, and times.
- Paginated attendee listing per event.
- Timezone-aware datetime storage and response.
- Auto-generated Swagger documentation via drf_yasg.

---

## 🧠 Assumptions

- Events are unique by combination of `(name, location, start_time, end_time)`.
- `start_time` and `end_time` are provided in ISO format and treated as UTC.
- No authentication is currently enforced (public API).
- Pagination is enabled with default page size.
- SQLite is used in development, but easily extendable.

---

## 🛠 Tech Stack

- Python 3.10+
- Django 4.x
- Django REST Framework
- drf-yasg (Swagger/OpenAPI)
- SQLite (for development)

---

## More Detail in this Doc: 
https://docs.google.com/document/d/1Fh13BW2jwjmDpGz63-CFknZ9lPraPIV3Zs2AdxNysmY/edit?tab=t.0
