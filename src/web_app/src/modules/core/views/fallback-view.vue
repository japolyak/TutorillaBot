<template>
	fallback view
</template>

<script setup lang="ts">
import { useDashboardLayout } from '@/modules/core/composables/dashboard-layout';

const { setHideLayoutValue } = useDashboardLayout();
setHideLayoutValue(true);
</script>

<style scoped lang="scss">

</style>
