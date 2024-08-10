<template>
	<v-switch v-model="setAssignment" label="Set assignment" color="primary" hide-details :class="elementTheme" />

	<template v-if="setAssignment">
		<div v-for="(item, index) in items" :key="index">
			<v-switch
				v-model="item.include"
				:label="item.title"
				color="primary"
				hide-details
				:class="elementTheme"
				:key="`${index}-switch`"
				@update:modelValue="!item.include ? item.value = null : null"
			/>
			<v-textarea
				v-if="item.include"
				v-model="item.value"
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
import { ref, computed, type PropType } from 'vue';

const props = defineProps({
    applicationTheme: {
        type: String as PropType<string | null>,
        default: null,
    },
});

interface Item {
    title: string;
    value: string | null;
    include: boolean;
}

const setAssignment = ref(false);

const items = ref<Array<Item>>([
    { title: 'Hurra 1', value: null, include: false },
    { title: 'Hurra 2', value: null, include: false },
    { title: 'Hurra 3', value: null, include: false },
    { title: 'Czas na czasownik', value: null, include: false },
    { title: 'Umiesz zdasz', value: null, include: false },
    { title: 'Megatest', value: null, include: false },
    { title: 'Dodatkowe', value: null, include: false },
]);

const elementTheme = computed(() => props.applicationTheme === 'dark' ? 'dark-theme' : 'bright-theme');
const textareaBgColor = computed(() => props.applicationTheme === 'dark' ? '#f1f1f1' : '');

const resetAssignment = () => {
    setAssignment.value = false;
    items.value.forEach((item: Item) => {
        item.value = null;
        item.include = false;
    });
};

defineExpose({ resetAssignment, setAssignment, items });
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
