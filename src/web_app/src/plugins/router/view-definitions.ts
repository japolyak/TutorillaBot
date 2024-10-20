export enum Module {
	adminModule = 'admin-module',
	tutorModule = 'tutor-module',
	studentModule = 'student-module',
	scheduleModule = 'schedule-module'
}

export enum View {
	fallbackView = 'FallbackView',
	adminView = 'AdminView',
	adminUserView = 'AdminUsersView',
	adminRequestsView = 'AdminRequestsView',
	adminRequestsRoleView = 'AdminRequestsRoleView',
	studentView = 'StudentView',
	tutorView = 'TutorView',
	scheduleView = 'ScheduleView',
	devView = 'DevView',
}

export const moduleViewDefinition: Record<Module, View> = {
	[Module.adminModule]: View.adminView,
	[Module.tutorModule]: View.tutorView,
	[Module.studentModule]: View.studentView,
	[Module.scheduleModule]: View.scheduleView,
};
