import { acceptHMRUpdate, defineStore } from 'pinia';
import { computed, ref } from 'vue';
import type { UserDto, ScheduleCourseDto } from '@/modules/core/services/api/api.models';
import { Role } from '@/modules/core/services/api/api.models';


export const useUserStore = defineStore('user-store', () => {
	const user = ref<UserDto | null>(null);

	const isTutor = computed(() => user.value?.isTutor ?? false);
	const isStudent = computed(() => user.value?.isStudent ?? false);
	const isAdmin = computed(() => user.value?.isAdmin ?? false);
	const hasAdminRole = computed(() => isStudent.value);

	const userFullName = computed(() => {
		if (!user.value) return 'Tutorilla';

		return user.value.firstName + ' ' + user.value.lastName;
	});

	const userRoles = computed(() => {
		const roles: Role[] = []

		if (!user.value) return roles;

		if (isTutor.value) roles.push(Role.Tutor);
		if (isStudent.value) roles.push(Role.Student);
		if (user.value.isAdmin) roles.push(Role.Admin);

		return roles;
	});

	const userInfo = computed(() => user.value);
	const userTimeZone = computed(() => user.value?.timeZone ?? null);
	const locale = computed(() => user.value?.locale ?? 'en-US');

	const coursesLoaded = ref(false);

	const courses = ref<ScheduleCourseDto[]>([]);
	const getCourses = computed(() => courses.value);

	function setUser(payload: UserDto) {
		user.value = payload;
	}

	function hasRoles(...roles: Role[]): boolean {
		if (!roles.length) return true;

		return !userRoles.value.length ? false : !!userRoles.value.filter(r => roles.includes(r));
	}

    return {
		userInfo,
		isTutor,
		isStudent,
		locale,
		userFullName,
		userTimeZone,
		setUser,
		hasRoles,
		coursesLoaded,
		courses,
		getCourses,
    };
});

if (import.meta.hot) {
    import.meta.hot.accept(acceptHMRUpdate(useUserStore, import.meta.hot));
}
