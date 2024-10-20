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
	[View.adminView]: new RouteMetaBuilder()
		.withTitle('AdminPage')
		.partOfModule(Module.adminModule)
		.withRoles(Role.Admin)
		.build(),
	[View.adminUserView]: new RouteMetaBuilder()
		.withTitle('Users')
		.partOfModule(Module.adminModule)
		.withRoles(Role.Admin)
		.build(),
	[View.adminRequestsView]: new RouteMetaBuilder()
		.withTitle('RegistrationRequests')
		.partOfModule(Module.adminModule)
		.withRoles(Role.Admin)
		.build(),
	[View.adminRequestsRoleView]: new RouteMetaBuilder()
		.withTitle('RegistrationRequests')
		.partOfModule(Module.adminModule)
		.withRoles(Role.Admin)
		.build(),
	[View.tutorView]: new RouteMetaBuilder()
		.withTitle('TutorPage')
		.partOfModule(Module.tutorModule)
		.withRoles(Role.Tutor)
		.build(),
	[View.studentView]: new RouteMetaBuilder()
		.withTitle('StudentPage')
		.partOfModule(Module.studentModule)
		.withRoles(Role.Student)
		.build(),
}
