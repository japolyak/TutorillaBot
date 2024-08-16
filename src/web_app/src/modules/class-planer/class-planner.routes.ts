import type { RouteRecordRaw } from 'vue-router';
import Dashboard from '@/modules/core/components/dashboard.vue';
import PlanClassView from '@/modules/class-planer/views/plan-class-view.vue';


export const classPlannerRoutes: RouteRecordRaw[] = [
	{
		path: '/private-course',
		component: Dashboard,
		children: [
			{
				path: ':privateCourseId',
				name: 'PlanClassView',
				component: PlanClassView,
			},
		],
	}
];
