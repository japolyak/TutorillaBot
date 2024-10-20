import { acceptHMRUpdate, defineStore } from 'pinia';
import { computed, ref } from 'vue';

export const useRouterStore = defineStore('router-store', () => {
	const initializing = ref(true);
	const initialized = computed(() => !initializing.value);

	function notifyAppInitialized() {
		initializing.value = false;
	}

    return {
		initializing,
		initialized,
		notifyAppInitialized,
    };
});

if (import.meta.hot) {
    import.meta.hot.accept(acceptHMRUpdate(useRouterStore, import.meta.hot));
}
