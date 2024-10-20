import { httpClient } from '@/modules/core/services/api/http-client';
import type { UserDto } from '@/modules/core/services/api/api.models';
import { type ApiResponse, ApiUtils } from '@/modules/core/services/api/api.utils';

export class AuthenticationClient {
    public static async validateInitData(initData: string): Promise<UserDto | null> {
		const request = httpClient.get('auth/me/', { headers: { 'Init-Data': initData }, timeout: 30000 }).json<UserDto>();
		const apiResponse = await ApiUtils.createApiResponse(request);

		return apiResponse.isSuccess ? apiResponse.data : null;
    }
}
