import type { NavigationGuardWithThis } from 'vue-router';
import {START_LOCATION} from 'vue-router';
import { View } from '@/plugins/router/view-definitions';

const guard: NavigationGuardWithThis<undefined> = async (to, from, next) => {
	const authCheck = to.meta?.authGuard?.checkAccess();

	if (authCheck?.hasAccess) {
		next();
		return;
	}
	console.log('bad')

	if (!authCheck?.hasAccess && authCheck?.noAccessReason === 'onlyAnonymous') {
		console.log('onlyAnonymous');
		next({ name: View.fallbackView, replace: true })
		return;
	}

	if (!authCheck?.hasAccess && authCheck?.noAccessReason === 'missingRoles') {
		console.log('missingRoles');
		if (from === START_LOCATION) {
			next({ name: View.fallbackView, replace: true })
			return;
		}

		next(false);
		return;
	}

	next({ name: View.fallbackView, replace: true, params: {} })
};

export default guard;

