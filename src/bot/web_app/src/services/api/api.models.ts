export enum Role {
	admin = 'admin',
	tutor = 'tutor',
	student = 'student',
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
    first_name: string
    last_name: string
    email: string
    time_zone: number
    locale: string
}

export interface UserDto extends UserBaseDto {
	normalized_email: boolean
    is_active: boolean
    is_tutor: boolean
    is_student: boolean
    is_admin: boolean
}

export interface SourceDto {
    title: string;
    assignment: string;
}

export interface NewClassDto {
    date: Date;
    sources: SourceDto[];
}

export interface ClassDto {
    date: Date;
	status: ClassStatus;
}
