import { acceptHMRUpdate, defineStore } from 'pinia';
import { ref, computed } from 'vue';

export interface SnackbarState {
    status: SnackbarStatus;
    message: string;
}

export interface SnackbarMessage {
    color: string;
    text: string;
}

const statusColor: Record<SnackbarStatus, string> = {
    generic: '#0288d1',
    success: '#6ab846',
    error: '#c7450b',
};

type SnackbarStatus = 'generic' | 'success' | 'error';

export const useActionSnackbarStore = defineStore('action-snackbar-store', () => {
    const isVisible = ref(false);
    const snackbarMessage = ref('');
    const snackbarColor = ref('');

    const snackbarAnswer = computed(
        (): SnackbarMessage => ({ color: snackbarColor.value, text: snackbarMessage.value })
    );

    const showSnackbar = (state: SnackbarState): void => {
        isVisible.value = true;
        snackbarMessage.value = state.message;
        snackbarColor.value = statusColor[state.status];
    };

    return {
        isVisible,
        snackbarAnswer,
        showSnackbar,
    };
});

if (import.meta.hot) {
    import.meta.hot.accept(acceptHMRUpdate(useActionSnackbarStore, import.meta.hot));
}
