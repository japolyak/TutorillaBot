import { createApp } from 'vue'
import App from './App.vue'
import vuetify from '@/plugins/vuetify/vuetify';
import router from '@/plugins/router/index';
import pinia from '@/plugins/pinia';

const app = createApp(App);

app.use(vuetify)
app.use(router)
app.use(pinia)
app.mount('#app')
