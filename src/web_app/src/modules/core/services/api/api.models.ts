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
	token: string;
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

export interface CourseMemberDto {
	id: number;
	firstName: string;
}

export interface SubjectDto {
	id: number;
	name: string;
}

export interface TextbookDto {
	id: number;
	title: string;
}

export interface TutorCourseDto<TUser> {
	id: number;
	tutor: TUser;
	subject: SubjectDto;
	textbooks: TextbookDto[];
	price: number | null;
}

export interface PrivateCourseDto<TUser> {
	id: number;
	tutorCourse: TutorCourseDto<TUser>;
	student: TUser;
	price: number;
}

export interface ClassDto {
    date: Date;
	status: ClassStatus;
}

export interface AssignmentDto {
    textbookId: number;
    description: string;
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
	title: string;
	duration: number;
	date: number;
	type: ScheduleEventType;
}
