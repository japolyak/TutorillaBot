import { View } from '@/plugins/router/view-definitions';
import type { RouteRecordRaw } from 'vue-router';
import { viewMetaDefinitions } from '@/plugins/router/view-metas';
import Dashboard from '@/modules/core/components/dashboard.vue';
import AdminView from '@/modules/admin/views/admin-view.vue';
import AdminRequestsRoleView from '@/modules/admin/views/admin-requests-role-view.vue';
import AdminRequestsView from '@/modules/admin/views/admin-requests-view.vue';
import AdminUsersView from '@/modules/admin/views/admin-users-view.vue';


export const adminRoutes: RouteRecordRaw[] = [
	{
		path: '/admin',
		component: Dashboard,
		children: [
			{
				path: '',
				name: View.adminView,
				component: AdminView,
				meta: viewMetaDefinitions[View.adminView],
			},
			{
				path: 'requests',
				children: [
					{
						path: '',
						name: View.adminRequestsView,
						component: AdminRequestsView,
						meta: viewMetaDefinitions[View.adminRequestsView],
					},
					{
						path: ':role',
						name: View.adminRequestsRoleView,
						component: AdminRequestsRoleView,
						meta: viewMetaDefinitions[View.adminRequestsRoleView],
					},
				],
			},
			{
				path: 'users',
				name: View.adminUserView,
				component: AdminUsersView,
				meta: viewMetaDefinitions[View.adminUserView],
			},
		],
	}
];
