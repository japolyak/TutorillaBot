import { View } from '@/plugins/router/view-definitions';
import type { RouterLinkProps } from 'vue-router';

type BreadcrumbLink = Partial<RouterLinkProps> & { title: string; disabled?: boolean; titleArguments?: any[] };
export type ViewBreadcrumbs = (string | BreadcrumbLink)[];

export const viewBreadcrumbDefinitions: Record<View, null | ViewBreadcrumbs> = {
	[View.devView]: [
		{
			title: 'DevPage',
			disabled: false,
		},
	],
	[View.scheduleView]: [
		{
			title: 'Schedule',
			disabled: false,
		},
	],
	[View.adminPanelView]: [
		{
			title: 'AdminPanel',
			disabled: false,
		},
	],
	[View.adminPanelRequestsView]: [
		{
			title: 'RegistrationRequests',
			disabled: false,
		},
	],
	[View.tutorView]: [
		{
			title: 'TutorPage',
			disabled: false,
		},
	],
	[View.studentView]: [
		{
			title: 'StudentPage',
			disabled: false,
		},
	],
	[View.adminRequestsRoleView]: [
		{
			title: 'RoleRequests',
			disabled: false,
		},
	],
	[View.fallbackView]: [
		{
			title: 'Error',
			disabled: false,
		},
	],
	[View.adminUserView]: [
		{
			title: 'AllUsers',
			disabled: false,
		},
	],
}
