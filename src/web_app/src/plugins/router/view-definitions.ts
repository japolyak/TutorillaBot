export enum Module {
	adminModule = 'admin-module',
	tutorModule = 'tutor-module',
	studentModule = 'student-module',
	scheduleModule = 'schedule-module',
	classPlannerModule = 'class-planner-module'
}

export enum View {
	fallbackView = 'FallbackView',
	adminPanelView = 'AdminPanelView',
	adminUserView = 'AdminUsersView',
	adminRequestsView = 'AdminRequestsView',
	adminRequestsRoleView = 'AdminRequestsRoleView',
	studentView = 'StudentView',
	tutorView = 'TutorView',
	scheduleView = 'ScheduleView',
	devView = 'DevView',
	// TODO - remove when schedule module will be ready
	classPlannerView = 'ClassPlannerView',
}

export const moduleViewDefinition: Record<Module, View> = {
	[Module.adminModule]: View.adminPanelView,
	[Module.tutorModule]: View.tutorView,
	[Module.studentModule]: View.studentView,
	[Module.scheduleModule]: View.scheduleView,
	[Module.classPlannerModule]: View.classPlannerView,
};
