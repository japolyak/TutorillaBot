import { computed, ref } from 'vue';
import type { EventNames, EventParams } from '@twa-dev/types';

export function useTelegramWebApp() {
	const webApp = window.Telegram.WebApp;

	const mainButtonVisible = computed(() => webApp.MainButton.isVisible);
	const colorScheme = computed(() => webApp.colorScheme);

	function getInitData() {
		return webApp.initData;
	}

	function setMainButton(value: string) {
		webApp.MainButton.text = value;
	}

	function showMainButton() {
		webApp.MainButton.show()
	}

	function hideMainButton() {
		webApp.MainButton.hide()
	}

	function toggleEvent<T extends EventNames>(eventName: T, callback: (params: EventParams[T]) => unknown) {
		webApp.onEvent(eventName, callback);
	}

	return {
		mainButtonVisible,
		colorScheme,

		getInitData,
		setMainButton,
		showMainButton,
		hideMainButton,
		toggleEvent,
	};
}
