<template>
    <v-app-bar name="app-bar" class="top-bar" height="60">
        <v-app-bar-nav-icon location="right" @click="$emit('toggleMainMenu')" />
		<v-app-bar-title>
			<v-breadcrumbs v-if="breadcrumbs != null" :items="breadcrumbs" />
		</v-app-bar-title>
    </v-app-bar>
</template>

<script setup lang="ts">
import { useI18n } from 'vue-i18n';
import { useRouter } from 'vue-router';
import { computed } from 'vue';
import type { View } from '@/plugins/router/view-definitions';
import {viewBreadcrumbDefinitions} from '@/plugins/router/view-breadcrumbs';

defineEmits(['toggleMainMenu']);

const { t } = useI18n();
const router = useRouter();

const breadcrumbs = computed(() => {
	const view = router.currentRoute.value.name as View;

	const foundBreadCrumbs = viewBreadcrumbDefinitions[view];
	if (!foundBreadCrumbs) return null;

	return foundBreadCrumbs.map(item => {
		if (typeof item === 'string') return t(item);

		const title = item.titleArguments && item.titleArguments.length
			? t(item.title, item.titleArguments)
			: t(item.title);

		return {
			...item,
			title,
		};
	});
});
</script>

<style lang="scss">
.v-app-bar.top-bar {
    .v-toolbar__content {
        flex-direction: row-reverse;
    }
}
</style>
