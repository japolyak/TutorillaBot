import ky, { type KyInstance} from 'ky';
import { StringUtils } from '@/utils/string.utils';
import { AuthenticationClient } from '@/modules/core/services/api-clients/authentication-client';
import { storeToRefs } from 'pinia';
import { useSessionStore } from '@/modules/core/store/session-store';


export const httpClient: KyInstance = ky.create({
    prefixUrl: import.meta.env.VITE_APP_API_LINK,
	hooks: {
		beforeRequest: [
			async (request) => {
				const { isAuthorized } = storeToRefs(useSessionStore());

				let token = sessionStorage.getItem('accessToken');

				if (!isAuthorized.value && StringUtils.isNotEmpty(token)) {
					sessionStorage.removeItem('accessToken');
					token = null;
				}

				if (StringUtils.isEmpty(token)) {
					const response = await AuthenticationClient.authenticateMe();
					if (!response) return;

					token = response.accessToken;

					sessionStorage.setItem('accessToken', token);
				}

				request.headers.set('Authorization', `Bearer ${token}`);
			},
		],
	},
});
