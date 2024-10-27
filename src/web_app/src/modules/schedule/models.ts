export interface CourseModel {
	id: number;
	name: string;
	selected: boolean;
	disabled: boolean;
	type: 'subject' | 'person';
	subject?: string;
    timezone?: number;
}

export enum EventType {
	class = 'Class',
	dayOff = 'DayOff'
}

export interface ScheduleEventModel {
	id: number;
	title: string;
	date: string;
	time: string;
	duration: number;
	type: EventType;
}
