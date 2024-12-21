<template>
    <div class="justify center">
        <v-row dense class="mb-2">
            <v-col cols="4">
                <v-btn prepend-icon="mdi-chevron-left" :text="t('Previous')" slim min-width="100" @click="moveTo('prev')" />
            </v-col>
            <v-col cols="4">
                <v-btn :text="t('Today')" block slim @click="moveTo" />
            </v-col>
            <v-col cols="4">
                <v-btn append-icon="mdi-chevron-right" :text="t('Next')" min-width="100" @click="moveTo('next')" />
            </v-col>
        </v-row>

        <div style="display: flex; max-width: 800px; width: 100%; height: 500px;">
            <q-calendar-day
                ref="calendar"
                v-model="selectedDate"
                view="week"
                cell-width="120px"
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
                            @click="console.log(event)"
                        />
                    </template>
                </template>
            </q-calendar-day>
        </div>
    </div>
	<div class="d-flex flex-column mt-1 schedule">
		<div class="d-flex justify-space-between align-center schedule-header py-2">
			<v-btn :text="t('Today')" variant="outlined" slim @click="moveTo" class="today-btn" />
			{{ currentMonthPosition }}
			<v-btn-group variant="outlined" divided density="compact" class="nav-group">
				<v-btn icon="mdi-chevron-left" class="nav-btn" @click="moveTo('prev')" />
				<v-btn icon="mdi-chevron-right" class="nav-btn" @click="moveTo('next')" />
			</v-btn-group>
		</div>
		<q-calendar-day
			ref="calendar"
			v-model="selectedDate"
			view="week"
			cell-width="120px"
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
						@click="console.log(event)"
					/>
				</template>
			</template>
		</q-calendar-day>
	</div>

    <planner-dialog @planned="reload" />
</template>

<script setup lang="ts">
import { ref, onMounted, nextTick, onBeforeMount, computed } from 'vue';
import { useDate } from 'vuetify';
import { useI18n } from 'vue-i18n';
import { storeToRefs } from 'pinia';
import { type QCalendarDay, type Timestamp, today, getEndOfWeek, getStartOfWeek } from '@quasar/quasar-ui-qcalendar';
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

const { t } = useI18n();
const { openDialog, getEvents } = useScheduleStore();
const { weekEvents, lastStartDay, lastEndDay, selectedDate } = storeToRefs(useScheduleStore());
const { coursesLoaded, courses, getCourses } = storeToRefs(useUserStore());
const { weekdays, getWeekBorder, getStartOfNextWeek, getStartOfPrevWeek } = useQCalendar();

const adapter = useDate();

const calendar = ref<QCalendarDay>();
const isMounted = ref(false);

const currentMonthPosition = computed(() => {
	const date = new Date(selectedDate.value);
	const timeStamp = ScheduleUtils.toTimestamp(date);
	if (!timeStamp) return '';

	const weekStart = getStartOfWeek(timeStamp, weekdays);
	const weekEnd = getEndOfWeek(timeStamp, weekdays);

	const month = date.toLocaleString('default', { month: 'short' });
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

async function onClickTime({ scope }: { scope: { timestamp: Timestamp } }) {
	await loadCourses();

	if (!getCourses.value.length) return;

    const date = adapter.parseISO(scope.timestamp.date);
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

async function reload(date: number) {
    if (!lastStartDay.value || !lastEndDay.value) return;

	selectedDate.value = ScheduleUtils.toTimestamp(date).date;
	await onChange({ start: lastStartDay.value, end: lastEndDay.value });
}

function moveTo(when?: 'prev' | 'next') {
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

	nextTick(() => {
		setTimeout(() => (calendar.value?.scrollToTime('09:00', 350)), 100);
	});
}

onBeforeMount(() => {
	selectedDate.value = getWeekBorder(new Date(), 'start')?.date ?? today();
});

onMounted(async () => {
	const dateNow = adapter.date() as Date;
	const now = ScheduleUtils.toTimestamp(dateNow);
	if (!now) return;

	selectedDate.value = now.date

	await nextTick(() => {
		setTimeout(() => {
			calendar.value?.scrollToTime(`${now.hour - 3}:${now.minute}`, 350);
		}, 100);
	});

	isMounted.value = true;
	await reload(dateNow.getTime());
});
</script>

<style lang="scss">
.schedule {
	max-width: 800px;
	width: 100%;
	height: 580px;

	.schedule-header {
		font-size: 1rem;
		font-weight: 600;
		color: #606c71;
		padding-inline: 11px;

		.today-btn {
			border: #e0e0e0 thin solid;
		}

		.nav-group {
			border-color: #e0e0e0;

			.nav-btn {
				width: 40px;
				color: #606c71;
			}
		}
	}
}
</style>
