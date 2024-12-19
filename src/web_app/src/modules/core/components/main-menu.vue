<template>
    <v-navigation-drawer v-model="mainMenuVisible" location="right">
        <template #prepend>
			<v-list-item
				v-if="selectedParent"
				:title="selectedParent.title"
				prepend-icon="mdi-chevron-left"
				@click="selectedParent = null"
			/>
			<v-list-item v-else :title="userFullName" />
		</template>

		<v-list nav density="compact" open-strategy="multiple" select-strategy="independent">
			<template v-for="item in mainMenu" :key="`${item.title}-group`">
				<v-list-item v-if="!item.parent" :append-icon="item.appendIcon" @click="openItemView(item.view)">
					{{ t(item.title) }}
				</v-list-item>

				<v-list-group v-else :active="item.isActive">
					<template #activator="{ props: { onClick, appendIcon, ...restProps } }">
						<v-list-item
							v-bind="restProps"
							:active="item.isActive"
							:append-icon="item.appendIcon"
							@click="selectGroupItemView(item)"
						>
							{{ t(item.title) }}
						</v-list-item>
					</template>
				</v-list-group>
			</template>
		</v-list>
    </v-navigation-drawer>
</template>

<script setup lang="ts">
import { computed, onMounted, ref, watch } from 'vue';
import type { View } from '@/plugins/router/view-definitions';
import { mainMenuItems } from '@/modules/core/core.constants';
import { viewMetaDefinitions } from '@/plugins/router/view-metas';
import { useI18n } from 'vue-i18n';
import { useRouter } from 'vue-router';
import {useUserStore} from "@/modules/core/store/user-store";
import {storeToRefs} from "pinia";

interface MainMenuGroupViewModel {
	view: View;
	icon: string;
	title: string;
	isActive: boolean;
	appendIcon: 'mdi-chevron-right' | undefined;
	parent: boolean;
}

const mainMenuVisible = defineModel<boolean>({ required: true, type: Boolean });

const { t } = useI18n();
const { userFullName } = storeToRefs(useUserStore());

const router = useRouter();
const routes = router.getRoutes();

const selectedParent = ref<MainMenuGroupViewModel | null>(null);

async function openItemView(view: View) {
	await router.push({ name: view });
}

function selectGroupItemView(view: MainMenuGroupViewModel) {
	selectedParent.value = view;
}

function hasAccessToView(view: View) {
	const currentView = routes.find(x => x.name === view);

	if (!currentView) return false;

	if (currentView.meta.hidden) {
		if (import.meta.env.VITE_APP_IS_DEV !== '1') return false;
	}

	return currentView.meta.authGuard.isAuthenticated();
}

const mainMenu = computed<MainMenuGroupViewModel[]>(() => {
	const filteredItems = mainMenuItems.filter(({ mainView }) => hasAccessToView(mainView))
	if (selectedParent.value) {
		return filteredItems
			.find(({ mainView }) => selectedParent.value.view === mainView)
			?.children
			.map(childView => ({
				view: childView,
				icon: viewMetaDefinitions[childView].icon,
				title: viewMetaDefinitions[childView].title,
				isActive: router.currentRoute.value.name === childView,
				appendIcon: undefined,
				parent: false,
			}));
	}

	return filteredItems
		.map(({ mainView, children }) => ({
			view: mainView,
			icon: viewMetaDefinitions[mainView].icon,
			title: viewMetaDefinitions[mainView].title,
			isActive: router.currentRoute.value.name === mainView,
			appendIcon: !children.length ? undefined : 'mdi-chevron-right',
			parent: !!children.length,
		}));
});

onMounted(() => {
    mainMenuVisible.value = false;
});

watch(mainMenuVisible, value => {
	if (value) selectedParent.value = null;
});
</script>
