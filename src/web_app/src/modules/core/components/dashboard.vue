<template>
	hhhh
	<v-container>
		hhhh
		<router-view v-slot="{ Component, route }">
            <component :is="Component" :key="route.path" />
        </router-view>
	</v-container>
</template>
