# Production setup

After the server is **properly** configured, follow these steps to configure the production environment for deployment.

---

## Setup steps

1. Clone the Repository
   * Clone the repository and switch to the `development` branch.
   * Update the path in `.github/workflows/production.yaml`
1. In the `src` directory, create a `.env` file with the following structure:
    ```
    IS_DEVELOPMENT=0

    # Database
    DB_USER=your_db_user
    DB_PASSWORD=your_db_password
    DB_NAME=your_db_name
    DB_PORT=your_db_port
    DB_HOST=postgres
    
    #API
    ALLOWED_ORIGINS=allowed_origins_separated_by_&_char
    API_PORT=your_api_port
    ALGORITHM=your_encryption_algorithm
    API_LINK=http://api_container_name:API_PORT
    
    #Telegram
    BOT_PORT=your_bot_port
    BOT_TOKEN=your_tg_bot_token
    ADMIN_TG_ID=your_tg_admin_id
    WEB_APP_LINK=your_web_app_link
    
    #Redis
    REDIS_HOST=redis
    
    #WebApp
    WEB_APP_PORT=your_web_app_port
    VITE_APP_API_LINK=https://your.domain.com/api
    ```
1. Create a Docker network running the following command
    ```shell
    docker network create tutorilla-network
    ```
1. Build and start the necessary containers for storage services using:
    ```shell
    docker compose -f docker-compose-storages.yaml -p tutorilla up -d
     ```

## Merging changes to the `main` branch

Once all the steps above are complete, you can cross fingers and update the remote `main` branch with changes from the remote `development` branch.
Follow these guidelines:

* Always pull the latest changes from the remote `development` branch before merging to the `main` branch.
