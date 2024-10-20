<template>
	<v-container fluid>
		<v-row>
			<v-col>
				<card-tile
					:title="t('Students')"
					:button-text="t('Manage')"
					:view="View.adminRequestsRoleView"
					:params="{ role: Role.Student }"
				/>
			</v-col>
			<v-col>
				<card-tile
					:title="t('Tutors')"
					:button-text="t('Manage')"
					:view="View.adminRequestsRoleView"
					:params="{ role: Role.Tutor }"
				/>
			</v-col>
		</v-row>
	</v-container>
</template>

<script setup lang="ts">
import CardTile from '@/modules/core/components/card-tile.vue';
import { useI18n } from 'vue-i18n';
import { View } from '@/plugins/router/view-definitions';
import { Role } from '@/modules/core/services/api/api.models';

const { t } = useI18n();
</script>

<style scoped lang="scss">

</style>
