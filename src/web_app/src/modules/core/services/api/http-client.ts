import ky, { type KyInstance} from 'ky';
import { StringUtils } from '@/utils/string.utils';
import { AuthenticationClient } from '@/modules/core/services/api-clients/authentication-client';
import { storeToRefs } from 'pinia';
import { useSessionStore } from '@/modules/core/store/session-store';


export const httpClient: KyInstance = ky.create({
    prefixUrl: import.meta.env.VITE_APP_API_URL,
	hooks: {
		beforeRequest: [
			async (request) => {
				const { isAuthorized } = storeToRefs(useSessionStore());

				let token = localStorage.getItem('authToken');

				if (!isAuthorized.value && StringUtils.isNotEmpty(token)) {
					localStorage.removeItem('authToken');
					token = null;
				}

				if (StringUtils.isEmpty(token)) {
					token = await AuthenticationClient.authenticateMe();
					if (!token) return;

					localStorage.setItem('authToken', token);
				}

				request.headers.set('Authorization', `Bearer ${token}`);
			},
		],
	},
});
