<template>
	<v-container fluid>
		<v-row dense>
			<template v-for="(page, index) in adminPanelPages" :key="`admin-page-${index}`">
				<v-col cols="12">
					<v-btn
						:text="page.text"
						block
						outlined
						:to="{ name: page.view }"
					/>
				</v-col>
			</template>
		</v-row>
	</v-container>
</template>

<script setup lang="ts">
import { useI18n } from 'vue-i18n';
import { View } from '@/plugins/router/view-definitions';

const { t } = useI18n();

const adminPanelPages = [
	{
		text: t('RegistrationRequests'),
		view: View.adminPanelRequestsView
	}
];
</script>
