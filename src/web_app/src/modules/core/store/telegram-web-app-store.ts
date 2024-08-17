import { acceptHMRUpdate, defineStore } from 'pinia';
import { ref, computed } from 'vue';

export const useTelegramWebAppStore = defineStore('telegram-web-app-store', () => {
	const applicationTheme = ref<string | null>(null);

    return {
        applicationTheme
    };
});

if (import.meta.hot) {
    import.meta.hot.accept(acceptHMRUpdate(useTelegramWebAppStore, import.meta.hot));
}
