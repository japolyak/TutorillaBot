# TutorillaBot

**TutorillaBot** is an online Telegram-based language learning platform, designed to facilitate language learning.
By connecting learners with experienced tutors, the platform provides a seamless and interactive platform where users can find
and book personalised language lessons.

From a technical perspective, the platform is powered by three different microservices and virtual machine with **Redis** and **PostgreSQL** databases.
All components are deployed in **Google Cloud Platform** and each plays a critical role in the overall system:

* **Telegram Bot** - Acts as the primary interface for users, providing direct interaction through the Telegram API.
It connects to both the API and the Web App to facilitate real-time communication.
It also integrates with **Redis** for caching and fast data retrieval.
* **Redis** - Acts as an in-memory data store, providing caching and quick access to frequently requested user data.
* **Web App** - Allows users to schedule lessons and manage their bookings.
* **API** - Handles the communication between the Telegram Bot, Web App and the database.
It handles data processing, storage, and retrieval, ensuring seamless integration and operation across the platform.

Due to the chosen cloud technologies and the location of the virtual machines, the initial interaction with the bot can
take up to 10 seconds. This latency is a trade-off for current setup, which accommodates a small initial user base.
As the project scales and the number of users increases, it's planned to adjust the deployment strategy to improve performance and reduce latency.

## Used technologies

# Deployment and Infrastructure

* **Docker**
* **Google Cloud Platform**
  * **Cloud Run**
  * **Cloud Build**
  * **Compute Engine**

# Bot

* **Python 3.12**
* **pyTelegramBotAPI**
* **Redis**
* **FastAPI**

# API

* **Python 3.12**
* **FastAPI**
* **PostgreSQL**
* **SQLAlchemy** and **Alembic**

# WebApp
* **TypeScript**
* **Vue.js (v3)**, **Vuetify** and **Pinia**
