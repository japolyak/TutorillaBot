<template>
	<v-container class="pa-0">
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
