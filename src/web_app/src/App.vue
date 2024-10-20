<script setup lang="ts">
import '@vuepic/vue-datepicker/dist/main.css';
import Snackbar from '@/modules/core/components/snackbar.vue';
import MainMenu from '@/modules/core/components/main-menu.vue';
import TopBar from '@/modules/core/components/top-bar.vue';
import { ref } from 'vue';
import { useI18nConfig } from '@/composables/i18n-config';

const { setLanguage } = useI18nConfig()
const mainMenuVisible = ref(false);

setLanguage('en-US')
</script>

<template>
	<v-app>
		<main-menu v-model="mainMenuVisible" />
		<top-bar @toggle-main-menu="mainMenuVisible = !mainMenuVisible"/>
		<v-main>
			<router-view />
			<snackbar />
		</v-main>
	</v-app>
</template>

<style lang="scss">
@use '@/styles/main.scss';
</style>
