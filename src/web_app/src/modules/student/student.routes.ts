import { View } from '@/plugins/router/view-definitions';
import type { RouteRecordRaw } from 'vue-router';
import StudentView from '@/modules/student/views/student-view.vue';
import Dashboard from '@/modules/core/components/dashboard.vue';
import { viewMetaDefinitions } from '@/plugins/router/view-metas';


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
