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
	[View.adminView]: [
		{
			title: 'AdminPage',
			disabled: false,
		},
	],
	[View.adminUserView]: [
		{
			title: 'Users',
			disabled: false,
		},
	],
	[View.adminRequestsView]: [
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
	[View.classPlannerView]: [
		{
			title: 'ClassPlanner',
			disabled: false,
		},
	],
}
