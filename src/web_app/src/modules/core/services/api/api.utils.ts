import { HTTPError } from 'ky';

export interface SuccessResponse<T> {
	readonly isSuccess: true;
	readonly data: T;
}

export interface FailedResponse {
	readonly isSuccess: false;
	readonly error: HTTPError;
}

export type ApiResponse<T> = SuccessResponse<T> | FailedResponse;

export class ApiUtils {
	public static async createApiResponse<T>(request: Promise<T>): Promise<ApiResponse<T>> {
		let data: T | null = null;
		let error: HTTPError | null = null;

		await request
			.then(t => (data = t))
			.catch((e: HTTPError) => {
				// TODO - reimplement
				error = e;
			});

		return error ? { isSuccess: false, error } : { isSuccess: true, data: data as T };
	}
}
