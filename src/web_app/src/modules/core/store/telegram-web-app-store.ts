import { acceptHMRUpdate, defineStore } from 'pinia';
import { ref } from 'vue';

type TelegramTheme = 'light' | 'dark';

export const useTelegramWebAppStore = defineStore('telegram-web-app-store', () => {
	const applicationTheme = ref<TelegramTheme>('light');

	function setWebAppTheme() {
		applicationTheme.value = window.Telegram.WebApp.colorScheme;
	}

	function setMainButton(value: string) {
		window.Telegram.WebApp.MainButton.text = value;
	}

    return {
        applicationTheme,
		setWebAppTheme,
		setMainButton,
    };
});

if (import.meta.hot) {
    import.meta.hot.accept(acceptHMRUpdate(useTelegramWebAppStore, import.meta.hot));
}
