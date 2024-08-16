export enum Role {
	Admin = 'Admin',
	Tutor = 'Tutor',
	Student = 'Student',
}

export enum ClassStatus {
	Scheduled = 'scheduled',
	Occurred = 'occurred',
	Paid = 'paid',
}

export interface ItemsDto<T> {
	items: T[]
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

export interface TutorCourseDto {
	id: number;
	subject: SubjectDto;
	tutor: CourseMemberDto;
	price: number | null;
}

export interface PrivateCourseDto {
	id: number;
	tutorCourse: TutorCourseDto;
	student: CourseMemberDto;
	textbooks: TextbookDto[];
	price: number;
}

export interface ClassDto {
    date: Date;
	status: ClassStatus;
}

export interface AssignmentDto {
    textbookId: number;
    description: string | null;
}

export interface NewClassDto {
    date: Date;
    assignments: AssignmentDto[];
}
