import { acceptHMRUpdate, defineStore } from 'pinia';
import { ref } from 'vue';
import { useTelegramWebApp } from '@/composables/telegram.web-app';

type TelegramTheme = 'light' | 'dark';

export const useTelegramWebAppStore = defineStore('telegram-web-app-store', () => {
	const applicationTheme = ref<TelegramTheme>('light');
	const { colorScheme } = useTelegramWebApp();

	function setWebAppTheme() {
		applicationTheme.value = colorScheme.value;
	}

    return {
        applicationTheme,
		setWebAppTheme,
    };
});

if (import.meta.hot) {
    import.meta.hot.accept(acceptHMRUpdate(useTelegramWebAppStore, import.meta.hot));
}
