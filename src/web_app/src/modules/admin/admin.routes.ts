import { View } from '@/plugins/router/view-definitions';
import type { RouteRecordRaw } from 'vue-router';
import AdminView from '@/modules/admin/views/admin-view.vue';
import Dashboard from "@/modules/core/components/dashboard.vue";


export const adminRoutes: RouteRecordRaw[] = [
	{
		path: '/admin',
		component: Dashboard,
		children: [
			{
				path: '',
				name: View.adminView,
				component: AdminView,
			},
		],
	}
];
