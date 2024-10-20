import { createRouter, createWebHistory } from 'vue-router';
import { classPlannerRoutes } from '@/modules/class-planer/class-planner.routes';
import { devRoutes } from '@/modules/dev/dev.routes';
import telegramGuard from './guards/telegram.guard'

const router = createRouter({
    history: createWebHistory(),
    routes: [
		...classPlannerRoutes,
		...devRoutes,
    ],
});

router.beforeEach(async (to, from, next) => await telegramGuard(next));

export default router;
