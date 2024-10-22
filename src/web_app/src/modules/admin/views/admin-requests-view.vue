<template>
	<v-container fluid>
		<v-row>
			<v-col>
				<card-tile
					:title="t('Students')"
					:button-text="t('Manage')"
					:view="View.adminRequestsRoleView"
					:params="{ role: Role.Student }"
					:component-items-count="studentsRequests"
				/>
			</v-col>
			<v-col>
				<card-tile
					:title="t('Tutors')"
					:button-text="t('Manage')"
					:view="View.adminRequestsRoleView"
					:params="{ role: Role.Tutor }"
					:component-items-count="tutorsRequests"
				/>
			</v-col>
		</v-row>
	</v-container>
</template>

<script setup lang="ts">
import { useI18n } from 'vue-i18n';
import { computed, onMounted, ref } from 'vue';
import CardTile from '@/modules/core/components/card-tile.vue';
import { View } from '@/plugins/router/view-definitions';
import { Role, type StatisticsDto } from '@/modules/core/services/api/api.models';
import { AdminClient } from '@/modules/core/services/api-clients/admin-client';
import { useActionSnackbarStore } from '@/modules/core/store/snackbar-store';

const { t } = useI18n();
const { showSnackbar } = useActionSnackbarStore();

const statistics = ref<StatisticsDto | undefined>();

const studentsRequests = computed(() => statistics.value?.studentsRequests ?? 0)
const tutorsRequests = computed(() => statistics.value?.tutorsRequests ?? 0)

async function loadStatistics() {
	const response = await AdminClient.loadRequestsStatistics();

	if (!response.isSuccess) {
		showSnackbar({
			message: response.error.message,
			status: 'error',
		});
		return;
	}

	statistics.value = response.data;
}

onMounted(async () => await loadStatistics());
</script>
