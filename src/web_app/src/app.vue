<script setup lang="ts">
import Snackbar from '@/modules/core/components/snackbar.vue';
import MainMenu from '@/modules/core/components/main-menu.vue';
import TopBar from '@/modules/core/components/top-bar.vue';
import { ref } from 'vue';
import { useI18nConfig } from '@/composables/i18n-config';
import { provideDashboardLayout } from './modules/core/composables/dashboard-layout'
import { LocaleCode } from '@/plugins/i18n/i18n-plugin';
import { useAppBehaviour } from '@/modules/core/composables/app-behaviour';

const { setLanguage } = useI18nConfig()
const mainMenuVisible = ref(false);

setLanguage(LocaleCode.enUs)

const { enableDashboardLayout, isMacOs } = provideDashboardLayout();
const { handleVersion } = useAppBehaviour();

handleVersion();
</script>

<template>
	<v-app>
		<main-menu v-if="enableDashboardLayout" v-model="mainMenuVisible" />
		<top-bar
			v-if="enableDashboardLayout"
			:class="{ 'btns-placeholder-margin': isMacOs }"
			@toggle-main-menu="mainMenuVisible = !mainMenuVisible"
		/>
		<div v-if="isMacOs" class="tg-header-placeholder" />
		<v-main>
			<router-view />
			<snackbar />
		</v-main>
	</v-app>
</template>

<style lang="scss">
@use '@/styles/main.scss';
@use '@quasar/quasar-ui-qcalendar/src/css/calendar-day.sass';
</style>
