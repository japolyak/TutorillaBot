import { httpClient } from '@/modules/core/services/api/http-client';
import type { ItemsDto, NewClassDto, ScheduleEventDto } from '@/modules/core/services/api/api.models';
import { type ApiResponse, ApiUtils } from '@/modules/core/services/api/api.utils';

export class EventsClient {
	private static readonly urlBase = 'events';

    public static async loadEvents(start: number, end: number): Promise<ScheduleEventDto[]> {
		const url = `${this.urlBase}/start/${start}/end/${end}/`

		const request = httpClient.get(url).json<ItemsDto<ScheduleEventDto>>();
		const apiResponse = await ApiUtils.createApiResponse(request);

		return apiResponse.isSuccess ? apiResponse.data.items : [];
    }

	public static async planNewClass(privateCourseId: number, payload: NewClassDto): Promise<ApiResponse<any>> {
		const url = `${this.urlBase}/class/courses/${privateCourseId}/`;

		const request = httpClient.post(url, { json: payload });
		return await ApiUtils.createApiResponse(request);
    }

	public static async getEvent(eventId: number): Promise<ScheduleEventDto | null> {
		const url = `${this.urlBase}/${eventId}/`;

		const request = httpClient.get(url).json<ScheduleEventDto | null>();
		const apiResponse = await ApiUtils.createApiResponse(request);

		return apiResponse.isSuccess ? apiResponse.data : null
	}

	public static async rescheduleEvent(eventId: number, payload: NewClassDto): Promise<ApiResponse<any>> {
		const url = `${this.urlBase}/${eventId}/`;

		const request = httpClient.patch(url, { json: payload });
		return await ApiUtils.createApiResponse(request);
    }

	public static async deleteEvent(eventId: number): Promise<ApiResponse<any>> {
		const url = `${this.urlBase}/${eventId}/`;

		const request = httpClient.delete(url);
		return await ApiUtils.createApiResponse(request);
    }
}
