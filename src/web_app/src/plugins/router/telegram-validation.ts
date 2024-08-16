import { AuthenticationClient } from '@/modules/core/services/api-clients/authentication-client';
import { useUserStore } from '@/modules/core/store/user-store';
import type { NavigationGuardNext } from 'vue-router';

export async function telegramUserAuthentication(initData: string, next: NavigationGuardNext): Promise<void> {
	if (import.meta.env.VITE_APP_IS_DEV === 'true') {
		initData = import.meta.env.VITE_APP_WEB_APP_INIT_DATA;
	}

	if (!initData) {
        next(false);
        return;
    }
	console.log('initData', initData);
    const response = await AuthenticationClient.validateInitData(initData);
    if (response.isSuccess) {
		const { setUser } = useUserStore();
		setUser(response.data);
		next();
	}
}
