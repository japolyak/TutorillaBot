import ky from 'ky';
import type { TokenDto } from '@/modules/core/services/api/api.models';
import { ApiUtils } from '@/modules/core/services/api/api.utils';
import { useTelegramWebApp } from '@/composables/telegram.web-app';
import { useSessionStore } from '@/modules/core/store/session-store';
import { StringUtils } from '@/utils/string.utils';

export class AuthenticationClient {
	public static async authenticateMe(): Promise<TokenDto | null> {
		let initData: string | undefined;

		if (import.meta.env.VITE_APP_IS_DEV === '1') {
			initData = import.meta.env.VITE_APP_WEB_APP_INIT_DATA;
		} else {
			const { getInitData } = useTelegramWebApp();
			initData = getInitData();
		}

		if (StringUtils.isEmpty(initData)) return null;

		const response = await AuthenticationClient.getSession(initData);
		if (!response) return null;

		useSessionStore().authorize(initData);

		return response;
	}

	public static async refreshSession(): Promise<TokenDto | null> {
		const response = await AuthenticationClient.refreshSessionRequest();
		if (!response) return null;

		return response;
	}

    private static async getSession(initData: string): Promise<TokenDto | null> {
		const url = `${import.meta.env.VITE_APP_API_LINK}/auth/me/`;

		const request = ky.get(
			url,
			{ headers: { 'Init-Data': initData }, cache: 'no-store', credentials: 'include' },
		).json<TokenDto>();
		const apiResponse = await ApiUtils.createApiResponse(request);

		return apiResponse.isSuccess ? apiResponse.data : null;
    }

    private static async refreshSessionRequest(): Promise<TokenDto | null> {
		const url = `${import.meta.env.VITE_APP_API_LINK}/auth/refresh/`;

		const request = ky.get(url, { cache: 'no-store', credentials: 'include' }).json<TokenDto>();
		const apiResponse = await ApiUtils.createApiResponse(request);

		return apiResponse.isSuccess ? apiResponse.data : null;
    }
}
