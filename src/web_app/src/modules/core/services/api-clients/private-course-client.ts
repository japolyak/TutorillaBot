import { httpClient } from '@/modules/core/services/api/http-client';
import type {
	NewClassDto,
	Role,
	ClassDto,
	ItemsDto,
	PrivateCourseDto,
	CourseMemberDto,
} from '@/modules/core/services/api/api.models'
import { type ApiResponse, ApiUtils } from '@/modules/core/services/api/api.utils';

export class PrivateCourseClient {
	private static readonly urlBase = 'private-courses';

	public static async loadPrivateCourse(privateCourseId: number): Promise<ApiResponse<PrivateCourseDto<CourseMemberDto>>> {
		const url = `${this.urlBase}/${privateCourseId}/`;

		const request = httpClient.get(url).json<PrivateCourseDto<CourseMemberDto>>();
		return  await ApiUtils.createApiResponse(request);
	}

    public static async planNewClass(privateCourseId: number, payload: NewClassDto): Promise<ApiResponse<any>> {
		const url = `${this.urlBase}/${privateCourseId}/new-class/`;

		const request = httpClient.post(url, { json: payload });
		return await ApiUtils.createApiResponse(request);
    }

	public static async getClassesByDate(privateCourseId: number, month: number, year: number): Promise<ApiResponse<ItemsDto<ClassDto>>> {
		const url = `${this.urlBase}/${privateCourseId}/classes/month/${month}/year/${year}/`;

		const request = httpClient.get(url).json<ItemsDto<ClassDto>>();
		return await ApiUtils.createApiResponse(request);
    }

	public static async test(): Promise<ApiResponse<any>> {
		const request = httpClient.post(`test/`, { json: { test: 'test' } });

		return await ApiUtils.createApiResponse(request)
    }
}
