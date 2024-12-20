import { acceptHMRUpdate, defineStore } from 'pinia';
import { computed, ref } from 'vue';
import { StringUtils } from '@/utils/string.utils';
import { UserClient } from '@/modules/core/services/api-clients/user-client';
import { useUserStore } from '@/modules/core/store/user-store';


export const useSessionStore = defineStore(
	'session-store',
	() => {
		const isAuthorized = ref<boolean>(false);
		const telegramInitData = ref<string>();

		const isTelegramUser = computed(() => StringUtils.isNotEmpty(telegramInitData.value));

		async function initializeAuthentication(): Promise<'allowed' | 'forbidden'> {
			const user = await UserClient.getMe();

			if (!user) return 'forbidden';

			const { setUser } = useUserStore();
			setUser(user);

			return 'allowed';
		}

		function authorize(initData: string) {
			telegramInitData.value = initData;
			isAuthorized.value = true;
		}

		return {
			telegramInitData,
			isAuthorized,
			isTelegramUser,
			initializeAuthentication,
			authorize,
		};
	},
	{
		persist: {
			paths: ['token', ],
		},
	}
);

if (import.meta.hot) {
    import.meta.hot.accept(acceptHMRUpdate(useSessionStore, import.meta.hot));
}
