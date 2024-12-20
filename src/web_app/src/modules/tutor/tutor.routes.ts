import { View } from '@/plugins/router/view-definitions';
import type { RouteRecordRaw } from 'vue-router';
import TutorView from '@/modules/tutor/views/tutor-view.vue';
import Dashboard from '@/modules/core/components/dashboard.vue';
import { viewMetaDefinitions } from '@/plugins/router/view-metas';


export const tutorRoutes: RouteRecordRaw[] = [
	{
		path: '/tutor',
		component: Dashboard,
		children: [
			{
				path: '',
				name: View.tutorView,
				component: TutorView,
				meta: viewMetaDefinitions[View.tutorView],
			},
		],
	}
];
