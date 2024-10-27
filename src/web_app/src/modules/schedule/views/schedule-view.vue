<template>
    <div class="justify center">
        <v-row dense class="mb-2">
            <v-col cols="4">
                <v-btn prepend-icon="mdi-chevron-left" :text="t('Previous')" slim min-width="100" @click="calendar?.prev()" />
            </v-col>
            <v-col cols="4">
                <v-btn :text="t('Today')" block slim @click="calendar?.moveToToday()" />
            </v-col>
            <v-col cols="4">
                <v-btn append-icon="mdi-chevron-right" :text="t('Next')" min-width="100" @click="calendar?.next()" />
            </v-col>
        </v-row>

        <div style="display: flex; max-width: 800px; width: 100%; height: 500px;">
            <q-calendar-day
                ref="calendar"
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

    <planner-dialog @planned="reload" />
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useDate } from 'vuetify';
import { useI18n } from 'vue-i18n';
import { storeToRefs } from 'pinia';
import { QCalendarDay } from '@quasar/quasar-ui-qcalendar/src/index.js'
import '@quasar/quasar-ui-qcalendar/src/QCalendarVariables.sass'
import '@quasar/quasar-ui-qcalendar/src/QCalendarTransitions.sass'
import '@quasar/quasar-ui-qcalendar/src/QCalendarDay.sass'
import PlannerDialog from '@/modules/schedule/components/planner-dialog.vue';
import ScheduleEvent from '@/modules/schedule/components/schedule-event.vue';
import { UserClient } from '@/modules/core/services/api-clients/user-client';
import { useScheduleStore } from '@/modules/schedule/services/schedule-store';
import { useUserStore } from '@/modules/core/store/user-store';
import { ScheduleUtils } from '@/modules/schedule/services/mappers';

const { t } = useI18n();
const { openDialog, getEvents } = useScheduleStore();
const { weekEvents, lastStartDay, lastEndDay, selectedDate } = storeToRefs(useScheduleStore());
const { userInfo } = storeToRefs(useUserStore());

const adapter = useDate();

const calendar = ref<QCalendarDay>();

function onClickTime({ scope }) {
    const date = adapter.parseISO(scope.timestamp.date);
    openDialog(date, scope.timestamp.hour);
}

async function onChange({start, end}) {
    if (!userInfo.value) return;

    const startDay = adapter.date(start).getTime();
    const endDay = adapter.endOfDay(adapter.date(end)).getTime();

    lastStartDay.value = start;
    lastEndDay.value = end;

    weekEvents.value = await UserClient.loadEvents(userInfo.value.id, startDay, endDay);
}

async function reload(date: number) {
    if (!lastStartDay.value || !lastEndDay.value) return;

	selectedDate.value = ScheduleUtils.toTimestamp(date).date;
	await onChange({ start: lastStartDay.value, end: lastEndDay.value });
}
</script>
