import { httpClient } from '@/modules/core/services/api/http-client';
import type { NewClassDto, Role, ClassDto, ItemsDto, PrivateCourseDto } from '@/modules/core/services/api/api.models'
import { type KyResponse} from 'ky';

export class PrivateCourseClient {
	private static readonly urlBase = 'private-courses';

	public static async loadPrivateCourse(privateCourseId: number): Promise<PrivateCourseDto | null> {
		const url = `${this.urlBase}/${privateCourseId}/`;

		try {
			return await httpClient.get(url).json<PrivateCourseDto>();
		} catch {
			return null;
		}
	}

    public static async planNewClass(privateCourseId: number, payload: NewClassDto, role: Role): Promise<KyResponse | null> {
		const url = `${this.urlBase}/${privateCourseId}/new-class/${role}/`;

		try {
			return await httpClient.post(url, { json: payload });
		} catch {
			return null;
		}
    }

	public static async getClassesByDate(privateCourseId: number, month: number, year: number): Promise<ItemsDto<ClassDto> | null> {
		const url = `${this.urlBase}/${privateCourseId}/classes/month/${month}/year/${year}/`;

		try {
			return await httpClient.get(url).json<ItemsDto<ClassDto>>();
		} catch {
			return null;
		}
    }

	public static async test(): Promise<KyResponse | null> {
		try {
			return await httpClient.post(`test/`, { json: { test: 'test' } });
		}
		catch {
			return null;
		}
    }
}
