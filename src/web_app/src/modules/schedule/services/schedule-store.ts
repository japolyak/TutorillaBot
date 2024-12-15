import { acceptHMRUpdate, defineStore } from 'pinia';
import { computed, ref } from 'vue';
import {
	today,
	addToDate,
	isBetweenDates,
	parsed,
	parseTime,
} from '@quasar/quasar-ui-qcalendar/src/index.js'
import type { CourseModel, ScheduleEventModel } from '@/modules/schedule/models';
import type { ScheduleEventDto } from '@/modules/core/services/api/api.models';
import { ScheduleUtils } from '@/modules/schedule/services/mappers';

export const useScheduleStore = defineStore('schedule-store', () => {
	const selectedDate = ref(today());

	const weekEvents = ref<ScheduleEventDto[]>([]);

	const eventsMap = computed(() => {
		if (!weekEvents.value?.length) return {};

		const map: Record<string, ScheduleEventModel[]> = {};

		const mappedEvents = weekEvents.value.map(ScheduleUtils.eventMapper);

		mappedEvents.forEach(event => {
			!map[event.date] ? map[event.date] = [] : map[event.date].push(event);
		});

		return map;
	});

	function getEvents(date: string): ScheduleEventModel[] {
		// get all events for the specified date
		const dateEvents: ScheduleEventModel[] = eventsMap.value[date] || [];

		if (dateEvents.length === 1) dateEvents[0].side = 'full';

		else if (dateEvents.length === 2) {
			// this example does no more than 2 events per day
			// check if the two events overlap and if so, select
			// left or right side alignment to prevent overlap
			const startTime = addToDate(parsed(dateEvents[0].date), { minute: parseTime(dateEvents[0].time) });
			const endTime = addToDate(startTime, { minute: dateEvents[0].duration });
			const startTime2 = addToDate(parsed(dateEvents[1].date), { minute: parseTime(dateEvents[1].time) });
			const endTime2 = addToDate(startTime2, { minute: dateEvents[1].duration });
			if (isBetweenDates(startTime2, startTime, endTime, true) || isBetweenDates(endTime2, startTime, endTime, true)) {
				dateEvents[0].side = 'left';
				dateEvents[1].side = 'right';
			}
			else {
				dateEvents[0].side = 'full';
				dateEvents[1].side = 'full';
			}
		}

		return dateEvents;
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
    };
});

if (import.meta.hot) {
    import.meta.hot.accept(acceptHMRUpdate(useScheduleStore, import.meta.hot));
}
