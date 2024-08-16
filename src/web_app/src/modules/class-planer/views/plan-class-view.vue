<template>
    <date-picker @plan-class="planClass" />
	<assignment v-if="isTutorInPrivateCourse" ref="assignmentRef" :application-theme="applicationTheme" />
</template>

<script setup lang="ts">
import DatePicker from '@/modules/class-planer/components/date-picker.vue';
import Assignment from '@/modules/class-planer/components/assignment.vue';
import { PrivateCourseClient } from '@/modules/core/services/api-clients/private-course-client';
import { useActionSnackbarStore } from '@/modules/core/store/snackbar-store';
import { useClassPlannerStore } from '@/modules/class-planer/services/class-planner-store';
import { useUserStore } from '@/modules/core/store/user-store';
import { onMounted, ref } from 'vue';
import { useRoute } from 'vue-router';
import { storeToRefs } from 'pinia';

const route = useRoute();

const { showSnackbar } = useActionSnackbarStore();

const { isTutorInPrivateCourse, privateCourseId, userRoleInPrivateCourse } = storeToRefs(useUserStore());
const { setPrivateCourse } = useUserStore();

const { newClass } = storeToRefs(useClassPlannerStore());
const { restoreClassPlanner, setFlatTextbookAssignmentsList } = useClassPlannerStore();

const applicationTheme = ref<string | null>(null);
const assignmentRef = ref<InstanceType<typeof Assignment> | null>(null);

async function loadPrivateCourse(privateCourseId: number) {
	const response = await PrivateCourseClient.loadPrivateCourse(privateCourseId);

	if (!response.isSuccess) return;

	setPrivateCourse(response.data);
	setFlatTextbookAssignmentsList(response.data.textbooks);
}

async function planClass() {
    if (!privateCourseId.value || !userRoleInPrivateCourse.value) return;

    const response = await PrivateCourseClient.planNewClass(
		privateCourseId.value,
		newClass.value,
		userRoleInPrivateCourse.value,
	);

	if (!response.isSuccess) {
		showSnackbar({
			message: 'Error occurred',
			status: 'error',
		});
		return;
	}

	showSnackbar({
		message: 'Class scheduled successfully!',
		status: 'success',
	});

	restoreClassPlanner(isTutorInPrivateCourse.value);

	window.Telegram.WebApp.MainButton.hide();
}

onMounted(async () => {
    applicationTheme.value = window.Telegram.WebApp.themeParams.secondary_bg_color === '#1c1c1d' ? 'dark' : 'bright';
	window.Telegram.WebApp.MainButton.text = 'Plan class';

	if (Array.isArray(route.params.privateCourseId)) return;

	const privateCourseIdFromRoute = parseInt(route.params.privateCourseId);

	if (isNaN(privateCourseIdFromRoute)) return;

	await loadPrivateCourse(privateCourseIdFromRoute);
});
</script>
