import { createRouter, createWebHistory } from 'vue-router';
import { classPlannerRoutes } from '@/modules/class-planer/class-planner.routes';
import { devRoutes } from '@/modules/dev/dev.routes';
import { adminRoutes } from '@/modules/admin/admin.routes';
import { tutorRoutes } from '@/modules/tutor/tutor.routes';
import { studentRoutes } from '@/modules/student/student.routes';
import telegramGuard from './guards/telegram.guard'

const router = createRouter({
    history: createWebHistory(),
    routes: [
		...classPlannerRoutes,
		...devRoutes,
		...adminRoutes,
		...tutorRoutes,
		...studentRoutes,
    ],
});

router.beforeEach(async (to, from, next) => await telegramGuard(next));

export default router;
