import { createApp } from 'vue'
import App from './app.vue'
import vuetify from '@/plugins/vuetify';
import router from '@/plugins/router/index';
import i18n from '@/plugins/i18n/index';
import pinia from '@/plugins/pinia';

const app = createApp(App);

app.use(i18n)
app.use(router)
app.use(pinia)
app.use(vuetify)
app.mount('#app')
