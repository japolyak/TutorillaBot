import type { TextbookDto } from '@/modules/core/services/api/api.models';


export interface TextbookAssignment extends TextbookDto {
	description: string | null;
	include: boolean;
}

export interface MonthYearChange {
	instance: number;
	month: number;
	year: number;
}
