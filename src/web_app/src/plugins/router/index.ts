import { createRouter, createWebHistory } from 'vue-router';
import { telegramUserAuthentication } from '@/plugins/router/telegram-validation'
import { classPlannerRoutes } from '@/modules/class-planer/class-planner.routes';
import { devRoutes } from '@/modules/dev/dev.routes';

const router = createRouter({
    history: createWebHistory(),
    routes: [
		...classPlannerRoutes,
		...devRoutes,
    ],
});

router.beforeEach(async (to, from, next) => await telegramUserAuthentication(window.Telegram.WebApp.initData, next));

export default router;
