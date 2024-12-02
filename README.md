# Mini Math Game

---

## Overview

Mini Math Game is an educational platform designed to enhance the arithmetic and logical skills of primary school students through interactive games and quizzes. The project is built using Django for the game interface and Directus as the CMS for administrative functions. PostgreSQL is used as the game database and MongoDB is used for session management. The game supports quick deployment using Docker.

---

## Features

- **Interactive Games**: Includes quizzes for arithmetic, geometry, and sorting tasks with dynamic difficulty levels.
- **Role-Based Access**: Teachers and students have distinct roles for appropriate access.
- **Performance Tracking**: Real-time scoring and performance analytics for students.
- **Admin Dashboard**: Managed via Directus, enabling teachers to create quizzes and monitor student progress.
- **Database Management**: Dual database system:
  - **PostgreSQL**: For structured data like users and quiz metadata.
  - **MongoDB**: For session data and detailed performance logs.

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
2. Reset to default game data (Optional):
   ```bash
   make reset
   ```
4. Start the project using docker compose:
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

## License

This project is licensed under the MIT License. See the LICENSE file for details.

