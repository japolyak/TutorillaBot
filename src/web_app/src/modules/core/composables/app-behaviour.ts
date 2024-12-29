import { StringUtils } from '@/utils/string.utils';


interface AppBehaviour {
	handleVersion: () => void;
}

export function useAppBehaviour(): AppBehaviour {
	const appVersionKey = 'appVersion';

	function handleVersion() {
		const currentVersion: undefined | string = import.meta.env.VITE_APP_VERSION?.replace('v', '');
		if (StringUtils.isEmpty(currentVersion)) return;

		const savedVersion = localStorage.getItem(appVersionKey);
		if (StringUtils.isEmpty(savedVersion)) {
			localStorage.setItem(appVersionKey, currentVersion);
			window.location.reload();
			return;
		}

		const currentVersionParts = currentVersion.split('.');
		const savedVersionParts = savedVersion.split('-');

		if (currentVersionParts.length !== savedVersionParts.length) return;

		for (let i = 0; i < currentVersionParts.length; i++) {
			if (parseInt(currentVersionParts[i]) > parseInt(savedVersionParts[i])) {
				localStorage.setItem(appVersionKey, currentVersion);
				window.location.reload();
				return;
			}
		}
	}

	return {
		handleVersion
	}
}
