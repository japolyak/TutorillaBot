<template>
	<v-container>
		<v-row>
			<v-col>
				{{ theme }}
			</v-col>
			<v-col>
				<theme-toggle v-model="theme" />
			</v-col>
		</v-row>
		<v-row>
			<v-col>
				<basic-toggle />
			</v-col>
		</v-row>
		<v-row>
			<v-col cols="12">
				<v-btn text="Test button" color="primary" class="mt-4" @click="openItemView" />
			</v-col>
		</v-row>
	</v-container>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { PrivateCourseClient } from '@/modules/core/services/api-clients/private-course-client';
import { useActionSnackbarStore } from '@/modules/core/store/snackbar-store';
import ThemeToggle from "@/modules/core/components/theme-toggle.vue";
import BasicToggle from "@/modules/core/components/basic-toggle.vue";
import { useRouter } from 'vue-router';
import { View } from '@/plugins/router/view-definitions';

const theme = ref(false);

const { showSnackbar } = useActionSnackbarStore();
const router = useRouter();

async function openItemView() {
	await router.push({ name: View.classPlannerView, params: { privateCourseId: 1 } });
}

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
