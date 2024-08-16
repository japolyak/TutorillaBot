import { httpClient } from '../api/http-client';
import type { UserDto } from '@/modules/core/services/api/api.models';

export class AuthenticationClient {
    public static async validateInitData(initData: string): Promise<UserDto | null> {
		const request = httpClient.get('auth/me/', { headers: { 'Init-Data': initData } }).json<UserDto>();

		return request;
    }
}
