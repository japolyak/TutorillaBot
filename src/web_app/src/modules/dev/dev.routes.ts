import type { RouteRecordRaw } from 'vue-router';
import Dashboard from '@/modules/core/components/dashboard.vue';
import DevView from '@/modules/dev/views/dev-view.vue';


export const devRoutes: RouteRecordRaw[] = [
	{
		path: '/dev',
		component: Dashboard,
		children: [
			{
				path: '',
				name: 'DevView',
				component: DevView,
			},
		],
	}
];
