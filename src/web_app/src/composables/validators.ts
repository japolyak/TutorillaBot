import { toValue, type ComputedRef, type MaybeRefOrGetter } from 'vue';
import { useDate } from 'vuetify';
import type { ValidationResult, ValidationRuleFn } from '../plugins/vuetify/models';
import { NumberUtils } from '../utils/number.utils';
import { StringUtils } from '../utils/string.utils';
import { useI18n } from 'vue-i18n';

type MaybeRefOrGetterOrComputedRef<T = any> = ComputedRef<T> | MaybeRefOrGetter<T>;

export interface CoreValidators {
    required: ValidationRuleFn;
    requireDigit: ValidationRuleFn;
    requireNonAlphanumeric: ValidationRuleFn;
    requireLowercase: ValidationRuleFn;
    requireUppercase: ValidationRuleFn;
    requireUniqueCharacters: (uniqueCharactersRequired: number) => ValidationRuleFn;
    email: (allowEmpty?: boolean) => ValidationRuleFn;
    minArrayLength: (minLength: number) => ValidationRuleFn;
    minLength: (minLength: number, allowEmpty?: boolean) => ValidationRuleFn;
    maxLength: (maxLength: number) => ValidationRuleFn;
    length: (minLength: number | null, maxLength: number | null, allowEmpty?: boolean) => ValidationRuleFn;
    number: (allowEmpty?: boolean) => ValidationRuleFn;
    integer: (allowEmpty?: boolean) => ValidationRuleFn;
    greaterThan: (valueToCompare: number, inclusive: boolean, allowEmpty?: boolean) => ValidationRuleFn;
    lowerThan: (valueToCompare: number, inclusive: boolean, allowEmpty?: boolean) => ValidationRuleFn;
    regex: (regex: RegExp, allowedCharacters: string, allowEmpty?: boolean) => ValidationRuleFn;
    uniqueItems: (existingItems: MaybeRefOrGetterOrComputedRef<any[]>, caseSensitive?: boolean) => ValidationRuleFn;
    date: (
        minIsoDate: string | null | undefined,
        maxIsoDate: string | null | undefined,
        allowEmpty?: boolean
    ) => ValidationRuleFn;
    time: (allowEmpty?: boolean) => ValidationRuleFn;
}

