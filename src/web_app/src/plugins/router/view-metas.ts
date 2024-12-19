import type { RouteMeta } from 'vue-router';
import { Module, View } from './view-definitions';
import { RouteMetaBuilder } from '@/plugins/router/utils/route-meta-builder';
import { Role } from '@/modules/core/services/api/api.models';

export const viewMetaDefinitions: Record<View, RouteMeta> = {
	[View.fallbackView]: new RouteMetaBuilder().allowAnonymous().hideDashboardLayout().build(),
	[View.devView]: new RouteMetaBuilder().allowAnonymous().withTitle('DevPage').build(),
	[View.scheduleView]: new RouteMetaBuilder()
		.withTitle('Schedule')
		.partOfModule(Module.scheduleModule)
		.withRoles(Role.Tutor, Role.Student)
		.build(),
	[View.adminPanelView]: new RouteMetaBuilder()
		.withTitle('AdminPanel')
		.partOfModule(Module.adminPanelModule)
		.withRoles(Role.Admin)
		.build(),
	[View.adminUserView]: new RouteMetaBuilder()
		.withTitle('Users')
		.partOfModule(Module.adminPanelModule)
		.withRoles(Role.Admin)
		.build(),
	[View.adminPanelRequestsView]: new RouteMetaBuilder()
		.withTitle('RegistrationRequests')
		.partOfModule(Module.adminPanelModule)
		.withRoles(Role.Admin)
		.build(),
	[View.adminRequestsRoleView]: new RouteMetaBuilder()
		.withTitle('RegistrationRequests')
		.partOfModule(Module.adminPanelModule)
		.withRoles(Role.Admin)
		.build(),
	[View.tutorView]: new RouteMetaBuilder()
		.withTitle('TutorPage')
		.partOfModule(Module.tutorModule)
		.withRoles(Role.Tutor)
		.hide()
		.build(),
	[View.studentView]: new RouteMetaBuilder()
		.withTitle('StudentPage')
		.partOfModule(Module.studentModule)
		.withRoles(Role.Student)
		.hide()
		.build(),
}
