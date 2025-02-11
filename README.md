# Microservice Starter

A starter pack for building microservices with Python, Flask, and SQLAlchemy. This project provides a development-ready structure with JWT authentication, database management, logging, and more.

## Features

- **Python 3**: Leverages the latest features of Python.
- **Flask**: A lightweight WSGI web application framework.
- **SQLAlchemy**: SQL toolkit and Object-Relational Mapping (ORM) library.
- **JWT Authentication**: Secure authentication mechanism.
- **Docker**: Containerization for consistent development and deployment environments.
- **Alembic**: Database migrations tool.

## Getting Started

### Prerequisites

- **Docker**: Ensure Docker is installed on your system. You can download it from the [official website](https://www.docker.com/get-started).

### Installation

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/stefanFramework/microservice-starter.git
   cd microservice-starter
   ```

2. **Configure Environment Variables**:

   - Duplicate the `.env.example` file and rename the copy to `.env`:

     ```bash
     cp .env.example .env
     ```

   - Open the `.env` file with a text editor and set the environment variables as needed. Below is a description of the key variables:
     - `ENVIRONMENT`: The environment in which the app is running; typically `development` or `production`.
     - `JWT_SECRET_KEY`: A private key that will be used to sign the token used for authentication.
     - `SQLALCHEMY_DATABASE_URI`: The database connection URL. For example, for a PostgreSQL database: `postgresql://user:password@localhost:5432/database_name`.

     Ensure that the `SQLALCHEMY_DATABASE_URI` matches the database configuration specified in the `docker-compose.yml` file if you're using Docker for the database service.

3. **Start the Application with Docker**:

   - Build and start the Docker containers:

     ```bash
     docker-compose up --build
     ```

     This command will build the Docker images and start the services defined in the `docker-compose.yml` file. By default, this includes the Flask application and a PostgreSQL database.

   - To stop the services:

     ```bash
     docker-compose down
     ```

     This command stops and removes the containers defined in the `docker-compose.yml` file.

## Project Structure

```
microservice-starter/
├── app/
│   ├── api/
│   ├── __init__.py
│   ├── config.py
│   ├── main.py
│   ├── models.py
│   └── ...
├── migrations/
├── tests/
├── .env.example
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

- `app/`: Contains the main application code.
- `migrations/`: Directory for Alembic database migrations.
- `tests/`: Contains test cases for the application.
- `.env.example`: Example environment variables file.
- `Dockerfile`: Docker configuration for the Flask application.
- `docker-compose.yml`: Docker Compose configuration for multi-container applications.
- `requirements.txt`: Python dependencies.

## Running Migrations

To handle database migrations with Alembic:

1. **Generate a New Migration**:

   ```bash
   docker-compose exec microservice_app alembic revision --autogenerate -m "Migration message"
   ```

2. **Apply Migrations**:

   ```bash
   docker-compose exec microservice_app alembic upgrade head
   ```

## Testing

To run tests:

```bash
docker-compose exec microservice_app pytest
```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the AGPL-3.0 License. See the [LICENSE](LICENSE) file for details.

