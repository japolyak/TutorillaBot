import { httpClient } from '@/modules/core/services/api/http-client';
import type { UserDto } from '@/modules/core/services/api/api.models';
import { ApiUtils } from '@/modules/core/services/api/api.utils';

export class UserClient {
	private static readonly urlBase = 'users';

	public static async getMe(): Promise<UserDto | null> {
		const url = `${this.urlBase}/me/`;

		const request = httpClient.get(url).json<UserDto>();
		const apiResponse = await ApiUtils.createApiResponse(request);

		return apiResponse.isSuccess ? apiResponse.data : null;
    }
}
