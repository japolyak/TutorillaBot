

export interface CourseModel {
	id: number;
	name: string;
	selected: boolean;
	disabled: boolean;
	type: 'subject' | 'person';
	subject?: string;
    timezone?: number;
}
