export enum Module {
	adminPanelModule = 'admin-panel-module',
	tutorModule = 'tutor-module',
	studentModule = 'student-module',
	scheduleModule = 'schedule-module'
}

export enum View {
	fallbackView = 'FallbackView',
	adminPanelView = 'AdminPanelView',
	adminUserView = 'AdminUsersView',
	adminPanelRequestsView = 'AdminPanelRequestsView',
	adminRequestsRoleView = 'AdminRequestsRoleView',
	studentView = 'StudentView',
	tutorView = 'TutorView',
	scheduleView = 'ScheduleView',
	devView = 'DevView',
}

export const moduleViewDefinition: Record<Module, View> = {
	[Module.adminPanelModule]: View.adminPanelView,
	[Module.tutorModule]: View.tutorView,
	[Module.studentModule]: View.studentView,
	[Module.scheduleModule]: View.scheduleView,
};
