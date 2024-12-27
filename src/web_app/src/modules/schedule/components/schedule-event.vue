<template>
	<div
		v-if="timePersists"
		class="event bg-blue px-1 d-flex justify-space-between align-center"
		:style="badgeStyles(event, timeStartPos, timeDurationHeight)"
	>
		{{ event.title }}
		<v-icon :icon="eventStatusIcon" size="17" />
	</div>
</template>

<script setup lang="ts">
import { computed, type PropType } from 'vue';
import type { ScheduleEventModel } from '@/modules/schedule/models';
import { StringUtils } from '@/utils/string.utils';
import type { TimeDurationHeightFn, TimeStartPosFn } from '@/plugins/quazar/qcalendar/types';
import { ClassStatus } from '@/modules/core/services/api/api.models';

const props = defineProps({
	event: {
		type: Object as PropType<ScheduleEventModel>,
		required: true,
	},
	timeStartPos: {
		type: Function as PropType<TimeStartPosFn>,
		required: true,
	},
	timeDurationHeight: {
		type: Function as PropType<TimeDurationHeightFn>,
		required: true,
	}
});

const timePersists = computed(() => StringUtils.isNotEmpty(props.event.time));
const eventStatusIcon = computed(() => {
	if (props.event.status === ClassStatus.Paid) return 'mdi-cash-check';
	if (props.event.status === ClassStatus.Occurred) return 'mdi-cash-clock';
	return 'mdi-calendar-clock-outline';
});

function badgeStyles(event: ScheduleEventModel, timeStartPos: TimeStartPosFn, timeDurationHeight: TimeDurationHeightFn) {
	return {
		alignItems: 'flex-start',
		top: timeStartPos ? timeStartPos(event.time) + 'px' : undefined,
		height: timeDurationHeight ? timeDurationHeight(event.duration) - 5 + 'px' : undefined
	};
}
</script>

<style scoped lang="scss">
.event {
	position: absolute;
	font-size: 0.75rem;
	margin: 3px 1px 0;
	text-overflow: ellipsis;
	overflow: hidden;
	cursor: pointer;
	border-radius: 2px;
	color: white;
	left: 0;
	width: calc(100% - 2px);
}
</style>
