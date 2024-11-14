<template>
	<v-container fluid>
		<v-card v-if="requests.length">
			<v-list lines="two">
				<v-list-group v-for="request in requests" :key="`group - ${request.id}`">
					<template v-slot:activator="{ props }">
						<v-list-item
							v-bind="props"
							loading
							:title="request.userFirstName + ' ' + request.userLastName"
							:subtitle="request.userEmail"
						/>
					</template>

					<v-list-item
						:key="`accept - ${request.id}`"
						prepend-icon="mdi-account-multiple-plus-outline"
						:title="t('Accept')"
						@click="performActionOnRequest(request.id, 'accept')"
					/>

					<v-list-item
						:key="`decline - ${request.id}`"
						prepend-icon="mdi-account-multiple-remove-outline"
						:title="t('Decline')"
						@click="performActionOnRequest(request.id, 'decline')"
					/>
				</v-list-group>
			</v-list>
		</v-card>
		<v-empty-state v-else :headline="t('NoRequests')" />
	</v-container>
</template>

<script setup lang="ts">
import { useI18n } from 'vue-i18n';
import { onMounted, ref } from 'vue';
import { Role, type UserRequestDto } from '@/modules/core/services/api/api.models';
import { AdminClient } from '@/modules/core/services/api-clients/admin-client';
import { useActionSnackbarStore } from '@/modules/core/store/snackbar-store';
import { useRouter } from 'vue-router';

const { t } = useI18n();
const router = useRouter()
const { showSnackbar } = useActionSnackbarStore();

const role = ref<Role | undefined>();
const loading = ref(false);
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

async function performActionOnRequest(requestId: number, action: 'accept' | 'decline') {
	loading.value = true;

	const response = await (
		action === 'accept'
			? AdminClient.acceptRoleRequest(requestId)
			: AdminClient.declineRoleRequest(requestId)
	);

	loading.value = false;

	if (!response.isSuccess) {
			showSnackbar({
			message: response.error.message,
			status: 'error',
		});
			return;

	}

	await loadRequests();
}

onMounted(async () => {
	const roleFromRoute: Role = router.currentRoute.value.params.role;
	role.value = roleFromRoute;

	await loadRequests();
});
</script>
