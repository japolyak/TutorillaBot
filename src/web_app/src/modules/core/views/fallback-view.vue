<template>
	<v-empty-state :headline="t('NotTodayBuddy')" title="Very sad:(" icon="mdi-alert-outline" />
</template>

<script setup lang="ts">
import { useDashboardLayout } from '@/modules/core/composables/dashboard-layout';
import { useI18n } from 'vue-i18n';

const { setHideLayoutValue } = useDashboardLayout();
const { t } = useI18n();

setHideLayoutValue(true);
</script>
