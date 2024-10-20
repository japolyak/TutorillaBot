import { useLocale } from 'vuetify';
import { getCurrentLocaleInVuetifyFormat, setI18nLanguage, type LocaleCodeDef } from '@/plugins/i18n/i18n-plugin';


/** Provides some configurations for i18n. **/
export function useI18nConfig() {
    const { current: currentVuetifyLocale } = useLocale();

    /** Set locale */
    function setLanguage(lang: LocaleCodeDef) {
        setI18nLanguage(lang);
        currentVuetifyLocale.value = getCurrentLocaleInVuetifyFormat();
    }

    return { setLanguage };
}