/** Creates specific validators */
export function useValidators(): CoreValidators {
    const { t } = useI18n();
    const adapter = useDate();

    /** At least one digit must be present in the provided value */
    function requireDigitValidator(value: any): ValidationResult {
        const stringValue = StringUtils.valueToString(value);
        for (const c of stringValue) {
            if (StringUtils.isDigit(c)) return true;
        }

        return t(i => i.validators.requireDigitValidator);
    }

    /** At least one special character (non letter/digit character) must be present in the value */
    function requireNonAlphanumericValidator(value: any): ValidationResult {
        const stringValue = StringUtils.valueToString(value);
        for (const c of stringValue) {
            if (!StringUtils.isLetterOrDigit(c)) return true;
        }

        return t(i => i.validators.requireNonAlphanumericValidator);
    }

    /** At least one lowercase character must be present in the value */
    function requireLowercaseValidator(value: any): ValidationResult {
        const stringValue = StringUtils.valueToString(value);
        for (const c of stringValue) {
            if (StringUtils.isLowercase(c)) return true;
        }

        return t(i => i.validators.requireLowercaseValidator);
    }

    /** At least one uppercase character must be present in the value */
    function requireUppercaseValidator(value: any): ValidationResult {
        const stringValue = StringUtils.valueToString(value);
        for (const c of stringValue) {
            if (StringUtils.isUppercase(c)) return true;
        }

        return t(i => i.validators.requireUppercaseValidator);
    }

    /** Specified number of unique characters must be present in the value */
    function requireUniqueCharactersValidator(value: any, uniqueCharactersRequired: number): ValidationResult {
        if (uniqueCharactersRequired <= 0) {
            throw new Error(
                `Invalid arguments for requireUniqueCharacters validator. Values { uniqueCharactersRequired: ${uniqueCharactersRequired} (min: 1) }`
            );
        }

        const stringValue = StringUtils.valueToString(value);
        const uniqueCharacters = new Set<string>();

        for (const c of stringValue) {
            uniqueCharacters.add(c);
            if (uniqueCharacters.size >= uniqueCharactersRequired) return true;
        }

        return t(i => i.validators.requireUniqueCharactersValidator, uniqueCharactersRequired);
    }

    /** Provided value must be a valid email address */
    function emailValidator(value: any, allowEmpty: boolean): ValidationResult {
        const stringValue = StringUtils.valueToString(value);

        const isEmpty = StringUtils.isEmpty(stringValue);
        if (allowEmpty && isEmpty) return true;

        const index = stringValue.indexOf('@');

        // it must contain only one @ character and it must not be the first or the last character
        const isValidEmail = index > 0 && index < stringValue.length - 1 && index === stringValue.lastIndexOf('@');
        return isValidEmail || t(i => i.validators.emailValidator);
    }

    /** Provided value must not be null or empty (doesn't work on arrays) */
    function requiredValidator(value: any): ValidationResult {
        const stringValue = StringUtils.valueToString(value);
        return stringValue.length > 0 || t('Validators.RequiredValidator');
    }

    /** Provided value must have the minimum length */
    function minLengthValidator(value: any, minLength: number | null, allowEmpty: boolean): ValidationResult {
        if (minLength == null || minLength < 0) {
            const minLen = minLength ?? 'null';
            throw new Error(`Invalid arguments for minLength validator. Values { minLength: ${minLen} }`);
        }

        const stringValue = StringUtils.valueToString(value);
        if (allowEmpty && StringUtils.isEmpty(stringValue)) return true;

        return stringValue.length >= minLength || t(i => i.validators.minLengthValidator, [minLength]);
    }

    /** Provided value must have the maximum length */
    function maxLengthValidator(value: any, maxLength: number | null): ValidationResult {
        if (maxLength == null || maxLength < 0) {
            const maxLen = maxLength ?? 'null';
            throw new Error(`Invalid arguments for maxLength validator. Values { maxLength: ${maxLen} }`);
        }

        const stringValue = StringUtils.valueToString(value);
        return stringValue.length <= maxLength || t(i => i.validators.maxLengthValidator, [maxLength]);
    }

    /** Provided value must have the minimum and maximum length */
    function lengthValidator(
        value: any,
        minLength: number | null,
        maxLength: number | null,
        allowEmpty: boolean
    ): ValidationResult {
        if (
            (minLength == null && maxLength == null) ||
            (minLength != null && minLength < 0) ||
            (maxLength != null && maxLength < 0) ||
            (minLength != null && maxLength != null && minLength > maxLength)
        ) {
            const minLen = minLength ?? 'null';
            const maxLen = maxLength ?? 'null';

            throw new Error(
                `Invalid arguments for length validator. Values { minLength: ${minLen}; maxLength: ${maxLen} }`
            );
        }

        const stringValue = StringUtils.valueToString(value);
        if (allowEmpty && StringUtils.isEmpty(stringValue)) return true;

        if (minLength == null) return maxLengthValidator(value, maxLength);
        if (maxLength == null) return minLengthValidator(value, minLength, false);

        if (minLength <= stringValue.length && stringValue.length <= maxLength) return true;

        return minLength === maxLength
            ? t(i => i.validators.exactLengthValidator, minLength)
            : t(i => i.validators.lengthValidator, [minLength, maxLength]);
    }

    /** Provided array must have the minimum number of items */
    function minArrayLengthValidator(value: any, minLength: number | null): ValidationResult {
        if (minLength == null || minLength < 0) {
            const minLen = minLength ?? 'null';
            throw new Error(`Invalid arguments for minArrayLength validator. Values { minLength: ${minLen} }`);
        }

        const arrayValue = value == null || !Array.isArray(value) ? [] : value;
        if (arrayValue.length >= minLength) return true;

        if (minLength === 1) return t(i => i.validators.requiredValidator);
        return t(i => i.validators.minArrayLengthValidator, [minLength]);
    }

    /**
     * Provided value must be a number.
     *
     * If returned `true` and the value is not empty, then it is safe to cast the value to number.
     **/
    function numberValidator(value: any, allowEmpty: boolean): ValidationResult {
        const stringValue = StringUtils.valueToString(value);

        const isEmpty = StringUtils.isEmpty(stringValue);
        if (allowEmpty && isEmpty) return true;

        return (!isEmpty && NumberUtils.isNumber(stringValue)) || t(i => i.validators.numberValidator);
    }

    /**
     * Provided value must be an integer.
     *
     * If returned `true` and the value is not empty, then it is safe to cast the value to number.
     **/
    function integerValidator(value: any, allowEmpty: boolean): ValidationResult {
        const stringValue = StringUtils.valueToString(value);

        const isEmpty = StringUtils.isEmpty(stringValue);
        if (allowEmpty && isEmpty) return true;

        return (!isEmpty && NumberUtils.isInteger(stringValue)) || t(i => i.validators.integerValidator);
    }

    /**
     * Provided value is greater than the valueToCompare.
     *
     * @param value value being validated
     * @param valueToCompare value to compare with
     * @param inclusive if true, then the value can be equal to the valueToCompare
     * @param allowEmpty if true, then empty values are considered valid
     * @returns true if the value is greater than the valueToCompare and value can be safely cast to number.
     **/
    function greaterThanValidator(
        value: any,
        valueToCompare: number,
        inclusive: boolean,
        allowEmpty: boolean
    ): ValidationResult {
        const stringValue = StringUtils.valueToString(value);

        const isEmpty = StringUtils.isEmpty(stringValue);
        if (allowEmpty && isEmpty) return true;

        if (!isEmpty && numberValidator(value, false) === true) {
            const parsedValue = parseFloat(stringValue);

            if (inclusive) {
                return (
                    parsedValue >= valueToCompare ||
                    t(i => i.validators.greaterThanInclusiveValidator, [valueToCompare])
                );
            }

            return parsedValue > valueToCompare || t(i => i.validators.greaterThanValidator, [valueToCompare]);
        }

        return inclusive
            ? t(i => i.validators.greaterThanInclusiveValidator, [valueToCompare])
            : t(i => i.validators.greaterThanValidator, [valueToCompare]);
    }

    /**
     * Provided value is lower than the valueToCompare.
     *
     * @param value value being validated
     * @param valueToCompare value to compare with
     * @param inclusive if true, then the value can be equal to the valueToCompare
     * @param allowEmpty if true, then empty values are considered valid
     * @returns true if the value is lower than the valueToCompare and value can be safely cast to number.
     **/
    function lowerThanValidator(
        value: any,
        valueToCompare: number,
        inclusive: boolean,
        allowEmpty: boolean
    ): ValidationResult {
        const stringValue = StringUtils.valueToString(value);

        const isEmpty = StringUtils.isEmpty(stringValue);
        if (allowEmpty && isEmpty) return true;

        if (!isEmpty && numberValidator(value, false) === true) {
            const parsedValue = parseFloat(stringValue);

            if (inclusive) {
                return (
                    parsedValue <= valueToCompare || t(i => i.validators.lowerThanInclusiveValidator, [valueToCompare])
                );
            }

            return parsedValue < valueToCompare || t(i => i.validators.lowerThanValidator, [valueToCompare]);
        }

        return inclusive
            ? t(i => i.validators.lowerThanInclusiveValidator, [valueToCompare])
            : t(i => i.validators.lowerThanValidator, [valueToCompare]);
    }

    /**
     * Verify that the provided value matches the provided regex.
     */
    function regexValidator(
        value: any,
        regex: RegExp,
        allowedCharacters: string,
        allowEmpty: boolean
    ): ValidationResult {
        const stringValue = StringUtils.valueToString(value);

        const isEmpty = StringUtils.isEmpty(stringValue);
        if (allowEmpty && isEmpty) return true;

        return (!isEmpty && regex.test(stringValue)) || t(i => i.validators.regexValidator, [allowedCharacters]);
    }

    /**
     * Verify that the provided value exists in the provided array.
     */
    function uniqueItemsValidator(
        value: any,
        existingItems: MaybeRefOrGetterOrComputedRef<any[]>,
        caseSensitive: boolean
    ): ValidationResult {
        let items = toValue(existingItems);

        value = StringUtils.valueToString(value);
        items = items.map((i: any) => StringUtils.valueToString(i));

        if (!caseSensitive) {
            value = value.toUpperCase();
            items = items.map((i: any) => i.toUpperCase());
        }

        return !items.includes(value) || t(i => i.validators.uniqueItemsValidator);
    }

    const formatDate = (val: Date) => adapter.format(val, 'keyboardDate');

    /**
     * Verify that the provided value is a correct date string in the current locale.
     *
     * If the dateBefore and dateAfter are provided, then the value must be between or equal to these dates.
     *
     * For comparisons, the `value` is converted to a Date object at midnight in the system timezone
     * or to polish timezone if the ZoneDateAdapter is enabled.
     *
     * For that make sure, the correct times are set in dateBefore/dateAfter, so the comparison is correct.
     *
     * @param value value being validated
     * @param minIsoDate ISO date to compare with
     * @param maxIsoDate ISO date to compare with
     * @param allowEmpty if true, then empty values are considered valid
     *
     * @returns true if the value is between or equal to the dateBefore and dateAfter.
     **/
    function dateValidator(
        value: any,
        minIsoDate: string | null | undefined,
        maxIsoDate: string | null | undefined,
        allowEmpty: boolean
    ): ValidationResult {
        const stringValue = StringUtils.valueToString(value);

        const isEmpty = StringUtils.isEmpty(stringValue);
        if (allowEmpty && isEmpty) return true;
        if (isEmpty) return t(i => i.validators.invalidDateValidator);

        const convertedDate = adapter.parseDateFromLocalizedFormat(value);
        if (convertedDate == null || !adapter.isValid(convertedDate)) {
            return t(i => i.validators.invalidDateValidator);
        }

        /** Convert string iso date to date object */
        function prepareMinMaxDate(value: string | null | undefined, processor: (date: Date) => Date) {
            if (StringUtils.isEmpty(value)) return null;

            const date = adapter.date(value);
            return date != null && adapter.isValid(date) ? processor(date) : null;
        }

        const minDate = prepareMinMaxDate(minIsoDate, val => adapter.startOfDay(val));
        const maxDate = prepareMinMaxDate(maxIsoDate, val => adapter.endOfDay(val));

        if (minDate != null && maxDate != null) {
            return (
                adapter.isWithinRange(convertedDate, [minDate, maxDate]) ||
                t(i => i.validators.dateBetweenInclusiveValidator, [formatDate(minDate), formatDate(maxDate)])
            );
        }

        if (maxDate != null && minDate == null) {
            return (
                adapter.isEqual(convertedDate, maxDate) ||
                adapter.isBefore(convertedDate, maxDate) ||
                t(i => i.validators.dateBeforeInclusiveValidator, [formatDate(maxDate)])
            );
        }

        if (maxDate == null && minDate != null) {
            return (
                adapter.isEqual(convertedDate, minDate) ||
                adapter.isAfter(convertedDate, minDate) ||
                t(i => i.validators.dateAfterInclusiveValidator, [formatDate(minDate)])
            );
        }

        return true;
    }

    /**
     * Verify that the provided value is a proper time format (HH:mm or HH:mm:ss)
     *
     * @param value value being validated
     * @param allowEmpty if true, then empty values are considered valid
     */
    function timeValidator(value: any, allowEmpty: boolean): ValidationResult {
        const stringValue = StringUtils.valueToString(value);

        const isEmpty = StringUtils.isEmpty(stringValue);
        if (allowEmpty && isEmpty) return true;

        const timeParts = stringValue.split(':');
        if (timeParts.length < 2 || timeParts.length > 3) return t(i => i.validators.validTimeFormatValidator);

        const [hoursPart, minutesPart, secondsPart = '0'] = timeParts;

        if (![hoursPart, minutesPart, secondsPart].every(part => NumberUtils.isInteger(part))) {
            return t(i => i.validators.validTimeFormatValidator);
        }

        const hours = Number(hoursPart);
        const minutes = Number(minutesPart);
        const seconds = Number(secondsPart);

        return !(hours < 0 || hours > 23) && !(minutes < 0 || minutes > 59) && !(seconds < 0 || seconds > 59)
            ? true
            : t(i => i.validators.invalidTimeValidator);
    }

    return {
        required: requiredValidator,
        requireDigit: requireDigitValidator,
        requireNonAlphanumeric: requireNonAlphanumericValidator,
        requireLowercase: requireLowercaseValidator,
        requireUppercase: requireUppercaseValidator,
        requireUniqueCharacters: num => value => requireUniqueCharactersValidator(value, num),
        email:
            (allowEmpty = false) =>
            value =>
                emailValidator(value, allowEmpty),
        minArrayLength: minLength => value => minArrayLengthValidator(value, minLength),
        maxLength: maxLength => value => maxLengthValidator(value, maxLength),
        minLength:
            (minLength, allowEmpty = false) =>
            value =>
                minLengthValidator(value, minLength, allowEmpty),
        length:
            (minLength, maxLength, allowEmpty = false) =>
            value =>
                lengthValidator(value, minLength, maxLength, allowEmpty),
        number:
            (allowEmpty = false) =>
            value =>
                numberValidator(value, allowEmpty),
        integer:
            (allowEmpty = false) =>
            value =>
                integerValidator(value, allowEmpty),
        greaterThan:
            (valueToCompare, inclusive, allowEmpty = false) =>
            value =>
                greaterThanValidator(value, valueToCompare, inclusive, allowEmpty),
        lowerThan:
            (valueToCompare, inclusive, allowEmpty = false) =>
            value =>
                lowerThanValidator(value, valueToCompare, inclusive, allowEmpty),
        regex:
            (regex, allowedCharacters, allowEmpty = false) =>
            value =>
                regexValidator(value, regex, allowedCharacters, allowEmpty),
        uniqueItems:
            (existingItems: MaybeRefOrGetterOrComputedRef<any[]>, caseSensitive = true) =>
            value =>
                uniqueItemsValidator(value, existingItems, caseSensitive),
        date:
            (minIsoDate, maxIsoDate, allowEmpty = false) =>
            value =>
                dateValidator(value, minIsoDate, maxIsoDate, allowEmpty),
        time:
            (allowEmpty = false) =>
            value =>
                timeValidator(value, allowEmpty),
    };
}
