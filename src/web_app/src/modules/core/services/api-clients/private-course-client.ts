import { httpClient } from '@/modules/core/services/api/http-client';
import type { ScheduleCourseDto, ItemsDto } from '@/modules/core/services/api/api.models'
import { type ApiResponse, ApiUtils } from '@/modules/core/services/api/api.utils';

export class PrivateCourseClient {
	private static readonly urlBase = 'private-courses';

	public static async loadPrivateCourses(): Promise<ApiResponse<ItemsDto<ScheduleCourseDto>>> {
		const url = `${this.urlBase}/`;

		const request = httpClient.get(url).json<ItemsDto<ScheduleCourseDto>>();
		return await ApiUtils.createApiResponse(request);
	}

	public static async test(): Promise<ApiResponse<any>> {
		const request = httpClient.post(`test/`, { json: { test: 'test' } });

		return await ApiUtils.createApiResponse(request)
    }
}
