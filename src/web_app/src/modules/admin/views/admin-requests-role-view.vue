<template>
	<v-container fluid>
		requests {{ requests }}
	</v-container>
</template>

<script setup lang="ts">
import { useI18n } from 'vue-i18n';
import { onMounted, ref } from 'vue';
import { Role, UserRequestDto } from '@/modules/core/services/api/api.models';
import { AdminClient } from '@/modules/core/services/api-clients/admin-client';
import { useActionSnackbarStore } from '@/modules/core/store/snackbar-store';
import { useRouter } from 'vue-router';

const { t } = useI18n();
const router = useRouter()
const { showSnackbar } = useActionSnackbarStore();

const role = ref<Role | undefined>();

const requests = ref<UserRequestDto[]>([]);

async function loadRequests() {
	if (!role.value) return;

	const response = await AdminClient.loadRequestsByRole(role.value);

	if (!response.isSuccess) {
		showSnackbar({
			message: response.error.message,
			status: 'error',
		});
		return;
	}

	requests.value = response.data.items;
}

onMounted(async () => {
	const roleFromRoute: Role = router.currentRoute.value.params.role;
	role.value = roleFromRoute;

	await loadRequests()
});
</script>
