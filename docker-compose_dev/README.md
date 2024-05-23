# Docker

This repository contains the necessary files to create a Docker environment for
development purposes.

## Prerequisites

Before setting up the Docker environment, make sure you have the following
files in this directory:

- `.env`: This file contains environment variables required for the Docker
  setup.
- `docker-compose-dev.env`: Another file that includes environment variables
  specifically for Docker Compose.
- `docker-compose-dev.yaml`: The Developement Docker Compose file that defines
  the services and configurations for the containers.

## Quickstart

To quickly start or restart the project, we have created a script
named `restart-dev-env.sh`. This script automates the process and saves you
time.

**Note**: Before running the `restart-dev-env.sh` script, ensure that you have
Docker and the required files mentioned in the prerequisites section.
**Warning**: This script does delete all the running conainers and images. The
user has to proceed with caution while running this script.

The `restart-dev-env.sh` script performs the following actions:

1. Deletes all existing containers.
2. Deletes all existing images.
3. Builds the Redis, bd, front and webserver images.
4. Runs the containers.
5. Launches Django in debug mode on port 8000 and the angular front on 4200

To use the script, follow these steps:

1. Open a terminal or command prompt.

2. Navigate to the directory containing the Docker files.

3. Run the following command:

   ```shell
   sh restart-dev-env.sh
   ```

After running the script, you will be able to access the app at the following
URLs:

- Back env:
  - http://localhost:8000/api/

- Front env:
  - http://localhost:4200/

## TODO:

Currently the breakpoint does not work on the backend environement.

## Manual setup

To set up the Docker environment, follow these steps:

1. Ensure that Docker is installed on your system. If not, please refer to the
   official Docker documentation for instructions on how to install Docker for
   your operating system.

2. Make sure you have the required files mentioned in the prerequisites
   section.

3. Open a terminal in the current directory.

4. Run the following command to start the Docker containers:

   ```shell
   docker-compose -f docker-compose-dev.yml up -d
   ```

   This command will build the necessary images and start the containers in the
   background.

5. Wait for the setup process to complete. You can monitor the logs to check
   the progress.

6. Once the containers are up and running, you can access the web app on

- http://localhost:8000/
- http://localhost:8080/

## Usage

After setting up the Docker environment, you can use it for
development purposes. Here are some useful commands:

- To build webapp image:

  ```shell
  docker-compose build
  ```

- To start the containers:

  ```shell
  docker-compose up -d
  ```

- To stop the containers:

  ```shell
  docker-compose down
  ```

- To view the logs:

  ```shell
  docker-compose logs
  ```

- To access a specific container's shell:

  ```shell
  docker-compose exec <service_name> bash
  ```

  Replace `<service_name>` with the actual name of the container's service
  defined in the `docker-compose.yaml` file.

