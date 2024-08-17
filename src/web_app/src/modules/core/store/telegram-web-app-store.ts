import { acceptHMRUpdate, defineStore } from 'pinia';
import { ref } from 'vue';

export const useTelegramWebAppStore = defineStore('telegram-web-app-store', () => {
	const applicationTheme = ref<string | null>(null);

	function setWebAppTheme() {
		switch (window.Telegram.WebApp.themeParams.secondary_bg_color) {
			case '#1c1c1d':
				applicationTheme.value = 'dark';
				break;
			default:
				applicationTheme.value = 'bright';
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
