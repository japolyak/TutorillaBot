import type { RouteRecordRaw } from 'vue-router';
import Dashboard from '@/modules/core/components/dashboard.vue';
import DevView from '@/modules/dev/views/dev-view.vue';
import { View } from '@/plugins/router/view-definitions';


export const devRoutes: RouteRecordRaw[] = [
	{
		path: '/dev',
		component: Dashboard,
		children: [
			{
				path: '',
				name: View.devView,
				component: DevView,
			},
		],
	}
];
