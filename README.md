# Drag-and-Drop Backend

## Description
This project is a backend designed to handle drag-and-drop operations. It is built with Python and follows a modular architecture to ensure scalability and maintainability.

## Project Structure
The main structure of the project is as follows:

```
/drag-and-drop-be
├── alembic/               # Database migrations
├── src/                   # Main source code
│   ├── api/               # API endpoints
│   ├── core/              # Core configuration and utilities
│   ├── models/            # Data models
│   ├── schemas/           # Validation schemas
│   └── services/          # Business logic
├── uploads/               # Uploaded files
├── alembic.ini            # Alembic configuration
├── docker-compose.yml     # Docker Compose configuration
├── Dockerfile             # Dockerfile to build the image
├── pyproject.toml         # Project configuration (dependencies, etc.)
├── start.py               # Project entry point
└── README.md              # This file
```

## Prerequisites
- Python 3.9 or higher
- Docker (optional, for containers)
- pipenv or pip to manage dependencies

## Installation
1. Clone this repository:
   ```bash
   git clone <REPOSITORY_URL>
   ```
2. Navigate to the project directory:
   ```bash
   cd drag-and-drop-be
   ```
3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
To start the server, run:
```bash
python start.py
```

## Running the Project with Docker

To run the project using Docker, follow these steps:

1. Build the Docker image:
   ```bash
   docker build -t drag-and-drop-be .
   ```

2. Start the services using Docker Compose:
   ```bash
   docker-compose up
   ```

3. The application will be available at `http://localhost:8000` (or the port specified in your `docker-compose.yml`).

4. To stop the services, use:
   ```bash
   docker-compose down
   ```

## Running Database Migrations in Docker

To apply database migrations while using Docker, follow these steps:

1. Start the database service:
   ```bash
   docker-compose up -d db
   ```

2. Run the migrations inside the `api` service:
   ```bash
   docker-compose run api alembic upgrade head
   ```

3. Once the migrations are applied, you can start the entire application:
   ```bash
   docker-compose up
   ```

## Migrations
To apply database migrations:
```bash
alembic upgrade head
```

## Contributions
Contributions are welcome! Please open an issue or submit a pull request to suggest improvements.

## License
This project is licensed under the MIT License.

## Limitations

Due to time constraints, the following features were not implemented:

- **Authentication**: The API does not include any form of authentication.
- **Middleware**: No middleware was developed for additional request/response handling.
- **File Management**: Integration with a file storage service like S3 was not implemented.
- **Error Handling**: Comprehensive error handling mechanisms were not implemented.
- **Logging**: Proper logging mechanisms were not implemented.
- **Unit Tests**: No unit tests were created to validate the functionality of the application.