import type { NavigationGuardWithThis } from 'vue-router';
import {START_LOCATION} from 'vue-router';
import { View } from '@/plugins/router/view-definitions';

const guard: NavigationGuardWithThis<undefined> = async (to, from, next) => {
	if (import.meta.env.VITE_APP_IS_DEV === '0' && to.meta?.hidden) {
		next({ name: View.fallbackView, replace: true });
		return;
	}

	const authCheck = to.meta?.authGuard?.checkAccess();

	if (authCheck?.hasAccess) {
		next();
		return;
	}

	if (!authCheck?.hasAccess && authCheck?.noAccessReason === 'onlyAnonymous') {
		next({ name: View.fallbackView, replace: true });
		return;
	}

	if (!authCheck?.hasAccess && authCheck?.noAccessReason === 'missingRoles') {
		if (from === START_LOCATION) {
			next({ name: View.fallbackView, replace: true });
			return;
		}

		next(false);
		return;
	}

	next({ name: View.fallbackView, replace: true, params: {} });
};

export default guard;

