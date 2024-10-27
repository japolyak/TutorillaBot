import { acceptHMRUpdate, defineStore } from 'pinia';
import { ref } from 'vue';
import type { CourseModel } from '@/modules/schedule/models';

export const useScheduleStore = defineStore('schedule-store', () => {
	// region Planner dialog
	const showDialog = ref(false);
	const isSaving = ref(false);

	const selectedPerson = ref<CourseModel>();

	const classDate = ref<Date>();
	const classDuration = ref<number>(60);
	const classDurations = ref<number[]>([30, 45, 60, 75, 90]);
	const classStartsOn = ref<number>();

	function openDialog(date: Date, hour: number) {
		selectedPerson.value = undefined;
		classDate.value = date;
		classStartsOn.value = hour;

		showDialog.value = true;
	}

	function closeDialog() {
		showDialog.value = false;
	}
	// endregion

    return {

		showDialog,
		isSaving,
		selectedPerson,
		classDate,
		classDuration,
		classStartsOn,
		classDurations,
		openDialog,
		closeDialog,
    };
});

if (import.meta.hot) {
    import.meta.hot.accept(acceptHMRUpdate(useScheduleStore, import.meta.hot));
}
