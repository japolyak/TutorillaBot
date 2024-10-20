import type { PluralizationRule } from 'vue-i18n';

// Documentation: https://vue-i18n.intlify.dev/guide/essentials/pluralization.html#custom-pluralization

/**
 * This function returns the index of the option in the JSON to use.
 *
 * The options in the JSON are separated by the pipe character `|`.
 *
 * Polish language should always have 4 options:
 * * index 0: for number 0
 * * index 1: for number 1
 * * index 2: for numbers ending with 2, 3 or 4 (except 12, 13 or 14)
 * * index 3: for all other numbers
 *
 * Example JSON value: `{ "XBananas": "zero bananów | jeden banan | {n} banany | {n} bananów" }`
 *
 * @param valueToCheck the number for which we want to get the correct pluralized text
 * @param choicesLength how many options are available for the specific translation
 */
export const plRules: PluralizationRule = (valueToCheck: number, choicesLength: number) => {
    const choice = Math.abs(valueToCheck);
    const maxValue = choicesLength - 1;

    if (choice === 0) return 0;
    if (choice === 1) return 1;

    // to decide which option to use, only the last two digits are important
    const lastTwoDigits = Math.abs(choice) % 100;

    // 2-4
    if (lastTwoDigits >= 2 && lastTwoDigits <= 4) return Math.min(2, maxValue);

    // 5-21
    if (lastTwoDigits <= 21) return Math.min(3, maxValue);

    const lastDigit = lastTwoDigits % 10;
    return lastDigit >= 2 && lastDigit <= 4 ? Math.min(2, maxValue) : Math.min(3, maxValue);
};
