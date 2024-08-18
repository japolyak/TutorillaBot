<template>
	<template v-if="!!privateCourseId">
		<date-picker @plan-class="planClass" />
		<assignment v-if="isTutorInPrivateCourse" />
		<v-btn
			v-if="isDev"
			id="debug button"
			text="Plan class"
			class="my-2"
			:color="testBtnColor"
			@click="planClass(new Date())"
		/>
	</template>
	<template v-else>
		<!--TODO-->
		Loading...
	</template>
</template>

<script setup lang="ts">
import DatePicker from '@/modules/class-planer/components/date-picker.vue';
import Assignment from '@/modules/class-planer/components/assignment.vue';
import { PrivateCourseClient } from '@/modules/core/services/api-clients/private-course-client';
import { useActionSnackbarStore } from '@/modules/core/store/snackbar-store';
import { useClassPlannerStore } from '@/modules/class-planer/services/class-planner-store';
import { useUserStore } from '@/modules/core/store/user-store';
import { useTelegramWebAppStore } from '@/modules/core/store/telegram-web-app-store';
import { onMounted, computed } from 'vue';
import { useRoute } from 'vue-router';
import { storeToRefs } from 'pinia';

const route = useRoute();

const { showSnackbar } = useActionSnackbarStore();

const { setPrivateCourse } = useUserStore();
const { isTutorInPrivateCourse, privateCourseId, userRoleInPrivateCourse } = storeToRefs(useUserStore());

const { setMainButton, setWebAppTheme } = useTelegramWebAppStore();

const { restoreClassPlanner, setFlatTextbookAssignmentsList, newClass } = useClassPlannerStore();

const isDev = computed(() => import.meta.env.VITE_APP_IS_DEV === 'true');
const testBtnColor = computed(() => window.Telegram.WebApp.colorScheme === 'light' ? 'blue' : 'green');

async function loadPrivateCourse(privateCourseId: number) {
	const response = await PrivateCourseClient.loadPrivateCourse(privateCourseId);

	if (!response.isSuccess) return;

	setPrivateCourse(response.data);
	setFlatTextbookAssignmentsList(response.data.tutorCourse.textbooks);
}

async function planClass(classDate: Date) {
	console.log("classDate - ", classDate);
	console.log("privateCourseId - ", privateCourseId.value);
	console.log("userRoleInPrivateCourse - ", userRoleInPrivateCourse.value);
    if (!privateCourseId.value || !userRoleInPrivateCourse.value) return;

    const response = await PrivateCourseClient.planNewClass(
		privateCourseId.value,
		newClass(classDate),
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
	setWebAppTheme();
	setMainButton('Plan class');

	if (Array.isArray(route.params.privateCourseId)) return;

	const privateCourseIdFromRoute = parseInt(route.params.privateCourseId);

	if (isNaN(privateCourseIdFromRoute)) return;

	await loadPrivateCourse(privateCourseIdFromRoute);
});
</script>
