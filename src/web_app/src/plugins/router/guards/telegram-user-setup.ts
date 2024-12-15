import { useSessionStore } from '@/modules/core/store/session-store';
import { useRouterStore } from '@/modules/core/store/router-store';
import { useUserStore } from '@/modules/core/store/user-store';
import { type NavigationGuardWithThis } from 'vue-router';
import { View } from '@/plugins/router/view-definitions';

const telegramUserSetup: NavigationGuardWithThis<undefined> = async (to, from, next) => {
	if (to.name === View.fallbackView) {
		next();
		return;
	}

	const userStore = useUserStore();

	if (userStore.userInfo) {
		next();
		return;
	}

	const authStore = useSessionStore();

	const allowed = await authStore.initializeAuthentication();

	if (allowed === 'forbidden') {
		next({ name: View.fallbackView, replace: true });
		return;
	}

	useRouterStore().notifyAppInitialized();
	next();
};

export default telegramUserSetup;
