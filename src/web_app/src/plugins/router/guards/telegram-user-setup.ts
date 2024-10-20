import { useTelegramWebApp } from '@/composables/telegram.web-app';
import { useSessionStore } from '@/modules/core/store/session-store';
import { useRouterStore } from '@/modules/core/store/router-store';
import { useUserStore } from '@/modules/core/store/user-store';

export async function setupTelegramUser(): Promise<void> {
	let initData: string | undefined;

	if (import.meta.env.VITE_APP_IS_DEV === 'true') {
		initData = import.meta.env.VITE_APP_WEB_APP_INIT_DATA;
	} else {
		const { getInitData } = useTelegramWebApp();
		initData = getInitData();
	}

	if (!initData) return;

	const authStore = useSessionStore();
	const userStore = useUserStore();

	if (initData === authStore.telegramInitData && userStore.userInfo) return;

	const allowed = await authStore.initializeAuthentication(initData);

	if (allowed === 'forbidden') return;

	useRouterStore().notifyAppInitialized();
}
