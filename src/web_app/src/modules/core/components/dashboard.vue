<template>
	<v-container class="pa-0 d-flex main-container">
		<router-view v-slot="{ Component, route }">
            <component :is="Component" :key="route.path" />
        </router-view>
	</v-container>
</template>

<script setup lang="ts">
import { onBeforeRouteLeave } from 'vue-router';
import { useDashboardLayout } from '@/modules/core/composables/dashboard-layout';

const { resetStateOnRouteLeave } = useDashboardLayout();
onBeforeRouteLeave((to, from) => resetStateOnRouteLeave());
</script>

<style lang="scss">
.main-container {
	display: flex;
	justify-content: center;
	max-width: 100% !important;
}
</style>
