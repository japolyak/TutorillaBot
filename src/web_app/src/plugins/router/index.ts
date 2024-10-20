import { createRouter, createWebHistory } from 'vue-router';
import telegramGuard from './guards/telegram.guard'
import type { Module } from '@/plugins/router/view-definitions';
import { classPlannerRoutes } from '@/modules/class-planer/class-planner.routes';
import { devRoutes } from '@/modules/dev/dev.routes';
import { adminRoutes } from '@/modules/admin/admin.routes';
import { tutorRoutes } from '@/modules/tutor/tutor.routes';
import { studentRoutes } from '@/modules/student/student.routes';
import { scheduleRoutes } from '@/modules/schedule/schedule.routes';

const router = createRouter({
    history: createWebHistory(),
    routes: [
		...classPlannerRoutes,
		...scheduleRoutes,
		...devRoutes,
		...adminRoutes,
		...tutorRoutes,
		...studentRoutes,
    ],
});

router.beforeEach(async (to, from, next) => await telegramGuard(next));

export default router;

declare module 'vue-router' {
	export interface RouteMeta {
		title: string;
		icon: string | null;
		module: Module | null;
	}
}
