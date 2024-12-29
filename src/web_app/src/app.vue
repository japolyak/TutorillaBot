<script setup lang="ts">
import Snackbar from '@/modules/core/components/snackbar.vue';
import MainMenu from '@/modules/core/components/main-menu.vue';
import TopBar from '@/modules/core/components/top-bar.vue';
import { computed, ref } from 'vue';
import { useI18nConfig } from '@/composables/i18n-config';
import { provideDashboardLayout } from './modules/core/composables/dashboard-layout'
import { LocaleCode } from '@/plugins/i18n/i18n-plugin';

const { setLanguage } = useI18nConfig()
const mainMenuVisible = ref(false);

setLanguage(LocaleCode.enUs)

const { enableDashboardLayout } = provideDashboardLayout();

const isMacOs = computed(() => window.Telegram.WebApp.platform === 'macos');
</script>

<template>
	<v-app>
		<main-menu v-if="enableDashboardLayout" v-model="mainMenuVisible" />
		<top-bar
			v-if="enableDashboardLayout"
			:class="{ 'tg-btns-placeholder': isMacOs }"
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
