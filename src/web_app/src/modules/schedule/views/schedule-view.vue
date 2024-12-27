<template>
	<div class="d-flex flex-column mt-1 schedule">
		<div class="d-flex justify-space-between align-center schedule-header py-2">
			<v-btn :text="t('Today')" variant="outlined" slim class="text-none" @click="moveTo" />
			{{ currentMonthPosition }}
			<v-btn-group variant="outlined" divided density="compact">
				<v-btn icon="mdi-chevron-left" @click="moveTo('prev')" />
				<v-btn icon="mdi-chevron-right" @click="moveTo('next')" />
			</v-btn-group>
		</div>
		<q-calendar-day
			ref="calendar"
			v-model="selectedDate"
			view="week"
			:cell-width="`${cellWidth}px`"
			weekday-align="right"
			:weekdays="weekdays"
			date-align="left"
			date-header="inline"
			short-weekday-label
			transition-prev=""
			transition-next=""
			animated
			bordered
			hour24-format
			@change="onChange"
			@click-time="onClickTime"
		>
			<template #day-body="{ scope: { timestamp, timeStartPos, timeDurationHeight } }">
				<template v-for="(event, index) in getEvents(timestamp.date)" :key="`event-${index}`">
					<schedule-event
						:time-duration-height="timeDurationHeight"
						:time-start-pos="timeStartPos"
						:event="event"
						@click="onEventClick(event)"
					/>
				</template>
			</template>
			<template #day-container="{ scope: { days }}">
				<template v-if="hasDate(days)">
					<div class="current-time-indicator" :style="currentTimeStyle" />
					<div class="current-time-line" :style="{ width: cellWidth + 'px', ...currentTimeStyle }" />
				</template>
			</template>
		</q-calendar-day>
	</div>

    <planner-dialog @planned="reload" />
</template>

<script setup lang="ts">
import { ref, onMounted, nextTick, onBeforeMount, onBeforeUnmount, computed } from 'vue';
import { useDate } from 'vuetify';
import { useI18n } from 'vue-i18n';
import { storeToRefs } from 'pinia';
import { useRoute, useRouter } from 'vue-router'
import {
	type QCalendarDay,
	type Timestamp,
	today,
	getEndOfWeek,
	getStartOfWeek,
	parseDate,
	diffTimestamp,
} from '@quasar/quasar-ui-qcalendar';
import '@quasar/quasar-ui-qcalendar/src/QCalendarVariables.sass';
import '@quasar/quasar-ui-qcalendar/src/QCalendarTransitions.sass';
import '@quasar/quasar-ui-qcalendar/src/QCalendarDay.sass';
import PlannerDialog from '@/modules/schedule/components/planner-dialog.vue';
import ScheduleEvent from '@/modules/schedule/components/schedule-event.vue';
import { EventsClient } from '@/modules/core/services/api-clients/events-client';
import { PrivateCourseClient } from '@/modules/core/services/api-clients/private-course-client';
import { useScheduleStore } from '@/modules/schedule/services/schedule-store';
import { useUserStore } from '@/modules/core/store/user-store';
import { ScheduleUtils } from '@/modules/schedule/services/mappers';
import { useQCalendar } from '@/composables/q-calendar';
import type { ScheduleEventModel } from '@/modules/schedule/models';

const { t } = useI18n();
const route = useRoute();
const router = useRouter();
const { openDialog, openToEdit, openToPreview, getEvents } = useScheduleStore();
const { weekEvents, lastStartDay, lastEndDay, selectedDate } = storeToRefs(useScheduleStore());
const { coursesLoaded, courses, getCourses, locale } = storeToRefs(useUserStore());
const { weekdays, getWeekBorder, getStartOfNextWeek, getStartOfPrevWeek } = useQCalendar();

const cellWidth = 120;
let intervalId: number | undefined;

const adapter = useDate();
const calendar = ref<QCalendarDay>();

const isMounted = ref(false);
const timeStartPos = ref(0);
const currentDate = ref<string | null>(null);
const currentTime = ref<string | null>(null);
const weekDay = ref<number | null>(null);

const currentTimeStyle = computed(() => {
	if (weekDay.value == null) return {};

	const base = 56;
	return {
		top: `${timeStartPos.value}px`,
		left: `${base + cellWidth * weekDay.value}px`,
	};
});

