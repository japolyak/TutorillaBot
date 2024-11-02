<template>
	<v-dialog v-model="showDialog" :max-width="400" class="align-start planner-dialog">
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
                        {{ t('Subject') + ' | ' + role }}
					</v-col>
					<v-col cols="12">
						<v-autocomplete ref="autocompleteRef" v-bind="autocompleteProps" v-model="selectedPerson">
							<template #selection="{ item }">
								{{ selectedPersonTitle(item.raw) }}
							</template>

							<template #item="{ item, props: { ...restProps } }">
								<v-list-item
									v-bind="restProps"
									:disabled="itemDisabled(item.raw)"
									class="model-list-item"
									:class="['model-list-item', { 'person': item.raw.type === 'person' }]"
									@click="setPerson(item.raw)"
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
                            <date-picker :min="minStartOn" :error="dateIsNotValid" />
                            <v-icon icon="mdi-arrow-right" class="mx-1" />
                            <v-select
                                v-bind="selectTimeProps"
                                v-model="classStartsOn"
                                max-width="110"
                                :error="dateIsNotValid"
                            />
                        </div>
                        <div v-if="forPersonIts" class="mt-4 d-flex align-end">
                            <v-icon icon="mdi-information-outline" size="20" class="mr-2" />
                            <div>{{ forPersonIts }}</div>
                        </div>
                        <div v-if="dateIsNotValid" class="mt-4 bg-red">
                            {{ t('Validators.DateFromPast') }}
                        </div>
					</v-col>
				</v-row>
			</v-card-text>

			<v-card-actions>
				<v-btn :loading="isSaving" variant="flat" block color="blue" @click="planClass">
					{{ t('Plan') }}
				</v-btn>
			</v-card-actions>
		</v-card>
	</v-dialog>
</template>

<script setup lang="ts">
import { useI18n } from 'vue-i18n';
import { useDate } from 'vuetify';
import { computed, ref } from 'vue';
import { storeToRefs } from 'pinia';
import { VAutocomplete } from 'vuetify/components';
import DatePicker from '@/modules/schedule/components/date-picker.vue';
import { useScheduleStore } from '@/modules/schedule/services/schedule-store';
import type { CourseModel } from '@/modules/schedule/models';
import { useUserStore } from '@/modules/core/store/user-store';
import { EventsClient } from '@/modules/core/services/api-clients/events-client';
import { useActionSnackbarStore } from '@/modules/core/store/snackbar-store';
import { useValidators } from '@/composables/validators';

const emit = defineEmits(['planned']);

const adapter = useDate();
const { t } = useI18n();
const { required } = useValidators();
const { showSnackbar } = useActionSnackbarStore();
const { userTimeZone, isTutor, getCourses } = storeToRefs(useUserStore());
const { closeDialog } = useScheduleStore();
const {
    showDialog,
    isSaving,
    classDate,
    classDuration,
    classDurations,
    classStartsOn,
    selectedPerson,
} = storeToRefs(useScheduleStore());

const autocompleteRef = ref<VAutocomplete | null>(null);

const role = computed(() => isTutor.value ? t('Student') : t('Tutor'));

const classDateInUnix = computed(() => {
    if (!classStartsOn.value || !classDate.value) return undefined;

    const date = new Date(classDate.value);

    const hours = classStartsOn.value % 1 == 0 ? classStartsOn.value : Math.trunc(classStartsOn.value);
    const minutes = classStartsOn.value % 1 == 0 ? 0 : 30;

    date.setHours(hours, minutes);

    return date.getTime();
});

const dateIsNotValid = computed(() => classDateInUnix.value < adapter.date()?.getTime());
const minStartOn = computed(() => adapter.toISO(adapter.endOfDay(adapter.date())));

