<template>
	<v-switch v-model="setAssignment" label="Set assignment" color="primary" hide-details :class="elementTheme" />

	<template v-if="setAssignment">
		<div v-for="(item, index) in textbookAssignments" :key="index">
			<v-switch
				v-model="item.include"
				:label="item.title"
				color="primary"
				hide-details
				:class="elementTheme"
				:key="`${index}-switch`"
			/>

			<v-textarea
				v-if="item.include"
				v-model="item.description"
				variant="outlined"
				hide-details
				rows="1"
				:bg-color="textareaBgColor"
				auto-grow
				:key="`${index}-textarea`"
			/>
		</div>
	</template>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { useClassPlannerStore } from '@/modules/class-planer/services/class-planner-store';
import { useTelegramWebAppStore } from '@/modules/core/store/telegram-web-app-store';
import { storeToRefs } from 'pinia';

const { textbookAssignments, setAssignment } = storeToRefs(useClassPlannerStore());
const { applicationTheme } = storeToRefs(useTelegramWebAppStore());

const elementTheme = computed(() => applicationTheme.value === 'dark' ? 'dark-theme' : 'bright-theme');
const textareaBgColor = computed(() => applicationTheme.value === 'dark' ? '#f1f1f1' : '');
</script>


<style lang="scss">
.dark-theme {
    .v-label {
        color: #f1f1f1;
    }
}

.bright-theme {
    .v-label {
        color: #1c1c1d;
    }
}
</style>
