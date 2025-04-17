# 🚀 Habitly – Track Your Habits, One Day at a Time

Habitly is a clean and scalable habit-tracking API built with **FastAPI**, **SQLAlchemy**, and **PostgreSQL**. It allows users to register, log in, and manage their daily habits with simple, token-secured endpoints — including a **streak tracking system** to boost motivation.

---

## 🔧 Features

- 🧑‍💻 User Registration & Login (JWT-based authentication)
- ✅ Create, track, and update daily habits
- 📅 Log daily habit completion
- 🔥 **Habit Streak Tracking** – daily, weekly, and monthly streaks
- 🧠 Modular architecture using FastAPI routers
- 🗃️ Alembic for database migrations
- 🐘 PostgreSQL integration
- 🌐 CORS support (configured for local dev)

---

## 🧠 How Streaks Work

Every time a user logs a habit:
- ✅ If completed the previous day, the **daily streak** increases by 1.
- 📆 If the habit was completed every day in a calendar week, the **weekly streak** increases.
- 🗓️ If completed across all weeks in a month, the **monthly streak** increases.
- 🟥 Miss a day/week/month? The corresponding streak resets.

Track consistency over time and build long-term discipline! 🔥

---