const currentMonthPosition = computed(() => {
	const date = adapter.date(selectedDate.value) as Date;
	const timeStamp = ScheduleUtils.toTimestamp(date);
	if (!timeStamp) return selectedDate.value;

	const weekStart = getStartOfWeek(timeStamp, weekdays);
	const weekEnd = getEndOfWeek(timeStamp, weekdays);

	const month = date.toLocaleString(locale.value, { month: 'short' });
	return `${weekStart.day}-${weekEnd.day} ${month}. ${timeStamp.year}`;
});

async function loadCourses() {
	if (coursesLoaded.value) return;

	const response = await PrivateCourseClient.loadPrivateCourses();

	if (response.isSuccess) {
		courses.value = response.data.items;
		coursesLoaded.value = true;
	}
}

async function onEventClick(event: ScheduleEventModel) {
	const now = adapter.date() as Date;

	const nowTimestamp = ScheduleUtils.toTimestamp(now);
	const eventTimestamp = ScheduleUtils.toTimestamp(`${event.date} ${event.time}`);
	if (!nowTimestamp || !eventTimestamp) return;

	const result = diffTimestamp(nowTimestamp, eventTimestamp, false);

	await loadCourses();

	if (!getCourses.value.length) return;

    const date = adapter.parseISO(event.date) as Date;
    result > 0 ? openToEdit(date, event) : openToPreview(date, event);
}

async function onClickTime({ scope }: { scope: { timestamp: Timestamp } }) {
	await loadCourses();

	if (!getCourses.value.length) return;

    const date = adapter.parseISO(scope.timestamp.date) as Date;
    openDialog(date, scope.timestamp.hour);
}

async function onChange({ start, end }: { start: string; end: string }) {
    const startDay = adapter.date(start).getTime();
    const endDay = adapter.endOfDay(adapter.date(end)).getTime();

    lastStartDay.value = start;
    lastEndDay.value = end;

	if (!isMounted.value) return;

    weekEvents.value = await EventsClient.loadEvents(startDay, endDay);
}

async function reload(date?: string) {
    if (!lastStartDay.value || !lastEndDay.value) return;

	if (date) selectedDate.value = date;

	await onChange({ start: lastStartDay.value, end: lastEndDay.value });
}

async function setDateDefaultPosition() {
	await nextTick(() => setTimeout(() => calendar.value?.scrollToTime('09:00', 350), 100));
}

async function moveTo(when?: 'prev' | 'next') {
	if (!calendar.value) return;

	switch (when) {
		case 'prev':
			const start = getStartOfPrevWeek(selectedDate.value);
			start ? selectedDate.value = start.date : calendar.value.next();
			break;
		case 'next':
			const end = getStartOfNextWeek(selectedDate.value);
			end ? selectedDate.value = end.date : calendar.value.next();
			break;
		default:
			calendar.value.moveToToday();
			break;
	}

	await setDateDefaultPosition();
}

function adjustCurrentTime() {
	const now = parseDate(new Date());
	if (!now) return;

	currentDate.value = now.date;
	currentTime.value = now.time;
	weekDay.value = !now.weekday ? 6 : now.weekday - 1;
	timeStartPos.value = (calendar.value?.timeStartPos(currentTime.value, false) ?? 0) + 30;
}

async function loadEvent(): Promise<string | undefined> {
	const eventId = route.query.eventId as (string | null);
	await router.replace({ path: route.path });

	if (!eventId) return undefined;

	const paramEventId = Number(eventId);
	if (Number.isNaN(paramEventId)) return;


	const response = await EventsClient.getEvent(paramEventId);
	if (!response) return;
	const event = ScheduleUtils.eventMapper(response);

	await onEventClick(event);
	return event.date;
}

function hasDate (days: Timestamp[]) {
	return currentDate.value ? days.find(day => day.date === currentDate.value) : false;
}

onBeforeMount(() => {
	selectedDate.value = getWeekBorder(new Date(), 'start')?.date ?? today();
});

onMounted(async () => {
	const loadEventDate = await loadEvent();
	let reloadDate: string | undefined;

	if (loadEventDate) {
		reloadDate = loadEventDate;
	} else {
		const dateNow = adapter.date() as Date;
		const now = ScheduleUtils.toTimestamp(dateNow);
		if (!now) return;

		reloadDate = now.date;
	}

	await setDateDefaultPosition();

	isMounted.value = true;
	await reload(reloadDate);

	adjustCurrentTime();
	intervalId = setInterval(() => adjustCurrentTime(), 60000);
});

onBeforeUnmount(() => clearInterval(intervalId));
</script>
