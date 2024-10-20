import { View } from '@/plugins/router/view-definitions';
import { viewMetaDefinitions } from '@/plugins/router/view-metas';
import type { RouteRecordRaw } from 'vue-router';
import Dashboard from '@/modules/core/components/dashboard.vue';
import StudentView from '@/modules/student/views/student-view.vue';


export const studentRoutes: RouteRecordRaw[] = [
	{
		path: '/student',
		component: Dashboard,
		children: [
			{
				path: '',
				name: View.studentView,
				component: StudentView,
				meta: viewMetaDefinitions[View.studentView],
			},
		],
	}
];