const forPersonIts = computed(() => {
    if (userTimeZone.value == null || !classDateInUnix.value || !selectedPerson.value) return undefined;

    let creatorDateInUnix = classDateInUnix.value;
    const person = selectedPerson.value;

    if (userTimeZone.value !== person.timezone) {
        let offset = 3600000;

        if (userTimeZone.value > person.timezone) {
            offset *= -(userTimeZone.value - person.timezone);
        } else {
            offset *= person.timezone - userTimeZone.value;
        }

        creatorDateInUnix += offset;
    }

    const creatorDate = new Date(creatorDateInUnix);

    const weekDay = adapter.format(creatorDate, 'weekday').toLowerCase();
    const time = adapter.format(creatorDate, 'fullTime24h').slice(0, 5);

    const dayPart = weekDay + ', ' + time;

    return t('ForXItsY', [person.name, dayPart]);
});

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

function selectedPersonTitle(item: CourseModel) {
	return `${item.subject} | ${item.name}`
}

function itemDisabled(item: CourseModel) {
	return item.disabled || (item.type === 'person' && selectedPerson.value?.id === item.id);
}

const coursesFlatList = computed(() => {
	return getCourses.value.flatMap(course => {
		const persons = course.persons.map(p => toFlatCourseModel('person', p.privateCourseId, p.participantName, course.subjectName, p.participantTimezone));

		const subject = toFlatCourseModel('subject', course.subjectId, course.subjectName, undefined, undefined, false, true);

		return [subject, ...persons];
	})
});

async function planClass() {
    if (!selectedPerson.value || selectedPerson.value.id == null || !classDateInUnix.value || dateIsNotValid.value) {
        await autocompleteRef.value?.validate();
        return;
    }

    isSaving.value = true;

    const payload = {
        time: classDateInUnix.value,
        duration: classDuration.value,
    };

    const response = await EventsClient.planNewClass(selectedPerson.value.id, payload);

    isSaving.value = false;

	if (!response.isSuccess) {
		showSnackbar({
			message: 'Error occured:(',
			status: 'error',
		});
		return;
	}

	showSnackbar({
		message: 'Class scheduled successfully!',
		status: 'success',
	});

	closeDialog();
	emit('planned', classDateInUnix.value);
}

function setPerson(person: CourseModel) {
	selectedPerson.value = person;
    autocompleteRef.value?.blur();
}

function uniqueItemValue(model: CourseModel) {
	return `${model.id}-${model.name}`;
}

function durationTitle(value: number) {
    if (value < 60) return t('XMinutes', [value]);
    if (!(value % 60)) return t('XHour', value / 60);

    return t('XHourYMinutes', [value - 60 * Math.floor(value / 60)], Math.floor(value / 60));
}

function timeTitle(value: number) {
    const formatTime = (hours: number, minutes: string = '00') => `${hours < 10 ? '0' : ''}${hours}:${minutes}`;

    return value % 1 ? formatTime(Math.trunc(value), 30) : formatTime(value);
}

const workHours = ref<number[]>([
    0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5,
    5, 5.5, 6, 6.5, 7, 7.5, 8, 8.5, 9, 9.5,
    10, 10.5, 11, 11.5, 12, 12.5, 13, 13.5, 14, 14.5,
    15, 15.5, 16, 16.5, 17, 17.5, 18, 18.5, 19, 19.5,
    20, 20.5, 21, 21.5, 22, 22.5, 23, 23.5
]);

const selectDurationProps = computed(() => ({
    readonly: isSaving.value,
	hideDetails: true,
	density: 'compact' as 'compact',
	variant: 'outlined' as 'outlined',
	items: classDurations.value,
    class: 'mb-2',
    returnObject: true,
    itemTitle: durationTitle
}));

const selectTimeProps = computed(() => ({
    readonly: isSaving.value,
	hideDetails: true,
	density: 'compact' as 'compact',
	variant: 'outlined' as 'outlined',
    items: workHours.value,
    returnObject: true,
    itemTitle: timeTitle
}));

const autocompleteProps = computed(() => ({
    readonly: isSaving.value,
	returnObject: true,
	itemColor: '',
	density: 'compact' as 'compact',
	variant: 'outlined' as 'outlined',
	items: coursesFlatList.value,
	itemTitle: 'name',
    class: 'person-details',
	itemValue: uniqueItemValue,
    rules: [required],
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

            .v-card-text {
                padding: 16px 24px;

                .v-row.v-row--dense {
                    margin-top: 0 !important;
                }

                .person-details .v-input__details {
                    padding-inline: 0;
                    padding-top: 4px;
                }
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
