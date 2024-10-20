<template>
	<v-container fluid>
		requests by role
	</v-container>
</template>

<script setup lang="ts">
import CardTile from '@/modules/core/components/card-tile.vue';
import { useI18n } from 'vue-i18n';
import { View } from '@/plugins/router/view-definitions';

const { t } = useI18n();
</script>

<style scoped lang="scss">

</style>
