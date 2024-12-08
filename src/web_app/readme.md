# Development Setup for Telegram Web App Debugging

To debug the WebApp within the Telegram environment, follow one of the testing methods outlined on this [page](https://docs.ton.org/develop/dapps/telegram-apps/testing-apps).

Telegram requires web apps to be served over https, making it impossible to test a locally running web app directly through Telegram.
To facilitate debugging and development, you need to deploy the application to `Netlify` and retrieve the `WebAppInitData` object that Telegram provides.

## Steps to Set Up Development Environment:

1. **Deploy the Application on Netlify**:
    - Choose the repository that contains your WebApp and branch for deployment in `Netlify`.
    - Set the `Base directory` to `src/web_app`.
    - Use `npm run build` command as the `Build command`.

2. **Integrate the Deployed Application**:
    - Once the application is successfully deployed, update the WebApp URL in the `BOT` application to point to the newly deployed `WebApp` on `Netlify`.

3. **Run Applications in Development Mode**:
    - Start the `BOT` application with disabled webhooks.
    - Open the `WebApp` in Telegram by clicking on the `Plan class` button. Ensure that the user opening the app has the same ID that was used for database mocking.
    - Inspect opened WebApp and find request to url that ends with `/auth/me/`.
    - Copy from Request value for `init-data` header

4. **Configure Local WebApp**:
    - In the root directory of your `WebApp`, create a `.env` file and define the `VITE_APP_WEB_APP_INIT_DATA` variable with the copied `init-data` value, enclosed in double quotes.

This setup will allow your locally running web application to connect to locally running `API`, but Telegram WebApp API will not be available.

To be able to debug application with Telegram WebApp API, do first of above steps and serve `API` over https.
Add url to `API` as `VITE_APP_API_LINK` environment variable on `netlify`.
At this point local database should be the same as remote.

# Production

The following environment variables are required for configuring the services:

* `WEB_APP_PORT` - Port used by `nginx` to run the application.
* `VITE_APP_API_LINK` - URL to the `API`.
* `VITE_APP_IS_DEV` - Indicates whether the build is in development mode - `1` or `0`
