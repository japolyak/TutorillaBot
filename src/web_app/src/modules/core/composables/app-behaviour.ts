import { StringUtils } from '@/utils/string.utils';


interface AppBehaviour {
	handleVersion: () => void;
}

export function useAppBehaviour(): AppBehaviour {
	function handleVersion() {
		window.Telegram.WebApp.CloudStorage.getItem('appVersion', (error, result) => {
			const currentVersion: undefined | string = import.meta.env.VITE_APP_VERSION?.replace('v', '');
			if (StringUtils.isEmpty(currentVersion)) return;

			if (StringUtils.isEmpty(result)) {
				window.Telegram.WebApp.CloudStorage.setItem('appVersion', currentVersion.replaceAll('.', '-'));
				window.location.reload();
				return;
			}

			const currentVersionParts = currentVersion.split('.');
			const savedVersionParts = result.split('-');

			if (currentVersionParts.length !== savedVersionParts.length) return;

			for (let i = 0; i < currentVersionParts.length; i++) {
				if (parseInt(currentVersionParts[i]) > parseInt(savedVersionParts[i])) {
					window.Telegram.WebApp.CloudStorage.setItem('appVersion', currentVersion.replaceAll('.', '-'));
					window.location.reload();
					return;
				}
			}
		});
	}

	return {
		handleVersion
	}
}
