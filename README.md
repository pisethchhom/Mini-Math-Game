# Mini Math Game

## Overview

Mini Math Game is an educational platform designed to enhance the arithmetic and logical skills of primary school students through interactive games and quizzes. The project is built using Django for the game interface and Directus as the CMS for administrative functions. PostgreSQL is used as the game database and MongoDB is used for session management. The game supports quick deployment using Docker.

---

## Features

- **Dynamic game questions**: Teacher or admin can create and assign game dynamically based on a game type and a difficulty level.
- **Admin dashboard**: This project utilised Directus CMS functionality which enabled admin to:
  - manage game content
  - monitor player information and progress
  - create new user and assign to specific role with permissions

## Project technologies

- **Frontend**:
  - [![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/HTML)
  - [![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/CSS)
  - [![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
- **Backend**:
  - [![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)
- **Admin Dashboard**:
  - [![Directus](https://img.shields.io/badge/Directus-2D69E0?style=for-the-badge&logo=directus&logoColor=white)](https://directus.io/)
- **Database**:
  - [![MongoDB](https://img.shields.io/badge/MongoDB-47A248?style=for-the-badge&logo=mongodb&logoColor=white)](https://www.mongodb.com/)
  - [![PostgreSQL](https://img.shields.io/badge/PostgreSQL-336791?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)

---

## System requirements

- **Python**: Version 3.10 or above.
- **Docker**: Latest version recommended.
- **RAM**: Minimum of 4GB (8GB recommended).
- **Disk Space**: 500MB or more.
- Ensure that Docker and Docker Compose are correctly installed and running before
proceeding to the installation.

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/pisethchhom/Mini-Math-Game.git
   cd Mini-Math-Game
   ```
2. Create .env file:
   ```bash
   cp .env.example .env
   ```
3. Create docker-compose file:
   ```bash
   cp docker-compose-sample.yml docker-compose.yml
   ```
4. Reset to default game data (Optional):
   ```bash
   make reset
   ```
5. Start the project using docker compose:
   ```bash
   docker-compose up -d
   ```

---

## Start the game

- **Game Url**: http://localhost:8000
- **Admin Dashboard (Directus)**: http://localhost:8055
  - Default email: admin@example.com
  - Default password: 123123123
- **Mongo Express Dashboard**: http://localhost:8081
  - Default username: admin
  - Default password: admin_pw
 
---

## Stop the project

1. Run:
   ```bash
   docker-compose down
   ```

---

## Images
### Project Architecture
![Project Architecture](./game_images/architecture.webp)

### Gameplay Screens
<div style="display: flex; flex-wrap: wrap; gap: 10px; justify-content: center;">
  <img src="./game_images/game-screen-0.webp" alt="login screen" style="width: 48%; max-width: 320px; height: auto;"/>
  <img src="./game_images/game-screen-1.webp" alt="register screen" style="width: 48%; max-width: 320px; height: auto;"/>
  <img src="./game_images/game-screen-2.webp" alt="game type" style="width: 48%; max-width: 320px; height: auto;"/>
  <img src="./game_images/game-screen-3.webp" alt="game level" style="width: 48%; max-width: 320px; height: auto;"/>
  <img src="./game_images/game-screen-4.webp" alt="select answer option" style="width: 48%; max-width: 320px; height: auto;"/>
  <img src="./game_images/game-screen-5.webp" alt="question and answer" style="width: 48%; max-width: 320px; height: auto;"/>
</div>

### Admin Dashboard
<div style="display: flex; flex-wrap: wrap; gap: 10px; justify-content: center;">
  <img src="./game_images/admin-dashboard-0.webp" alt="Admin dashboard record detail" style="width: 48%; max-width: 320px; height: auto;"/>
  <img src="./game_images/admin-dashboard-1.webp" alt="Admin dashboard game category" style="width: 48%; max-width: 320px; height: auto;"/>
  <img src="./game_images/admin-dashboard-2.webp" alt="Admin dashboard player" style="width: 48%; max-width: 320px; height: auto;"/>
  <img src="./game_images/admin-dashboard-3.webp" alt="Admin dashboard progress history" style="width: 48%; max-width: 320px; height: auto;"/>
</div>

### Mongo Express
<div style="display: flex; flex-wrap: wrap; gap: 10px; justify-content: center;">
  <img src="./game_images/mongo-express-0.webp" alt="Mongo sample record list" style="width: 48%; max-width: 320px; height: auto;"/>
  <img src="./game_images/mongo-express-1.webp" alt="Mongo sample record detail" style="width: 48%; max-width: 320px; height: auto;"/>
</div>

---

## License

This project is licensed under the MIT License. See the LICENSE file for details.

