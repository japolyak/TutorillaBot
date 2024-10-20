import { type ComputedRef, inject, provide, computed, type InjectionKey, ref } from 'vue';
import { useRouter } from 'vue-router';
import { storeToRefs } from 'pinia';
import { useRouterStore } from '@/modules/core/store/router-store';

interface DashboardLayoutInjectable {
	setHideLayoutValue: (hide: boolean) => void;
	resetStateOnRouteLeave: () => void;
	enableDashboardLayout: ComputedRef<boolean>;
	initializing: ComputedRef<boolean>;
}

const injectable = Symbol('DashboardLayoutInjectable') as InjectionKey<DashboardLayoutInjectable>;

export function useDashboardLayout(): DashboardLayoutInjectable {
	const injectedValue = inject(injectable);
	if (!injectable) {
		throw new Error(
			'useDashboardLayout must be used within a component that has a DashboardLayout injectable provider'
		);
	}

	return injectedValue as any;
}

export function provideDashboardLayout(): DashboardLayoutInjectable {
	const forceHideLayout = ref(false);

	const router = useRouter();
	const { initializing } = storeToRefs(useRouterStore());

	const enableDashboardLayout = computed(() => {
		if (initializing.value || forceHideLayout.value) return false;

		return router.currentRoute.value.meta?.useDashboardLayout ?? false;
	});

	function setHideLayoutValue(hide: boolean) {
		forceHideLayout.value = hide;
	}

	function resetStateOnRouteLeave() {
		forceHideLayout.value = false;
	}

	const provideValue: DashboardLayoutInjectable = {
		setHideLayoutValue,
		resetStateOnRouteLeave,
		enableDashboardLayout,
		initializing: computed(() => initializing.value),
	}

	provide(injectable, provideValue);

	return provideValue;
}
