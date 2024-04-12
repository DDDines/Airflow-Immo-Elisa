# Real Estate Analysis Project with Airflow

This project uses Apache Airflow to automate the collection, cleaning, and analysis of real estate data. The system is structured around Docker, facilitating configuration and scalability.

## Configuration and Installation

The project is containerized using Docker and Docker Compose, including services for Airflow and PostgreSQL.

### Prerequisites

- Docker
- Docker Compose

### Installation Instructions

1. Clone the repository:

   ```bash
   git clone [repository URL]
   cd [repository directory name]
   ```

2. Start the services using Docker Compose:
   ```bash
   docker-compose up
   ```

## System Components

### Docker Services

- **PostgreSQL**: Database for Airflow.
- **Webserver**: Airflow's web interface for monitoring and managing workflows.
- **Scheduler**: Airflow's scheduler that executes scheduled tasks.

### Python Scripts

- **`train.py`**: Trains a regression model to predict real estate prices using cleaned data. Utilizes scikit-learn for training and model evaluation.
- **`clean.py`**: Cleans collected data, preparing it for analysis. Includes detailed cleaning processes like value mapping and unnecessary column removal.
- **`main.py`**: Main script that can initiate the crawler for data collection.

### Airflow DAGs

- **`dags.py`**: Defines the scheduling and dependency logic among scraping, cleaning, and model training tasks.

## Usage

After starting the Docker services, access the Airflow web interface through a browser at `localhost:8080` to monitor and interact with scheduled DAGs.
