<template>
    <v-snackbar v-model="isVisible" timeout="3000" location="top center" :color="snackbarAnswer.color">
        {{ snackbarAnswer.text }}

        <template #actions>
            <v-icon color="white" icon="mdi-close" @click="isVisible = false" />
        </template>
    </v-snackbar>
</template>

<script setup lang="ts">
import { useActionSnackbarStore } from '@/modules/core/store/snackbar-store';
import { storeToRefs } from 'pinia';

const { isVisible, snackbarAnswer } = storeToRefs(useActionSnackbarStore());
</script>
