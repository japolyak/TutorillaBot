import { acceptHMRUpdate, defineStore } from 'pinia';
import { ref, computed } from 'vue';
import type { UserDto, PrivateCourseDto, CourseMemberDto } from '@/modules/core/services/api/api.models';
import { Role } from '@/modules/core/services/api/api.models';


export const useUserStore = defineStore('user-store', () => {
	const user = ref<UserDto | null>(null);
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

	function setUser(payload: UserDto | null) {
		if (payload == null) {
			user.value = null;
			return;
		}

		user.value = payload;
	}

	function setPrivateCourse(payload: PrivateCourseDto<CourseMemberDto>) {
		privateCourse.value = payload;
	}

    return {
		privateCourse,
		privateCourseId,
		userRoleInPrivateCourse,
		isTutorInPrivateCourse,
		userInfo,
		locale,
		userTimeZone,
		setUser,
		setPrivateCourse,
    };
});

if (import.meta.hot) {
    import.meta.hot.accept(acceptHMRUpdate(useUserStore, import.meta.hot));
}
