<template>
	<v-btn text="Test button" color="primary" class="mt-4" @click="sendRequest" />
</template>

<script setup lang="ts">
import { PrivateCourseClient } from '@/modules/core/services/api-clients/private-course-client';
import { useActionSnackbarStore } from '@/modules/core/store/snackbar-store';

const { showSnackbar } = useActionSnackbarStore();

const sendRequest = async () => {
	const response = await PrivateCourseClient.test();

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
};
</script>
