<template>
	<vue-date-picker
		v-model="date"
		ref="datepicker"
		:locale="locale"
		:loading="loading"
		:format="dateFormat"
		:markers="markers"
		disable-year-select
		month-name-format="long"
		placeholder="Select Date"
		@open="openPlanner"
		@closed="closePlanner"
		@update-month-year="handleMonthYear"
		@update:model-value="setTelegramMainButtonState"
	>
		<template #marker="{ marker }">
        	<span class="custom-marker" :class="marker.color" />
        </template>
		<template #marker-tooltip="{ tooltip }">
        	{{ tooltip.text }}
        </template>
		<template #calendar-header="{ index, day }">
			<div :class="index === 5 || index === 6 ? 'red-color' : ''">
				{{ day }}
			</div>
		</template>
		<template #action-row="{ internalModelValue, selectDate }">
			<div class="d-flex flex-column w-100">
				<div class="text-center mb-2">
					{{ formatDate(internalModelValue) }}
				</div>
				<div class="d-flex justify-space-between">
					<v-btn text="Cancel" min-width="97" size="small" variant="outlined" @click="closeMenu" />
					<v-btn
						text="Confirm"
						color="#2481cc"
						min-width="97"
						size="small"
						variant="flat"
						:disabled="!confirmationAllowed(internalModelValue)"
						@click="selectDate"
					/>
				</div>
			</div>
		</template>
	</vue-date-picker>
</template>

<script setup lang="ts">
import VueDatePicker, { type DatePickerMarker, type DatePickerInstance } from '@vuepic/vue-datepicker'
import { ref, watchEffect } from 'vue';
import { useUserStore } from '@/modules/core/store/user-store';
import { format } from 'date-fns'
import { type ClassDto, ClassStatus } from '@/modules/core/services/api/api.models'
import { PrivateCourseClient } from '@/modules/core/services/api-clients/private-course-client';
import { useClassPlannerStore } from '@/modules/class-planer/services/class-planner-store';
import { storeToRefs } from 'pinia';
import type { MonthYearChange } from '@/modules/class-planer/models';

defineEmits(['planClass']);

const { userTimeZone, locale, privateCourseId } = storeToRefs(useUserStore());
const { date } = storeToRefs(useClassPlannerStore());

const loading = ref(false);
const openDate = ref<Date | null>(null);
const markers = ref<DatePickerMarker[]>([]);
const dateFormat = ref('dd-MM-yyyy HH:mm');
const datepicker = ref<DatePickerInstance>(null);

async function loadClasses(month: number, year: number): Promise<ClassDto[]> {
	if (!privateCourseId.value) return [];

	loading.value = true;

	const response = await PrivateCourseClient.getClassesByDate(privateCourseId.value, month, year);

	loading.value = false;

	if (!response.isSuccess) {
		//TODO - Show snackbar
		return [];
	}

	return response.data.items;
}

const handleMonthYear = async (value: MonthYearChange) => {
	const classes = await loadClasses(value.month + 1, value.year);

	markers.value = mapToDatePickerMarker(classes);
}

const openPlanner = async () => {
	const currentDate = new Date();

	openDate.value = currentDate;

	const classes = await loadClasses(currentDate.getMonth() + 1, currentDate.getFullYear());

	markers.value = mapToDatePickerMarker(classes);
};

const closePlanner = () => {
	openDate.value = null;
	markers.value = [];
};

function mapToDatePickerMarker(data: ClassDto[]): DatePickerMarker[] {
	return data.map((day) => {
		let color = '';
		let tooltipText = '';
		const occurredAt = formatDate(day.date, 'HH:mm');

		switch (day.status) {
			case ClassStatus.Occurred:
				color = 'red';
				tooltipText = `Occurred at ${occurredAt}`;
				break;
			case ClassStatus.Scheduled:
				color = 'green';
				tooltipText = `Scheduled at ${occurredAt}`;
				break;
			case ClassStatus.Paid:
				color = 'blue';
				tooltipText = `Paid. Occurred at ${occurredAt}`;
				break;
		}

		const marker: DatePickerMarker = {
			date: day.date,
			color: color,
			tooltip: [{ text: tooltipText }]
		};

		return marker;
	});
}

const closeMenu = () => {
	datepicker.value?.closeMenu();
};

const confirmationAllowed = (value: Date | null) => {
	if (!value) return false;
	// TODO - rethink implementation
	return formatDate(value, 'HH:mm') !== formatDate(openDate.value, 'HH:mm');
};

const setTelegramMainButtonState = (): void => {
    if (date.value) {
        if (window.Telegram.WebApp.MainButton.isVisible) return;

        window.Telegram.WebApp.MainButton.show();
        return;
    }

    window.Telegram.WebApp.MainButton.hide();
};

const formatDate = (date: Date | null, datetimeFormat: string = 'dd.MM.yyyy, HH:mm') => {
	if (!date) return '';

	return format(date, datetimeFormat);
};

const planClass = (): void => {
    if (!date.value || !userTimeZone.value) return;

	const payload = new Date(Date.UTC(
		date.value.getFullYear(),
		date.value.getMonth(),
		date.value.getDate(),
		date.value.getHours() - userTimeZone.value,
		date.value.getMinutes(),
		date.value.getSeconds()
	));
};

watchEffect(() => window.Telegram.WebApp.onEvent('mainButtonClicked', planClass));
</script>

<style lang="scss">
.dp__active_date {
	background: #2481cc;
}

.dp__today {
	border: 1px solid #2481cc;
}

//.dp__action_row {
//	display: flex;
//	justify-content: space-between;
//	gap: 12px;
//	padding-inline: 13px;
//}

.red-color {
	color: red;
}

.custom-marker {
	position: absolute;
	top: 0;
	right: 0;
	height: 8px;
	width: 8px;
	border-radius: 100%;

}

.green {
	background-color: green;
}

.red {
	background-color: red;
}

.blue {
	background-color: blue;
}
</style>
