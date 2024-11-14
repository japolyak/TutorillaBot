import { View } from '@/plugins/router/view-definitions';

export interface MainMenuGroup {
	mainView: View;
	children: View[];
}

export const mainMenuItems: MainMenuGroup[] = [
	{
		mainView: View.scheduleView,
		children: [],
	},
	{
		mainView: View.adminPanelView,
		children: [View.adminPanelRequestsView],
	},
	{
		mainView: View.studentView,
		children: [],
	},
	{
		mainView: View.tutorView,
		children: [],
	},
	{
		mainView: View.devView,
		children: [],
	},
	{
		mainView: View.classPlannerView,
		children: [],
	},
];
