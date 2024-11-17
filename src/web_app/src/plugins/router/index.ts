import { createRouter, createWebHistory } from 'vue-router';
import { setupTelegramUser } from './guards/telegram-user-setup'
import authGuard from './guards/auth.guard'
import type { Module } from '@/plugins/router/view-definitions';
import type { RouteAuthMeta } from '@/plugins/router/utils/route-auth-meta';
import { coreRoutes } from '@/modules/core/core.routes';
import { devRoutes } from '@/modules/dev/dev.routes';
import { adminPanelRoutes } from '@/modules/admin-panel/admin-panel.routes';
import { tutorRoutes } from '@/modules/tutor/tutor.routes';
import { studentRoutes } from '@/modules/student/student.routes';
import { scheduleRoutes } from '@/modules/schedule/schedule.routes';

// TODO - remove when all modules will be ready
function availableRoutes() {
	if (import.meta.env.VITE_APP_IS_DEV === '0') return [...scheduleRoutes, ...adminPanelRoutes, ...devRoutes];

	return [
		...scheduleRoutes,
		...adminPanelRoutes,
		...tutorRoutes,
		...studentRoutes,
		...devRoutes,
	]
}

const router = createRouter({
    history: createWebHistory(),
    routes: [
		...availableRoutes(),
		// Must be the last one!
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
