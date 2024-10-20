import { createRouter, createWebHistory } from 'vue-router';
import { setupTelegramUser } from './guards/telegram-user-setup'
import authGuard from './guards/auth.guard'
import type { Module } from '@/plugins/router/view-definitions';
import type { RouteAuthMeta } from '@/plugins/router/utils/route-auth-meta';
import { classPlannerRoutes } from '@/modules/class-planer/class-planner.routes';
import { coreRoutes } from '@/modules/core/core.routes';
import { devRoutes } from '@/modules/dev/dev.routes';
import { adminRoutes } from '@/modules/admin/admin.routes';
import { tutorRoutes } from '@/modules/tutor/tutor.routes';
import { studentRoutes } from '@/modules/student/student.routes';
import { scheduleRoutes } from '@/modules/schedule/schedule.routes';

const router = createRouter({
    history: createWebHistory(),
    routes: [
		...classPlannerRoutes,
		...devRoutes,
		...scheduleRoutes,
		...adminRoutes,
		...tutorRoutes,
		...studentRoutes,
		...coreRoutes,
	],
});

router.beforeEach(setupTelegramUser);
router.beforeEach(authGuard);

export default router;

declare module 'vue-router' {
	export interface RouteMeta {
		title: string;
		icon: string | null;
		module: Module | null;
		authGuard: RouteAuthMeta;
		/** Removes or adds dashboard layout. */
		useDashboardLayout: boolean;
	}
}
