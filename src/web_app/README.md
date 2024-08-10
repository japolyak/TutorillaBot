# TutorillaBotWebApp

This web application is part of the [TutotillaBot](https://github.com/users/japolyak/projects/2/views/4) project.
Its main purpose is to help users plan classes, check schedules, set homework, and more in an easy-to-use interface.

The app runs on Docker containers and uses Google Cloud Platform for reliability and scalability. It requires the following environment variables for service configuration:

* `VITE_APP_API_URL` - url to [TutorillaBotAPI](https://github.com/japolyak/TutorillaBotAPI)
* `VITE_APP_IS_DEV` - controls the build mode.

The application automatically rebuilds whenever changes are committed to the main branch.
In production, it may be accessed through a Telegram bot, restricting usage to registered bot users.

Technologies and libraries used:
* Vue.js (Vue3) with TypeScript
* Vuetify - UI Library
* [vue-datepicker](https://github.com/Vuepic/vue-datepicker) - simple dateTime picker
