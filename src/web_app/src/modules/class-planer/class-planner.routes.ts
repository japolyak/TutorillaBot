import type { RouteRecordRaw } from 'vue-router';
import Dashboard from '@/modules/core/components/dashboard.vue';
import PlanClassView from '@/modules/class-planer/views/plan-class-view.vue';
import { View } from '@/plugins/router/view-definitions';
import { viewMetaDefinitions } from '@/plugins/router/view-metas';


export const classPlannerRoutes: RouteRecordRaw[] = [
	{
		path: '/private-course',
		component: Dashboard,
		children: [
			{
				path: ':privateCourseId',
				name: View.classPlannerView,
				component: PlanClassView,
				meta: viewMetaDefinitions[View.classPlannerView],
			},
		],
	}
];
