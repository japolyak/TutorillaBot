import { acceptHMRUpdate, defineStore } from 'pinia';
import { computed, ref } from 'vue';
import { today, parseTime } from '@quasar/quasar-ui-qcalendar';
import type { CourseModel, ScheduleEventModel } from '@/modules/schedule/models';
import type { ScheduleEventDto } from '@/modules/core/services/api/api.models';
import { ScheduleUtils } from '@/modules/schedule/services/mappers';

export const useScheduleStore = defineStore('schedule-store', () => {
	const selectedDate = ref(today());

	const edition = ref(false);
	const isEdition = computed(() => edition.value);

	const preview = ref(false);
	const isPreview = computed(() => preview.value);

	const selectedEventId = ref<number | null>(null);
	const selectedEventDate = ref<Date | null>(null);
	const selectedEventStartsOn = ref<number | null>(null);
	const selectedEventDuration = ref<number | null>(null);

	const selectedEventChanged = computed(() => {
		if (!selectedEventId.value) return false;

		if (classDate.value?.getTime() !== selectedEventDate.value?.getTime()) return true;

		if (classStartsOn.value !== selectedEventStartsOn.value) return true;

		return classDuration.value !== selectedEventDuration.value;
	});

	const weekEvents = ref<ScheduleEventDto[]>([]);

	const eventsMap = computed(() => {
		if (!weekEvents.value?.length) return {};

		const map: Record<string, ScheduleEventModel[]> = {};

		const mappedEvents = weekEvents.value.map(ScheduleUtils.eventMapper);

		mappedEvents.forEach(event => {
			!map[event.date] ? map[event.date] = [event] : map[event.date].push(event);
		});

		return map;
	});

	function getEvents(date: string): ScheduleEventModel[] {
		// get all events for the specified date
		return eventsMap.value[date] || [];
	}

	const lastStartDay = ref<string>();
	const lastEndDay = ref<string>();

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
		classDuration.value = 60;

		edition.value = false;
		preview.value = false;

		selectedEventId.value = null;
		selectedEventDate.value = null;
		selectedEventStartsOn.value = null;
		selectedEventDuration.value = null;

		showDialog.value = true;
	}

	function setEvent(date: Date, event: ScheduleEventModel) {
		classDate.value = date;
		selectedEventDate.value = date;

		classStartsOn.value = parseTime(event.time) / 60;
		selectedEventStartsOn.value = parseTime(event.time) / 60;

		classDuration.value = event.duration;
		selectedEventDuration.value = event.duration;

		selectedPerson.value = {
			id: event.privateCourseId,
			name: event.personName,
			selected: false,
			subject: event.subjectName,
			timezone: event.personTimezone,
			disabled: false,
			type: 'person'
		};

		selectedEventId.value = event.id;
	}

	function openToEdit(date: Date, event: ScheduleEventModel) {
		setEvent(date, event);

		edition.value = true;
		preview.value = false;
		showDialog.value = true;
	}

	function openToPreview(date: Date, event: ScheduleEventModel) {
		setEvent(date, event);

		edition.value = false;
		preview.value = true;
		showDialog.value = true;
	}

	function closeDialog() {
		showDialog.value = false;
	}
	// endregion

    return {
		selectedDate,
		weekEvents,
		getEvents,
		lastStartDay,
		lastEndDay,

		showDialog,
		isSaving,
		selectedPerson,
		classDate,
		classDuration,
		classStartsOn,
		classDurations,
		openDialog,
		closeDialog,
		openToEdit,
		isEdition,
		selectedEventChanged,
		selectedEventId,
		openToPreview,
		isPreview
    };
});

if (import.meta.hot) {
    import.meta.hot.accept(acceptHMRUpdate(useScheduleStore, import.meta.hot));
}
