import type { RouteRecordRaw } from 'vue-router';
import { View } from '@/plugins/router/view-definitions';
import { viewMetaDefinitions } from '@/plugins/router/view-metas';
import Dashboard from '@/modules/core/components/dashboard.vue';
import ScheduleView from '@/modules/schedule/views/schedule-view.vue';


export const scheduleRoutes: RouteRecordRaw[] = [
	{
		path: '/schedule',
		component: Dashboard,
		children: [
			{
				path: '',
				name: View.scheduleView,
				component: ScheduleView,
				meta: viewMetaDefinitions[View.scheduleView],
			},
		],
	}
];
