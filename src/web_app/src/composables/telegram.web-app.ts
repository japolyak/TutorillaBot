import { computed, ref } from 'vue';
import type { EventNames, EventParams } from '@twa-dev/types';

export function useTelegramWebApp() {
	const webApp = ref(window.Telegram.WebApp);

	const mainButtonVisible = computed(() => webApp.value.MainButton.isVisible);
	const colorScheme = computed(() => webApp.value.colorScheme);

	function getInitData() {
		return webApp.value.initData;
	}

	function setMainButton(value: string) {
		webApp.value.MainButton.text = value;
	}

	function showMainButton() {
		webApp.value.MainButton.show()
	}

	function hideMainButton() {
		webApp.value.MainButton.hide()
	}

	function toggleEvent<T extends EventNames>(eventName: T, callback: (params: EventParams[T]) => unknown) {
		webApp.value.onEvent(eventName, callback());
	}

	return {
		webApp,

		mainButtonVisible,
		colorScheme,

		getInitData,
		setMainButton,
		showMainButton,
		hideMainButton,
		toggleEvent,
	};
}
