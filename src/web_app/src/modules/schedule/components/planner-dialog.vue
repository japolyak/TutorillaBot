<template>
	<v-dialog v-model="showDialog" :max-width="400" class="planner-dialog">
		<v-card class="planner-dialog">
			<v-card-title class="d-flex justify-space-between">
				{{ t('ScheduleClass') }}
				<v-btn
					icon="mdi-close"
					size="small"
					elevation="0"
					variant="text"
					density="comfortable"
					style="text-transform: none; font-weight: 400; margin-right: -17px; margin-top: -17px"
					@click="closeDialog"
				/>
			</v-card-title>

			<v-card-text>
				<v-row dense>
					<v-col cols="12">
						Student
					</v-col>
					<v-col cols="12">
						<v-autocomplete v-bind="autocompleteProps" v-model="selectedPerson">
							<template #selection="{ item }">
								{{ selectedPersonTitle(item.raw) }}
							</template>

							<template #item="{ item, props: { onClick, ...restProps } }">
								<v-list-item
									v-bind="restProps"
									:disabled="itemDisabled(item.raw)"
									class="model-list-item"
									:class="['model-list-item', { 'person': item.raw.type === 'person' }]"
									@click="
										$event => {
											setPerson(item.raw);
											() => (onClick as any)($event);
										}
									"
								/>
							</template>
						</v-autocomplete>
					</v-col>
				</v-row>

				<v-row dense>
					<v-col cols="12">
						{{ t('DateAndTime') }}
					</v-col>
					<v-col cols="12">
                        <v-select v-bind="selectDurationProps" v-model="classDuration" />
                        <div class="d-flex align-center">
                            <date-picker />
                            <v-icon icon="mdi-arrow-right" class="mx-1" />
                            <v-select v-bind="selectTimeProps" v-model="classStartsOn" max-width="110" />
                        </div>
                        <div v-if="forPersonIts" class="mt-1 d-flex align-end">
                            <v-icon icon="mdi-information-outline" size="20" />
                            <div>{{ forPersonIts }}</div>
                        </div>
					</v-col>
				</v-row>
			</v-card-text>

			<v-card-actions>
				<v-btn variant="flat" flat color="blue" block @click="planClass">
					{{ t('Plan') }}
				</v-btn>
			</v-card-actions>
		</v-card>
	</v-dialog>
</template>

<script setup lang="ts">
import { useI18n } from 'vue-i18n';
import { computed, ref } from 'vue';
import { Role } from '@/modules/core/services/api/api.models';
import DatePicker from '@/modules/schedule/components/date-picker.vue';
import { useScheduleStore } from '@/modules/schedule/services/schedule-store';
import { storeToRefs } from 'pinia';
import type { CourseModel } from '@/modules/schedule/models';
import { useUserStore } from '@/modules/core/store/user-store';
import { useDate } from 'vuetify';

const adapter = useDate();
const { t } = useI18n();
const { userTimeZone } = storeToRefs(useUserStore());
const { closeDialog } = useScheduleStore();
const {
    showDialog,
    classDate,
    classDuration,
    classDurations,
    classStartsOn,
    selectedPerson,
} = storeToRefs(useScheduleStore());

const forPersonIts = computed(() => {
    if (userTimeZone.value == null || !selectedPerson.value || !classStartsOn.value || !classDate.value) return undefined;

    const person = selectedPerson.value;
    let creatorDate = adapter.date(classDate.value);

    const hours = classStartsOn.value % 1 == 0 ? classStartsOn.value : Math.trunc(classStartsOn.value);
    const minutes = classStartsOn.value % 1 == 0 ? 0 : 30;

    creatorDate.setHours(hours, minutes);

    if (userTimeZone.value !== person.timezone){
        let offset = 3600000;

        if (userTimeZone.value > person.timezone) {
            offset *= -(userTimeZone.value - person.timezone);
        } else {
            offset *= person.timezone - userTimeZone.value;
        }

        creatorDate = new Date(creatorDate.getTime() + offset);
    }

    const weekDay = adapter.format(creatorDate, 'weekday').toLowerCase();
    const time = adapter.format(creatorDate, 'fullTime24h').slice(0, 5);

    const dayPart = weekDay + ', ' + time;

    return t('ForXItsY', [person.name, dayPart]);
});

