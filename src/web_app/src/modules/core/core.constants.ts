import { View } from '@/plugins/router/view-definitions';

export interface MainMenuGroup {
	mainView: View;
	children: View[];
}

export const mainMenuItems: MainMenuGroup[] = [
	{
		mainView: View.adminView,
		children: [],
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
];
