<template>
	<v-container>
		<router-view v-slot="{ Component, route }">
            <component :is="Component" :key="route.path" />
        </router-view>
	</v-container>
</template>
