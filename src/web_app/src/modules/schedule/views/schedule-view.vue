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
                @change="onChange"
                @moved="onMoved"
                @click-date="onClickDate"
                @click-time="onClickTime"
                @click-interval="onClickInterval"
                @click-head-intervals="onClickHeadIntervals"
                @click-head-day="onClickHeadDay"
            />
        </div>
    </div>
    <planner-dialog />
</template>

<script setup lang="ts">
import { QCalendarDay, today } from '@quasar/quasar-ui-qcalendar/src/index.js'
import '@quasar/quasar-ui-qcalendar/src/QCalendarVariables.sass'
import '@quasar/quasar-ui-qcalendar/src/QCalendarTransitions.sass'
import '@quasar/quasar-ui-qcalendar/src/QCalendarDay.sass'
import { ref } from 'vue';
import PlannerDialog from "@/modules/schedule/components/planner-dialog.vue";
import { useScheduleStore } from '@/modules/schedule/services/schedule-store';
import { useDate } from 'vuetify';

const { openDialog } = useScheduleStore();

const adapter = useDate();

const selectedDate = ref(today());
const calendar = ref<QCalendarDay | null>(null);

function onMoved(data: any) {
    console.log('onMoved', data);
}

function onChange(data: any) {
    console.log('onChange', data);
}

function onClickDate(data: any) {
    console.log('onClickDate', data);
}

function onClickTime({ scope }) {
    console.log(scope);
    const date = adapter.parseISO(scope.timestamp.date);
    openDialog(date, scope.timestamp.hour);
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
</script>
