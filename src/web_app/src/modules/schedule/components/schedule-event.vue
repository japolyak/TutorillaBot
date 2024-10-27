<template>
	<div
		v-if="event.time !== undefined"
		class="my-event"
		:class="badgeClasses(event)"
		:style="badgeStyles(event, timeStartPos, timeDurationHeight)"
	>
		<span class="title q-calendar__ellipsis">
			{{ event.title }}
		</span>
	</div>
</template>

<script setup lang="ts">
defineProps({
	event: {
		type: Object,
		required: true,
	},
	timeStartPos: {
		type: Function,
		required: true,
	},
	timeDurationHeight: {
		type: Function,
		required: true,
	}
});

function badgeClasses(event) {
	return {
		['text-white bg-blue']: true,
		'full-width': (!event.side || event.side === 'full'),
		'left-side': event.side === 'left',
		'right-side': event.side === 'right',
		'rounded-border': true,
	};
}

function badgeStyles(event, timeStartPos: (time: string) => string, timeDurationHeight: (time: string) => string) {
	const s = {};

	if (timeStartPos && timeDurationHeight) {
		s.top = timeStartPos(event.time) + 'px';
		s.height = timeDurationHeight(event.duration) + 'px';
	}

	s[ 'align-items' ] = 'flex-start';
	return s;
}
</script>

<style scoped lang="scss">
.my-event {
	position: absolute;
	font-size: 12px;
	justify-content: center;
	margin: 0 1px;
	text-overflow: ellipsis;
	overflow: hidden;
	cursor: pointer;
}

.title {
	position: relative;
	display: flex;
	justify-content: center;
	align-items: center;
	height: 100%;
}

.text-white {
	color: white;
}

.bg-blue {
	background: blue;
}

.bg-green {
	background: green;
}

.bg-orange {
	background: orange;
}

.bg-red {
	background: red;
}

.bg-teal {
	background: teal;
}

.bg-grey {
	background: grey;
}

.bg-purple {
	background: purple;
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
