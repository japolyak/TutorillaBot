<template>
    <router-view />
	<snackbar />
</template>

<script setup lang="ts">
import '@vuepic/vue-datepicker/dist/main.css';
import Snackbar from '@/modules/core/components/snackbar.vue';
</script>

<style lang="scss">
@use '@/styles/main.scss';
</style>
