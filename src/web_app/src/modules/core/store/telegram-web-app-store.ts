import { acceptHMRUpdate, defineStore } from 'pinia';
import { ref } from 'vue';

type TelegramTheme = 'light' | 'dark';

export const useTelegramWebAppStore = defineStore('telegram-web-app-store', () => {
	const applicationTheme = ref<TelegramTheme>('light');

	function setWebAppTheme() {
		window.Telegram.WebApp.setHeaderColor('#FF0000');
		window.Telegram.WebApp.themeParams.bg_color = '#FF0000';
		window.Telegram.WebApp.setBackgroundColor('#FF0000');
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
