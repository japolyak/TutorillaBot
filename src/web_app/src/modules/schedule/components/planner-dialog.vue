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
				<v-autocomplete v-bind="selectProps" v-model="selectedPerson">
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

const showDialog = defineModel<boolean>({ required: true, type: Boolean });

const { t } = useI18n();

interface CourseModel {
	id: number;
	name: string;
	selected: boolean;
	disabled: boolean;
	type: 'subject' | 'person';
	subject?: string;
}

interface PersonDto {
	id: number;
	name: string;
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
				role: Role.Student,
				privateCourseId: 1,
			},
			{
				id: 2,
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
				name: 'Irvin',
				role: Role.Student,
				privateCourseId: 3,
			},
			{
				id: 2,
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
	selected: boolean = false,
	disabled: boolean = false
): CourseModel {
	return { id, name, selected, subject, disabled, type };
}

const personCourses = ref<CourseDto[]>(mockCourses);
const selectedPerson = ref<CourseModel>();

function selectedPersonTitle(item: CourseModel) {
	return `${item.subject} | ${item.name}`
}

function itemDisabled(item: CourseModel) {
	return item.disabled || (item.type === 'person' && selectedPerson.value?.id === item.id);
}

const coursesFlatList = computed(() => {
	return personCourses.value.flatMap(course => {
		const persons = course.persons.map(p => toFlatCourseModel('person', p.privateCourseId, p.name, course.subject));

		const subject = toFlatCourseModel('subject', course.id, course.subject, undefined, false, true);

		return [subject, ...persons];
	})
});

function closeDialog() {
	showDialog.value = false;
}

function planClass() {
	closeDialog()
}

function setPerson(person: CourseModel) {
	selectedPerson.value = person;
}

function uniqueItemValue(model: CourseModel) {
	return `${model.id}-${model.name}`;
}

const selectProps = computed(() => ({
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
