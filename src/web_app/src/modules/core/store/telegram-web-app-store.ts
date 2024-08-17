import { acceptHMRUpdate, defineStore } from 'pinia';
import { ref } from 'vue';

type TelegramTheme = 'default' | 'night' | 'dark';

export const useTelegramWebAppStore = defineStore('telegram-web-app-store', () => {
	const applicationTheme = ref<TelegramTheme | null>(null);

	function setWebAppTheme() {
		console.log(window.Telegram.WebApp.themeParams);
		switch (window.Telegram.WebApp.themeParams.secondary_bg_color) {
			case '#1c1c1d':
				applicationTheme.value = 'dark';
				break;
			case '#18222d':
				applicationTheme.value = 'dark';
				break;
			default:
				applicationTheme.value = 'default';
				break;
		}
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
