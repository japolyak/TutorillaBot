import { acceptHMRUpdate, defineStore } from 'pinia';
import { ref, computed } from 'vue';
import { type UserDto } from '@/services/api/api.models';


export const useUserStore = defineStore('user-store', () => {
	const user = ref<UserDto | null>(null);

	const userInfo = computed(() => user.value);
	const isTutor = computed(() => user.value?.is_tutor ?? false);
	const userTimeZone = computed(() => user.value?.time_zone ?? null);
	const locale = computed(() => user.value?.locale ?? 'en-US');

	const setUser = (payload: UserDto | null) => {
		if (payload == null) {
			user.value = null;
			return;
		}

		user.value = payload;
	}

    return {
		isTutor,
		userInfo,
		locale,
		userTimeZone,
		setUser,
    };
});

if (import.meta.hot) {
    import.meta.hot.accept(acceptHMRUpdate(useUserStore, import.meta.hot));
}
