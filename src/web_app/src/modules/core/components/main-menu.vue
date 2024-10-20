<template>
    <v-navigation-drawer v-model="mainMenuVisible" location="right">
        <template #prepend>
            <v-list-item title="Tutorilla"/>
        </template>
    </v-navigation-drawer>
</template>

<script setup lang="ts">
import { onMounted } from 'vue';

const mainMenuVisible = defineModel<boolean>({ required: true, type: Boolean });

onMounted(() => {
    mainMenuVisible.value = true;
});
</script>

<style scoped lang="scss">

</style>
