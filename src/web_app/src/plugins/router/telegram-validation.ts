import { AuthenticationClient } from '@/modules/core/services/api-clients/authentication-client';
import { useUserStore } from '@/modules/core/store/user-store';
import type { NavigationGuardNext } from 'vue-router';

export async function telegramUserAuthentication(initData: string, next: NavigationGuardNext): Promise<void> {
	if (import.meta.env.VITE_APP_IS_DEV === 'true') {
		next();
		return;
	}

	if (!initData) {
        next(false);
        return;
    }

    const request = await AuthenticationClient.validateInitData(initData);
    if (request) {
		const { setUser } = useUserStore();
		setUser(request);
		next();
	}
}
