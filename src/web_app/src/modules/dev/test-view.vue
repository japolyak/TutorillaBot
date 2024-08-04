<template>
	<v-btn text="Test button" color="primary" class="mt-4" @click="sendRequest" />
</template>

<script setup lang="ts">
import { PrivateCourseClient } from '@/services/api/clients/private-course-client';
import { useActionSnackbarStore } from '@/stores/snackbar-store';

const { showSnackbar } = useActionSnackbarStore();

const sendRequest = async () => {
	const response = await PrivateCourseClient.test();

	if (response?.status !== 200) {
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
