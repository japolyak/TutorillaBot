<template>
    <v-app-bar name="app-bar" class="top-bar" height="60">
        <v-app-bar-nav-icon location="right" @click="$emit('toggleMainMenu')" />
		<v-app-bar-title>{{ t('Classroom') }}</v-app-bar-title>
    </v-app-bar>
</template>

<script setup lang="ts">
import { useI18n } from 'vue-i18n';

defineEmits(['toggleMainMenu']);

const { t } = useI18n();
</script>

<style lang="scss">
.v-app-bar.top-bar {
    .v-toolbar__content {
        flex-direction: row-reverse;
    }
}
</style>
