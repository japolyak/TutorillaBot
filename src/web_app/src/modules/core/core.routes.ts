import { View } from '@/plugins/router/view-definitions';
import type { RouteRecordRaw } from 'vue-router';
import { viewMetaDefinitions } from '@/plugins/router/view-metas';
import Dashboard from '@/modules/core/components/dashboard.vue';
import FallbackView from './views/fallback-view.vue';

export const coreRoutes: RouteRecordRaw[] = [
	{
		path: '/error',
		component: Dashboard,
		children: [
			{
				path: '',
				name: View.fallbackView,
				component: FallbackView,
				meta: viewMetaDefinitions[View.fallbackView],
			},
		],
	}
];
