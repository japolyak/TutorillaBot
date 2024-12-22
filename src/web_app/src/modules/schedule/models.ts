import { type ScheduleEventType } from '@/modules/core/services/api/api.models';

export interface CourseModel {
	id: number;
	name: string;
	selected: boolean;
	disabled: boolean;
	type: 'subject' | 'person';
	subject?: string;
    timezone?: number;
}

export interface ScheduleEventModel {
	id: number;
	title: string;
	date: string;
	time: string;
	subjectName: string;
	duration: number;
	type: ScheduleEventType;
	side?: 'left' | 'right' | 'full';
	personName: string;
	personTimezone: number;
	privateCourseId: number;
}
