import { useSessionStore } from '@/modules/core/store/session-store';
import { useRouterStore } from '@/modules/core/store/router-store';
import { useUserStore } from '@/modules/core/store/user-store';

export async function setupTelegramUser(): Promise<void> {
	const userStore = useUserStore();

	if (userStore.userInfo) return;

	const authStore = useSessionStore();

	const allowed = await authStore.initializeAuthentication();

	if (allowed === 'forbidden') return;

	useRouterStore().notifyAppInitialized();
}
