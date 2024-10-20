import { AuthenticationClient } from '@/modules/core/services/api-clients/authentication-client';
import { useUserStore } from '@/modules/core/store/user-store';
import type { NavigationGuardNext } from 'vue-router';
import { useTelegramWebApp } from '@/composables/telegram.web-app';

async function guard(next: NavigationGuardNext): Promise<void> {
	let initData: string | undefined;

	if (import.meta.env.VITE_APP_IS_DEV === 'true') {
		initData = import.meta.env.VITE_APP_WEB_APP_INIT_DATA;
	} else {
		const { getInitData } = useTelegramWebApp();
		initData = getInitData();
	}

	if (!initData) {
        next(false);
        return;
    }

    const response = await AuthenticationClient.validateInitData(initData);
    if (response.isSuccess) {
		const { setUser } = useUserStore();
		setUser(response.data);
		next();
	}
}

export default guard;
