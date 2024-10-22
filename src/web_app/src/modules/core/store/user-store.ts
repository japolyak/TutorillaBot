import { acceptHMRUpdate, defineStore } from 'pinia';
import { computed, ref } from 'vue';
import type { CourseMemberDto, PrivateCourseDto, UserDto } from '@/modules/core/services/api/api.models';
import { Role } from '@/modules/core/services/api/api.models';


export const useUserStore = defineStore('user-store', () => {
	const user = ref<UserDto | null>(null);

	const userFullName = computed(() => {
		if (!user.value) return 'Tutorilla';

		return user.value.firstName + ' ' + user.value.lastName;
	});

	const userRoles = computed(() => {
		const roles: Role[] = []

		if (!user.value) return roles;

		if (user.value.isTutor) roles.push(Role.Tutor);
		if (user.value.isStudent) roles.push(Role.Student);
		if (user.value.isAdmin) roles.push(Role.Admin);

		return roles;
	});

	const privateCourse = ref<PrivateCourseDto<CourseMemberDto> | null>(null);

	const privateCourseId = computed(() => privateCourse.value?.id ?? null);

	const userRoleInPrivateCourse = computed(() => {
		if (!user.value || !privateCourse.value) return null;

		if (privateCourse.value.student.id === user.value.id) return Role.Student;
		if (privateCourse.value.tutorCourse.tutor.id === user.value.id) return Role.Tutor;

		return null;
	});

	const isTutorInPrivateCourse = computed(() => (userRoleInPrivateCourse.value === Role.Tutor));

	const userInfo = computed(() => user.value);
	const userTimeZone = computed(() => user.value?.timeZone ?? null);
	const locale = computed(() => user.value?.locale ?? 'en-US');

	function setUser(payload: UserDto) {
		user.value = payload;
	}

	function setPrivateCourse(payload: PrivateCourseDto<CourseMemberDto>) {
		privateCourse.value = payload;
	}

	function hasRoles(...roles: Role[]): boolean {
		if (!roles.length) return true;

		return !userRoles.value.length ? false : !!userRoles.value.filter(r => roles.includes(r));
	}

    return {
		privateCourse,
		privateCourseId,
		userRoleInPrivateCourse,
		isTutorInPrivateCourse,
		userInfo,
		locale,
		userFullName,
		userTimeZone,
		setUser,
		setPrivateCourse,
		hasRoles,
    };
});

if (import.meta.hot) {
    import.meta.hot.accept(acceptHMRUpdate(useUserStore, import.meta.hot));
}
