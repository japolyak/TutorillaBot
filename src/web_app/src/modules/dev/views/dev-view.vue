<template>
	<v-container>
		<v-row>
			<v-col>
				Must be hidden - {{ theme }}
			</v-col>
			<v-col>
				<theme-toggle v-model="theme" />
			</v-col>
		</v-row>
		<v-row>
			<v-col>
				<basic-toggle />
			</v-col>
		</v-row>
		<v-row>
			<v-col cols="12">
				<v-btn text="Test button" color="primary" class="mt-4" @click="testFn" />
			</v-col>
		</v-row>
	</v-container>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import ThemeToggle from "@/modules/core/components/theme-toggle.vue";
import BasicToggle from "@/modules/core/components/basic-toggle.vue";

const theme = ref(false);


function testFn() {
	alert("Wake up!");
}
</script>
