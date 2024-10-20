import type { RouteMeta } from 'vue-router';
import { Module, View } from './view-definitions';
import { RouteMetaBuilder } from '@/plugins/router/utils/route-meta-builder';

export const viewMetaDefinitions: Record<View, RouteMeta> = {
	[View.devView]: new RouteMetaBuilder().withTitle('DevPage').build(),
	[View.scheduleView]: new RouteMetaBuilder()
		.withTitle('Schedule')
		.partOfModule(Module.scheduleModule)
		.build(),
	[View.adminView]: new RouteMetaBuilder()
		.withTitle('AdminPage')
		.partOfModule(Module.adminModule)
		.build(),
	[View.adminUserView]: new RouteMetaBuilder()
		.withTitle('Users')
		.partOfModule(Module.adminModule)
		.build(),
	[View.adminRequestsView]: new RouteMetaBuilder()
		.withTitle('RegistrationRequests')
		.partOfModule(Module.adminModule)
		.build(),
	[View.adminRequestsRoleView]: new RouteMetaBuilder()
		.withTitle('RegistrationRequests')
		.partOfModule(Module.adminModule)
		.build(),
	[View.tutorView]: new RouteMetaBuilder()
		.withTitle('TutorPage')
		.partOfModule(Module.tutorModule)
		.build(),
	[View.studentView]: new RouteMetaBuilder()
		.withTitle('StudentPage')
		.partOfModule(Module.studentModule)
		.build(),
}
