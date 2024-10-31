import { httpClient } from '@/modules/core/services/api/http-client';
import type {
	PrivateCourseDto,
	CourseMemberDto,
} from '@/modules/core/services/api/api.models'
import { type ApiResponse, ApiUtils } from '@/modules/core/services/api/api.utils';

export class PrivateCourseClient {
	private static readonly urlBase = 'private-courses';

	public static async loadPrivateCourse(privateCourseId: number): Promise<ApiResponse<PrivateCourseDto<CourseMemberDto>>> {
		const url = `${this.urlBase}/${privateCourseId}/`;

		const request = httpClient.get(url).json<PrivateCourseDto<CourseMemberDto>>();
		return await ApiUtils.createApiResponse(request);
	}

	public static async test(): Promise<ApiResponse<any>> {
		const request = httpClient.post(`test/`, { json: { test: 'test' } });

		return await ApiUtils.createApiResponse(request)
    }
}
