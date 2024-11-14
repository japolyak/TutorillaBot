import { httpClient } from '@/modules/core/services/api/http-client';
import type { StatisticsDto, UserRequestDto, Role, ItemsDto } from '@/modules/core/services/api/api.models'
import { type ApiResponse, ApiUtils } from '@/modules/core/services/api/api.utils';

export class AdminClient {
	private static readonly urlBase = 'admin';

	public static async loadRequestsStatistics(): Promise<ApiResponse<StatisticsDto>> {
		const url = `${this.urlBase}/requests-statistics/`;
		const request = httpClient.get(url).json<StatisticsDto>();

		return await ApiUtils.createApiResponse(request);
	}

	public static async loadRequestsByRole(role: Role): Promise<ApiResponse<ItemsDto<UserRequestDto>>> {
		const url = `${this.urlBase}/role-requests/${role}/`;
		const request = httpClient.get(url).json<ItemsDto<UserRequestDto>>();

		return await ApiUtils.createApiResponse(request);
	}

	public static async acceptRoleRequest(requestId: number): Promise<ApiResponse<any>> {
		const url = `${this.urlBase}/role-requests/${requestId}/accept/`;
		const request = httpClient.put(url);

		return await ApiUtils.createApiResponse(request);
	}

	public static async declineRoleRequest(requestId: number): Promise<ApiResponse<any>> {
		const url = `${this.urlBase}/role-requests/${requestId}/decline/`;
		const request = httpClient.put(url);

		return await ApiUtils.createApiResponse(request);
	}
}
