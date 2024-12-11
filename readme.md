# Tutorilla

**Tutorilla** is an interactive, Telegram-based language learning platform designed to connect learners with
tutors for personalized language lessons. The platform prioritizes convenience and seamless interaction, enabling users
to book and manage lessons directly through Telegram or via a dedicated web application.

The platform is powered by 3 interconnected applications: **Telegram Bot**, **API** and **Web App**,
supported by 2 data storage systems: **Redis** and **PostgreSQL**.
These components work together to deliver a smooth, reliable user experience.

---

## System overview

The **Telegram Bot** serves as the primary interface, enabling users to communicate directly with the platform through Telegram. It connects to the
**API** for data processing and to the **Web App** for scheduling and managing lessons, ensuring real-time interaction.

The **Web App** provides an intuitive interface for users to schedule lessons, manage bookings, and view their progress.

The **API** is the backbone of the system, facilitating communication between the **Telegram Bot**, **Web App** and the database.
It handles data processing, storage operations, and integration to ensure consistent functionality across the platform.

**Redis** is used as an in-memory data store, offering access to frequently used data, improving responsiveness for both the **Telegram Bot** and the **API**.

## Technologies and Infrastructure

### CI/CD

* **GitHub Actions** for automated continuous integration and deployment pipelines
* **Docker** and **Docker Compose** for containerization
* **GitHub Container Registry (GHCR)** storage for Docker images

### Server and Deployment

* **Hetzner Cloud** for hosting
* **Debian 12** operating system
* **Nginx** for reverse proxy and load balancing
* **DNS** configuration for domain management

### Data Storage

* **Redis 7.4.1**: In-memory caching for real-time performance
* **PostgreSQL 16.5**: Reliable relational database

### Bot

* Built with **Python**
* Uses **pyTelegramBotAPI** for Telegram integration

### API

* Built with **Python** and **FastAPI** for high-performance web services
* Utilizes **SQLAlchemy** for ORM and **Alembic** for database migrations

### WebApp
* Developed with **TypeScript**
* Frontend powered by **Vue 3**, **Vue Router** and managed via **Pinia**
* Styled with **Vuetify** and **QCalendar** for **Quazar**
