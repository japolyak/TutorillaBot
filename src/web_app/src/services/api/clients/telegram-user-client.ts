import { httpClient } from '../http-client';
import type { UserDto } from '@/services/api/api.models';

export class TelegramUserClient{
    public static async validateInitData(initData: string): Promise<UserDto | null> {
		const request = httpClient.get('auth/me/', {headers: {'Init-Data': initData}}).json<UserDto>();

		return request;
    }
}
