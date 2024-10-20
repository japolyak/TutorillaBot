export class StringUtils {
    /**
     * Checks whether provided value is null or in case of a string, whether it consists of only white-spaces.
     * @param value the value that is checked
     */
    public static isEmpty(value: string | null | undefined): value is null | undefined {
        if (value == null || typeof value !== 'string') return true;

        return value.trim().length <= 0;
    }

    /**
     * Checks whether provided value is not null and in case of a string, whether it contains at least one non white-space character.
     * @param value the value that is checked
     */
    public static isNotEmpty(value: string | null | undefined): value is string {
        if (value == null || typeof value !== 'string') return false;

        return value.trim().length > 0;
    }

    /**
     * Compare two strings. Empty strings (with white-spaces) are considered to be null.
     * @example
     * areEqual(null, undefined) // true
     * areEqual(undefined, null) // true
     * areEqual(null, '') // true
     * areEqual('', null) // true
     * areEqual('', undefined) // true
     * areEqual(undefined, '') // true
     */
    public static equals(value1: string | null | undefined, value2: string | null | undefined): boolean {
        if (StringUtils.isEmpty(value1) && StringUtils.isEmpty(value2)) return true;
        return value1 === value2;
    }

    /** Checks whether provided character is a digit */
    public static isDigit(c: string) {
        return typeof c === 'string' && c.length === 1 && c >= '0' && c <= '9';
    }

    /** Checks whether provided character is a lowercase character */
    public static isLowercase(c: string) {
        return typeof c === 'string' && c.length === 1 && c >= 'a' && c <= 'z';
    }

    /** Checks whether provided character is an uppercase character */
    public static isUppercase(c: string) {
        return typeof c === 'string' && c.length === 1 && c >= 'A' && c <= 'Z';
    }

    /** Checks whether provided character is an lowercase or uppercase character */
    public static isLetter(c: string) {
        return StringUtils.isLowercase(c) || StringUtils.isUppercase(c);
    }

    /** Checks whether provided character is a letter or digit */
    public static isLetterOrDigit(c: string) {
        return StringUtils.isDigit(c) || StringUtils.isLetter(c);
    }

    /** Converts any value to string. Value is trimmed. */
    public static valueToString(value: any) {
        if (typeof value === 'string') return value.trim();
        if (value == null) return '';

        return String(value).trim();
    }
}
