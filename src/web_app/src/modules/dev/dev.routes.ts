import type { RouteRecordRaw } from 'vue-router';
import Dashboard from '@/modules/core/components/dashboard.vue';
import DevView from '@/modules/dev/views/dev-view.vue';
import { View } from '@/plugins/router/view-definitions';
import { viewMetaDefinitions } from '@/plugins/router/view-metas';


export const devRoutes: RouteRecordRaw[] = [
	{
		path: '/dev',
		component: Dashboard,
		children: [
			{
				path: '',
				name: View.devView,
				component: DevView,
				meta: viewMetaDefinitions[View.devView],
			},
		],
	}
];
