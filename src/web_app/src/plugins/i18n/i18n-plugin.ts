import type { LocaleMessage } from '@intlify/core-base';
import { createI18n as originalCreateI18n, type I18n } from 'vue-i18n';
import { enFormats, plFormats, type CmplDateTimeFormats } from './datetime-formats';
import { defaultTranslationMessages } from './i18n-constants';
import { plRules } from './pluralization-rules';
import { VuetifyUtils } from '@/utils/vuetify.utils';

// problem with enums in libraries: https://www.typescriptlang.org/docs/handbook/enums.html#objects-vs-enums
export const LocaleCode = {
    enUs: 'en-US',
    plPL: 'pl-PL',
} as const;

export type LocaleCodeDef = (typeof LocaleCode)[keyof typeof LocaleCode];

interface I18nCache {
    i18n: I18n<Record<string, LocaleMessage>, CmplDateTimeFormats, Record<string, unknown>, string, false> | null;
    localStorageKey: string;
    defaultLangCode: LocaleCodeDef;
    fallbackLangCode: LocaleCodeDef;
    setLanguageCallback: ((newLocale: LocaleCodeDef) => void) | null;
}

const allowedLangCodes: LocaleCodeDef[] = [LocaleCode.enUs, LocaleCode.plPL];

const i18nCache: I18nCache = {
    i18n: null,
    defaultLangCode: LocaleCode.plPL,
    fallbackLangCode: LocaleCode.enUs,
    localStorageKey: 'i18n_locale',
    setLanguageCallback: null,
};

/** Returns the i18n instance if it was initialized. To be used only inside this library. */
export function getGlobalI18n() {
    return i18nCache.i18n!.global;
}

/** Initialized the vue-i18n plugin to be used with our library. */
export function createI18n(
    messages: Record<string, LocaleMessage> = {},
    localStorageKey = 'i18n_locale',
    defaultLangCode: LocaleCodeDef = LocaleCode.plPL,
    fallbackLangCode: LocaleCodeDef = LocaleCode.enUs,
    recreate = false,
    setLanguageCallback: ((newLocale: LocaleCodeDef) => void) | null = null
): I18n<Record<string, LocaleMessage>, CmplDateTimeFormats, Record<string, unknown>, string, false> {
    if (i18nCache.i18n != null && !recreate) return i18nCache.i18n;

    i18nCache.defaultLangCode = defaultLangCode;
    i18nCache.fallbackLangCode = fallbackLangCode;
    i18nCache.localStorageKey = localStorageKey;
    i18nCache.setLanguageCallback = setLanguageCallback;

    let selectedLang = localStorage.getItem(localStorageKey) as LocaleCodeDef;
    if (!allowedLangCodes.includes(selectedLang)) selectedLang = defaultLangCode;

    i18nCache.i18n = originalCreateI18n({
        legacy: false,
        locale: selectedLang,
        fallbackLocale: fallbackLangCode,
        globalInjection: true,
        messages: VuetifyUtils.mergeDeep(defaultTranslationMessages, messages),
        pluralRules: {
            [LocaleCode.plPL]: plRules,
        },
        datetimeFormats: {
            [LocaleCode.enUs]: enFormats,
            [LocaleCode.plPL]: plFormats,
        },
    });

    setI18nLanguage(selectedLang);
    return i18nCache.i18n;
}

/** Set language and saves it in the local storage */
export function setI18nLanguage(locale: LocaleCodeDef) {
    if (i18nCache.i18n == null) return;

    i18nCache.i18n.global.locale.value = locale;
    window?.document?.querySelector('html')?.setAttribute('lang', locale);
    localStorage.setItem(i18nCache.localStorageKey, locale);
    i18nCache.setLanguageCallback?.(locale);
}

/** Convert the currently used language to the one's that vuetify understand */
export function getCurrentLocaleInVuetifyFormat() {
    const currentLang = i18nCache.i18n?.global.locale.value ?? i18nCache.defaultLangCode;
    switch (currentLang) {
        case LocaleCode.enUs:
            return 'en';
        case LocaleCode.plPL:
            return 'pl';
    }

    return 'en';
}