interface PersonDto {
	id: number;
	name: string;
    timezone: number;
	role: Role.Tutor | Role.Student;
	privateCourseId: number;
}

interface CourseDto {
	id: number;
	subject: string;
	persons: PersonDto[];
}

const mockCourses: CourseDto[] = [
	{
		id: 1,
		subject: 'Math',
		persons: [
			{
				id: 1,
				name: 'Andrew',
				timezone: 2,
				role: Role.Student,
				privateCourseId: 1,
			},
			{
				id: 2,
                timezone: 3,
				name: 'Kate',
				role: Role.Student,
				privateCourseId: 2,
			}
		]
	},
	{
		id: 2,
		subject: 'Polish',
		persons: [
			{
				id: 3,
                timezone: 1,
				name: 'Irvin',
				role: Role.Student,
				privateCourseId: 3,
			},
			{
				id: 2,
                timezone: 0,
				name: 'Andrew',
				role: Role.Student,
				privateCourseId: 4,
			}
		]
	},
];

function toFlatCourseModel(
	type: 'subject' | 'person',
	id: number,
	name: string,
	subject?: string,
    timezone?: number,
	selected: boolean = false,
	disabled: boolean = false
): CourseModel {
	return { id, name, selected, subject, timezone, disabled, type };
}

const personCourses = ref<CourseDto[]>(mockCourses);

function selectedPersonTitle(item: CourseModel) {
	return `${item.subject} | ${item.name}`
}

function itemDisabled(item: CourseModel) {
	return item.disabled || (item.type === 'person' && selectedPerson.value?.id === item.id);
}

const coursesFlatList = computed(() => {
	return personCourses.value.flatMap(course => {
		const persons = course.persons.map(p => toFlatCourseModel('person', p.privateCourseId, p.name, course.subject, p.timezone));

		const subject = toFlatCourseModel('subject', course.id, course.subject, undefined, undefined, false, true);

		return [subject, ...persons];
	})
});

function planClass() {
    // add api request;
	closeDialog();
}

function setPerson(person: CourseModel) {
	selectedPerson.value = person;
}

function uniqueItemValue(model: CourseModel) {
	return `${model.id}-${model.name}`;
}

function durationTitle(value: number) {
    if (value === 1) return '1 hour';
    else if (value < 1) return t('XMinutes', [value * 60])

    return t('XHourYMinutes', [1, value % 1 * 60]);
}

function timeTitle(value: number) {
    const title = (a, b = '00') => a + ":" + b;

    return value % 1 ? title(Math.trunc(value), 30) : title(value);
}

const workHours = ref<number[]>([
    5, 5.5, 6, 6.5, 7, 7.5, 8, 8.5, 9, 9.5,
    10, 10.5, 11, 11.5, 12, 12.5, 13, 13.5, 14, 14.5,
    15, 15.5, 16, 16.5, 17, 17.5, 18, 18.5, 19, 19.5,
    20, 20.5, 21, 21.5, 22, 22.5, 23, 23.5
]);

const selectDurationProps = computed(() => ({
	hideDetails: true,
	density: 'compact' as 'compact',
	variant: 'outlined' as 'outlined',
	items: classDurations.value,
    class: 'mb-2',
    returnObject: true,
    itemTitle: durationTitle
}));

const selectTimeProps = computed(() => ({
	hideDetails: true,
	density: 'compact' as 'compact',
	variant: 'outlined' as 'outlined',
    items: workHours.value,
    returnObject: true,
    itemTitle: timeTitle
}));

const autocompleteProps = computed(() => ({
	hideDetails: true,
	clearable: true,
	returnObject: true,
	itemColor: '',
	density: 'compact' as 'compact',
	variant: 'outlined' as 'outlined',
	items: coursesFlatList.value,
	itemTitle: 'name',
	itemValue: uniqueItemValue
}));
</script>

<style lang="scss">
.v-dialog.planner-dialog {
	.v-overlay__content {
		width: 368px;

		.v-card {
			.v-card-title {
				padding: 24px 24px 8px;
			}

			.v-card-item {
				padding: 12px 12px 0 0;
			}

			.v-card-actions {
				padding: 0 24px 24px;
			}
		}
	}
}

.model-list-item {
	min-height: 24px !important;

	.v-list-item__overlay {
		opacity: 0;
	}
}

.person {
	margin-left: 20px;
}
</style>
