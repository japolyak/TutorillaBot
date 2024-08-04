import { httpClient } from '@/services/api/http-client';
import type { NewClassDto, Role, ClassDto, ItemsDto } from '@/services/api/api.models'
import { type KyResponse} from 'ky';

export class PrivateCourseClient {
    public static async planNewClass(privateCourseId: number, payload: NewClassDto, role: Role): Promise<KyResponse | null> {
		try {
			const request = await httpClient.post(`private-courses/${privateCourseId}/new-class/${role}/`, { json: payload });

			return request;
		} catch {
			return null;
		}
    }

	public static async getClassesByDate(privateCourseId: number, month: number, year: number): Promise<ItemsDto<ClassDto> | null> {
		try {
			const request = await httpClient.get(`private-courses/${privateCourseId}/classes/month/${month}/year/${year}/`).json<ItemsDto<ClassDto>>();

			return request;
		} catch {
			return null;
		}
    }

	public static async test(): Promise<KyResponse | null> {
		try {
			const request = await httpClient.post(`test/`, { json: { test: 'test' } });

			return request;
		}
		catch {
			return null;
		}
    }
}
