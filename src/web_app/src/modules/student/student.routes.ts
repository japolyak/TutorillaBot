import { View } from '@/plugins/router/view-definitions';
import type { RouteRecordRaw } from 'vue-router';
import StudentView from '@/modules/student/views/student-view.vue';
import Dashboard from "@/modules/core/components/dashboard.vue";


export const studentRoutes: RouteRecordRaw[] = [
	{
		path: '/student',
		component: Dashboard,
		children: [
			{
				path: '',
				name: View.studentView,
				component: StudentView,
			},
		],
	}
];
