<template>
    <div class="justify center">
        <div style="display: flex; max-width: 800px; width: 100%; height: 500px;">
            <q-calendar-day
                v-model="selectedDate"
                view="week"
                cell-width="120px"
                weekday-align="right"
                date-align="left"
                date-header="inline"
                short-weekday-label
                animated
                bordered
                hour24-format
                @change="onChange"
                @moved="onMoved"
                @click-date="onClickDate"
                @click-time="onClickTime"
                @click-interval="onClickInterval"
                @click-head-intervals="onClickHeadIntervals"
                @click-head-day="onClickHeadDay"
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
    <planner-dialog />
</template>

<script setup lang="ts">
import { computed, ref } from 'vue';
import { useDate } from 'vuetify';
import {
    addToDate,
    isBetweenDates,
    parsed,
    parseTime,
    parseTimestamp,
    QCalendarDay,
    today,
    parseDate,
} from '@quasar/quasar-ui-qcalendar/src/index.js'
import '@quasar/quasar-ui-qcalendar/src/QCalendarVariables.sass'
import '@quasar/quasar-ui-qcalendar/src/QCalendarTransitions.sass'
import '@quasar/quasar-ui-qcalendar/src/QCalendarDay.sass'
import PlannerDialog from '@/modules/schedule/components/planner-dialog.vue';
import ScheduleEvent from '@/modules/schedule/components/schedule-event.vue';
import { useScheduleStore } from '@/modules/schedule/services/schedule-store';
import { EventType, type ScheduleEventModel } from '@/modules/schedule/models';

const { openDialog } = useScheduleStore();

const adapter = useDate();

const selectedDate = ref(today());
const calendar = ref<QCalendarDay | null>(null);

function getCurrentDay(day: number) {
    const newDay = new Date(new Date())
    newDay.setDate(day)
    const tm = parseDate(newDay)
    return tm.date;
}

const events = computed(() => {
    const even: ScheduleEventModel[] = [
        {
            id: 1,
            title: 'Polish',
            date: getCurrentDay(27),
            time: '10:00',
            duration: 120,
            type: EventType.class
        },
        {
            id: 2,
            title: 'Polish',
            date: getCurrentDay(27),
            time: '12:30',
            duration: 90,
            type: EventType.class
        },
        {
            id: 3,
            title: 'Polish',
            date: getCurrentDay(27),
            time: '14:30',
            duration: 60,
            type: EventType.class
        },
    ];

    return even;
});

const eventsMap = computed(() => {
    const map = {};
    // this.events.forEach(event => (map[ event.date ] = map[ event.date ] || []).push(event))
    events.value.forEach(event => {
        if (!map[ event.date ]) map[ event.date ] = [];

        map[ event.date ].push(event);

        if (event.days) {
            let timestamp = parseTimestamp(event.date);
            let days = event.days;
            do {
                timestamp = addToDate(timestamp, { day: 1 });
                if (!map[ timestamp.date ]) map[ timestamp.date ] = [];
                map[ timestamp.date ].push(event);
            } while (--days > 0)
        }
    });

    return map;
});

function getEvents(date: string) {
    // get all events for the specified date
    const dateEvents = eventsMap.value[date] || [];

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

function onClickTime({ scope }) {
    const date = adapter.parseISO(scope.timestamp.date);
    openDialog(date, scope.timestamp.hour);
}

// region Clicks
function onMoved(data: any) {
    console.log('onMoved', data);
}

function onChange(data: any) {
    console.log('onChange', data);
}

function onClickDate(data: any) {
    console.log('onClickDate', data);
}

function onClickInterval(data: any) {
    console.log('onClickInterval', data);
}

function onClickHeadIntervals(data: any) {
    console.log('onClickHeadIntervals', data);
}

function onClickHeadDay(data: any) {
    console.log('onClickHeadDay', data);
}
// endregion
</script>
