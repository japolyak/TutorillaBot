# WebApp

The WebApp is an integral part of the **Tutorilla** project, designed to operate exclusively through Telegram.
Its primary functions include scheduling classes, managing schedules, setting homework, and providing a user-friendly interface for various tasks.

## Development Setup for Telegram Web App Debugging

To debug the WebApp within the Telegram environment, follow one of the testing methods outlined on this [page](https://docs.ton.org/develop/dapps/telegram-apps/testing-apps).

Telegram requires web apps to be served over https, making it impossible to test a locally running web app directly through Telegram.
To facilitate debugging and development, you need to deploy the application to `Netlify` and retrieve the `WebAppInitData` object that Telegram provides.

### Steps to Set Up Development Environment:

1. **Deploy the Application on Netlify**:
    - Choose the repository that contains your web app for deployment in `Netlify`.
    - Set the `Base directory` to `src/web_app`.
    - Use `npm run build` command as the `Build command`.

2. **Integrate the Deployed Application**:
    - Once the application is successfully deployed, update the WebApp URL in the `BOT` application to point to the newly deployed `WebApp` on `Netlify`.

3. **Run Applications in Development Mode**:
    - Start both the `BOT` application in development mode.
    - Open the `WebApp` in Telegram by clicking on the `Plan class` button. Ensure that the user opening the app has the same ID that was used for database mocking.
    - Inspect opened WebApp and find request to url with `/auth/me/`.
    - Copy from Request value for `init-data` header

4. **Configure Local Web App**:
    - In the root directory of your `WebApp`, create a `.env` file and define the `VITE_APP_WEB_APP_INIT_DATA` variable with the copied `init-data` value, enclosed in double quotes.

This setup will allow your locally running web app to connect with the API.

## Production

The production environment uses **Docker** containers and is deployed on **Google Cloud Platform** to ensure reliability and scalability.
The following environment variables are required for configuring the services:

* `PORT` - Port used by **nginx** to run the application.
* `VITE_APP_API_URL` - URL of the *API*.
* `VITE_APP_IS_DEV` - Indicates whether the build is in development mode.
