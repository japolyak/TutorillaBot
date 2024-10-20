<template>
    <v-navigation-drawer v-model="mainMenuVisible" location="right">
        <template #prepend>
            <v-list-item title="Tutorilla"/>
        </template>

		<v-list nav density="compact" open-strategy="multiple" select-strategy="independent">
			<template v-for="item in mainMenu" :key="`${item.title}-group`">
				<v-list-item v-if="item.children.length === 0" :to="{ name: item.view }">
					{{ t(item.title) }}
				</v-list-item>

				<v-list-group v-else :active="item.isActive">
					<template #activator="{ props: { onClick, ...restProps }, isOpen }">
						<v-list-item
							v-bind="restProps"
							:active="item.isActive"
							@click="
								$event => openGroupItemView(item.view, item.isActive, isOpen, () => (onClick as any)($event))
							"
						>
							{{ t(item.title) }}
						</v-list-item>
					</template>
					<v-list density="compact">
						<template v-for="childView in item.children" :key="`${childView.title}-groupItem`">
							<v-list-item :to="{ name: childView.view }">
								{{ t(childView.title) }}
							</v-list-item>
						</template>
					</v-list>
				</v-list-group>
			</template>
		</v-list>
    </v-navigation-drawer>
</template>

<script setup lang="ts">
import { computed, onMounted } from 'vue';
import type { View } from '@/plugins/router/view-definitions';
import { mainMenuItems } from '@/modules/core/core.constants';
import { viewMetaDefinitions } from '@/plugins/router/view-metas';
import { useI18n } from 'vue-i18n';
import { useRouter } from 'vue-router';

interface MainMenuChildViewModel {
	view: View;
	title: string;
}

interface MainMenuGroupViewModel {
	view: View;
	icon: string;
	title: string;
	isActive: boolean;
	children: MainMenuChildViewModel[];
}

const mainMenuVisible = defineModel<boolean>({ required: true, type: Boolean });

const { t } = useI18n();

const router = useRouter();
const routes = router.getRoutes();

async function openGroupItemView(view: View, isActive: boolean, isOpen: boolean, toggleMenu: () => void) {
	await router.push({ name: view });

	if (!isActive && isOpen) return;

	toggleMenu();
}

function hasAccessToView(view: View) {
	const currentView = routes.find(x => x.name === view);
	if (!currentView) return false;

	return currentView.meta.authGuard.isAuthenticated();
}

const mainMenu = computed<MainMenuGroupViewModel[]>(() => {
	return mainMenuItems
		.filter(({ mainView }) => hasAccessToView(mainView))
		.map(({ mainView, children }) => ({
			view:mainView,
			icon: viewMetaDefinitions[mainView].icon,
			title: viewMetaDefinitions[mainView].title,
			isActive: router.currentRoute.value.name === mainView,
			children: children
				.map(childView => ({
					view: childView,
					title: viewMetaDefinitions[childView].title,
				})),
		}));
});

onMounted(() => {
    mainMenuVisible.value = false;
});
</script>

<style scoped lang="scss">

</style>
