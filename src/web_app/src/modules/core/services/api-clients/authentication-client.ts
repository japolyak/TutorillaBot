import ky from 'ky';
import type { TokenDto } from '@/modules/core/services/api/api.models';
import { ApiUtils } from '@/modules/core/services/api/api.utils';
import { useTelegramWebApp } from '@/composables/telegram.web-app';
import { storeToRefs } from 'pinia';
import { useSessionStore } from '@/modules/core/store/session-store';

export class AuthenticationClient {
	public static async authenticateMe (): Promise<string | null> {
		let initData: string | undefined;

		if (import.meta.env.VITE_APP_IS_DEV === 'true') {
			initData = import.meta.env.VITE_APP_WEB_APP_INIT_DATA;
		} else {
			const { getInitData } = useTelegramWebApp();
			initData = getInitData();
		}

		if (!initData) return null;

		const response = await AuthenticationClient.validateInitData(initData);
		if (!response) return null;

		const { telegramInitData } = storeToRefs(useSessionStore());
		telegramInitData.value = initData;

		return response.token;
	}

    public static async validateInitData(initData: string): Promise<TokenDto | null> {
		const url = `${import.meta.env.VITE_APP_API_URL}auth/me/`;

		const request = ky.get(url, { headers: { 'Init-Data': initData }, timeout: 30000 }).json<TokenDto>();
		const apiResponse = await ApiUtils.createApiResponse(request);

		return apiResponse.isSuccess ? apiResponse.data : null;
    }
}
