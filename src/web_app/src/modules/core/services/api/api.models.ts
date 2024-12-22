export enum Role {
	Admin = 'Admin',
	SuperAdmin = 'SuperAdmin',
	Tutor = 'Tutor',
	Student = 'Student',
}

export enum ClassStatus {
	Scheduled = 'Scheduled',
	Occurred = 'Occurred',
	Paid = 'Paid',
}

export interface ItemsDto<T> {
	items: T[]
}

export interface TokenDto {
	accessToken: string;
}

interface UserBaseDto {
	id: number
    firstName: string
    lastName: string
    email: string
    timeZone: number
    locale: string
}

export interface UserDto extends UserBaseDto {
	normalizedEmail: boolean
    isActive: boolean
    isTutor: boolean
    isStudent: boolean
    isAdmin: boolean
}

export interface NewClassDto {
    time: number;
	duration: number;
}

export interface StatisticsDto {
	studentsRequests: number;
	tutorsRequests: number;
}

export interface UserRequestDto {
	id: number;
    userId: number;
    userFirstName: string;
    userLastName: number;
    userEmail: number;
    userRole: Role;
}

export enum ScheduleEventType {
	class = 'Class',
	dayOff = 'DayOff'
}

export interface ScheduleEventDto {
	id: number;
	subjectName: string;
	duration: number;
	date: number;
	type: ScheduleEventType;
	personId: number;
	personName: string;
	personTimezone: number;
	privateCourseId: number;
}

export interface ScheduleCoursePersonDto {
	privateCourseId: number
    participantId: number
    participantName: string
    participantTimezone: number
}

export interface ScheduleCourseDto {
	subjectId: number
    subjectName: string
    persons: ScheduleCoursePersonDto[]
}
