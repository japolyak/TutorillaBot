import { StringUtils } from './string.utils';

export class NumberUtils {
    /**
     * Check whether the provided value consists of optional `-` sign at the beginning and digits (at least one).
     *
     * If true is returned, then it is safe to cast the value to number.
     **/
    public static isInteger(value: any): boolean {
        if (!NumberUtils.isNumber(value)) return false;

        const stringValue = StringUtils.valueToString(value);
        return /^([+-])?[0-9]{1,}$/.test(stringValue);
    }

    /**
     * Check whether the provided value consists of digits (at least one).
     *
     * If true is returned, then it is safe to cast the value to number.
     **/
    public static isPositiveInteger(value: any): boolean {
        if (!NumberUtils.isNumber(value)) return false;

        const stringValue = StringUtils.valueToString(value);
        return /^[0-9]{1,}$/.test(stringValue);
    }

    /**
     * Checks whether the provided value is any number (integer or decimal).
     *
     * The value is first converted into a string and then checked.
     *
     * If true is returned, then it is safe to cast the value to number.
     **/
    public static isNumber(value: any): boolean {
        const stringValue = StringUtils.valueToString(value);
        if (StringUtils.isEmpty(stringValue)) return false;

        // src: https://stackoverflow.com/a/35759874
        return !isNaN(+value) && !isNaN(parseFloat(value));
    }

    /**
     * Checks whether the provided value is any number (integer or decimal).
     *
     * Returns true, if the value is >= 0.
     **/
    public static isPositiveNumber(value: any): boolean {
        if (!NumberUtils.isNumber(value)) return false;

        const stringValue = StringUtils.valueToString(value);
        const parsedValue = parseFloat(stringValue);
        return parsedValue >= 0;
    }
}
