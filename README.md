# IoT-Project

Developed by Rúben Torres (fc62531@alunos.fc.ul.pt) and João Martins (fc62532@alunos.fc.ul.pt).

*As part of the curricular unit Internet of Things (23/24) at the Faculty of Sciences, University of Lisbon.*

## Table of Contents
- [Prerequisites](#prerequisites)
- [How to Run the Project](#how-to-run-the-project)

## Prerequisites

1. **Git:**
    - [ ] Install Git for version control.
        - [Git Installation](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)

2. **Python:**
    - [ ] Ensure that Python is installed on your machine.
        - [Python Installation](https://www.python.org/downloads/)
        - After installation, verify by running:
            ```bash
            python --version
            ```

3. **Docker:**
    - [ ] Install Docker to run containers.
        - [Docker Installation](https://docs.docker.com/get-docker/)
        - After installation, verify by running:
            ```bash
            docker --version
            ```

## How to Run the Project

Follow these steps to set up and run the project on your local machine:

1. **Clone the Repository:**
    - Choose one of the following options:

    - **HTTPS:**
      ```bash
      git clone https://github.com/rubentorres-developer/IoT-Project.git
      ```

    - **SSH:**
      ```bash
      git clone git@github.com:rubentorres-developer/IoT-Project.git
      ```

    - Change to the project directory:
      ```bash
      cd IoT-Project
      ```

2. **Create the .env File:**
    - Create a file named `.env` in the project root.
    - You can use a text editor or run the following command:
        ```bash
        touch .env
        ```
    - Open the `.env` file and add the following variables:
        ```dotenv
        MONGO_INITDB_ROOT_USERNAME=your_username
        MONGO_INITDB_ROOT_PASSWORD=your_password
        ME_CONFIG_MONGODB_URL=mongodb://your_username:your_password@mongo:27017/
        ```

3. **Create a Virtual Environment Inside the Client Folder, Activate, and Install Dependencies:**
    - Navigate to the `client` folder:
        ```bash
        cd client
        ```
    - Create a virtual environment named `.venv` and activate it:
        ```bash
        python -m venv .venv
        ```
        - For Windows:
            ```bash
            .venv\Scripts\activate
            ```
        - For macOS/Linux:
            ```bash
            source .venv/bin/activate
            ```
    - Install project dependencies using pip:
        ```bash
        pip install -r requirements.txt
        ```

4. **Run with Docker in the Root Directory:**
       - If you prefer using Docker, you can use the provided `docker-compose.yaml` file.
         - Ensure you are in the root directory:
            ```bash
            cd ..
            ```
         - Run the following command:
            ```bash
            docker compose up --force-recreate
            ```

   - Note: Wait for the Docker setup to finish before proceeding to the next step.

5. **Run the Client Inside the Client Folder:**
    - Ensure you are still inside the `client` folder:
        ```bash
        cd client
        ```
    - Execute the following command to start the client:
         ```bash
         python client.py
         ```

6. **Access the Application:**
       - Once the project is running, access the application in your web browser at [http://localhost:8888](http://localhost:8888).
