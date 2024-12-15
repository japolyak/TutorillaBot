<template>
	<div
		v-if="timePersists"
		class="my-event text-white bg-blue rounded-border"
		:class="badgeClasses(event)"
		:style="badgeStyles(event, timeStartPos, timeDurationHeight)"
	>
		<span class="title q-calendar__ellipsis">
			{{ event.title }}
		</span>
	</div>
</template>

<script setup lang="ts">
import { type PropType, computed } from 'vue';
import type { ScheduleEventModel } from '@/modules/schedule/models';
import { StringUtils } from '@/utils/string.utils';
import type { TimeDurationHeightFn, TimeStartPosFn } from '@/plugins/quazar/qcalendar/types';

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

function badgeClasses(event: ScheduleEventModel) {
	return {
		'full-width': (!event.side || event.side === 'full'),
		'left-side': event.side === 'left',
		'right-side': event.side === 'right',
	};
}

function badgeStyles(event: ScheduleEventModel, timeStartPos: TimeStartPosFn, timeDurationHeight: TimeDurationHeightFn) {
	return {
		alignItems: 'flex-start',
		top: timeStartPos ? timeStartPos(event.time) + 'px' : undefined,
		height: timeDurationHeight ? timeDurationHeight(event.duration) - 5 + 'px' : undefined
	};
}
</script>

<style scoped lang="scss">
.my-event {
	position: absolute;
	font-size: 12px;
	justify-content: center;
	margin: 3px 1px 0;
	text-overflow: ellipsis;
	overflow: hidden;
	cursor: pointer;
}

.title {
	position: relative;
	display: flex;
	justify-content: center;
	align-items: center;
	height: 90%;
}

.text-white {
	color: white;
}

.bg-blue {
	background: blue;
}

.full-width {
	left: 0;
	width: calc(100% - 2px);
}

.left-side {
	left: 0;
	width: calc(50% - 3px);
}

.right-side {
	left: 50%;
	width: calc(50% - 3px);
}

.rounded-border {
	border-radius: 2px;
}
</style>
