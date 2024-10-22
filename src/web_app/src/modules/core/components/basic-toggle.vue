<template>
	{{ lightTheme }}
	<div
		:class="['toggle-switch', { 'is-checked': lightTheme }]"
		@click="toggle"
	>
		<div :class="['toggle-thumb', { 'is-checked': lightTheme }]" />
	</div>
</template>

<script setup lang="ts">
import { ref } from 'vue';

const lightTheme = ref(true);

const emit = defineEmits(['update:modelValue']);

function toggle() {
  emit('update:modelValue', !lightTheme.value);
  lightTheme.value = !lightTheme.value;
}
</script>

<style scoped lang="scss">
.toggle-switch {
	width: 56px;
	height: 32px;
	background-color: #202020;
	border: 3px solid #484848;
	border-radius: 16px;
	position: relative;
	cursor: pointer;
	transition: all .1s cubic-bezier(0.250, 0.460, 0.450, 0.940);

	&.is-checked {
		background-color: #c0e6f6;
		border-color: #81c0d5;
	}

	.toggle-thumb {
		width: 22px;
		height: 22px;
		background-color: #fffdf2;
		border: 3px solid #dee1c5;
		border-radius: 50px;
		position: absolute;
		top: 2px;
		left: 26px;
		transition: all .1s cubic-bezier(0.250, 0.460, 0.450, 0.940);

		&.is-checked {
			left: 2px;
			background-color: #f5fb42;
			border-color: #e4c74d;
		}
	}
}
</style>
