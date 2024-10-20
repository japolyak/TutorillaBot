import { acceptHMRUpdate, defineStore } from 'pinia';
import {computed, ref} from 'vue';
import { useTelegramWebApp } from '@/composables/telegram.web-app';
import {StringUtils} from '@/utils/string.utils';
import {AuthenticationClient} from "@/modules/core/services/api-clients/authentication-client";
import {useUserStore} from "@/modules/core/store/user-store";


export const useSessionStore = defineStore('session-store', () => {
	const telegramInitData = ref<string | undefined>();

	const isTelegramUser = computed(() => StringUtils.isNotEmpty(telegramInitData.value));

	async function initializeAuthentication(initData: string): Promise<'allowed' | 'forbidden'> {
		const user = await AuthenticationClient.validateInitData(initData);

		if (!user) {
			telegramInitData.value = undefined;
			return 'forbidden';
		}

		telegramInitData.value = initData;

		const { setUser } = useUserStore();
		setUser(user);

		return 'allowed';
	}

    return {
		telegramInitData,
		isTelegramUser,
		initializeAuthentication,
    };
});

if (import.meta.hot) {
    import.meta.hot.accept(acceptHMRUpdate(useSessionStore, import.meta.hot));
}
