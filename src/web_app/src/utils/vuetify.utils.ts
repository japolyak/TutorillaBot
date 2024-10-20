export type SelectItemKey<T = Record<string, any>> =
    | boolean
    | null
    | undefined // Ignored
    | string // Lookup by key, can use dot notation for nested objects
    | readonly (string | number)[] // Nested lookup by key, each array item is a key in the next level
    | ((item: T, fallback?: any) => any);

export class VuetifyUtils {
    /**
     * Creates colors entry for the Vuetify theme. Object returned by this function must be destructured into the `colors` object in the theme.
     *
     * Such colors can be used in the templates in the following way:
     * * as a css class with `bg-` prefix: `class="bg-{name}"`
     * * as a value for `color` prop for vuetify components: `color="{name}"`
     *
     * @example
     * ...createColor('btn-hover-color', #ffffff, #000000);
     * @param name color will be available by this name
     * @param bgColor background color
     * @param textColor foreground color
     */
    public static createColor(name: string, bgColor: string, textColor: string) {
        const result: any = {};
        result[name] = bgColor;
        result[`on-${name}`] = textColor;
        return result;
    }

    /**
     * Checks whether provided value is an object.
     * @param obj
     */
    public static isObject(obj: any): obj is object {
        return obj !== null && typeof obj === 'object' && !Array.isArray(obj);
    }

    /**
     * Deep merge objects.
     *
     * This function is copied from vuetify source code.
     *
     * @param source
     * @param target
     * @param arrayFn
     */
    public static mergeDeep(
        source: Record<string, any> = {},
        target: Record<string, any> = {},
        arrayFn?: (a: unknown[], b: unknown[]) => unknown[]
    ) {
        const out: Record<string, any> = {};

        for (const key in source) {
            out[key] = source[key];
        }

        for (const key in target) {
            const sourceProperty = source[key];
            const targetProperty = target[key];

            // Only continue deep merging if
            // both properties are objects
            if (VuetifyUtils.isObject(sourceProperty) && VuetifyUtils.isObject(targetProperty)) {
                out[key] = VuetifyUtils.mergeDeep(sourceProperty, targetProperty, arrayFn);

                continue;
            }

            if (Array.isArray(sourceProperty) && Array.isArray(targetProperty) && arrayFn) {
                out[key] = arrayFn(sourceProperty, targetProperty);

                continue;
            }

            out[key] = targetProperty;
        }

        return out;
    }

    // source: https://github.com/vuetifyjs/vuetify/blob/ec746d37adcabbf30bbbe6112124929c2f3bcb00/packages/vuetify/src/util/helpers.ts#L79
    /** Return property value from the item */
    public static getPropertyFromItem(item: any, property: SelectItemKey, fallback?: any): any {
        if (property === true) return item === undefined ? fallback : item;

        if (property == null || typeof property === 'boolean') return fallback;

        if (item !== Object(item)) {
            if (typeof property !== 'function') return fallback;

            const value = property(item, fallback);

            return typeof value === 'undefined' ? fallback : value;
        }

        if (typeof property === 'string') return VuetifyUtils.getObjectValueByPath(item, property, fallback);

        if (Array.isArray(property)) return VuetifyUtils.getNestedValue(item, property, fallback);

        if (typeof property !== 'function') return fallback;

        const value = property(item, fallback);

        return typeof value === 'undefined' ? fallback : value;
    }

    // source: https://github.com/vuetifyjs/vuetify/blob/ec746d37adcabbf30bbbe6112124929c2f3bcb00/packages/vuetify/src/util/helpers.ts#L64
    /** Returns the value of the provided nested path */
    public static getObjectValueByPath(obj: any, path?: string | null, fallback?: any): any {
        // credit: http://stackoverflow.com/questions/6491463/accessing-nested-javascript-objects-with-string-key#comment55278413_6491621
        if (obj == null || !path || typeof path !== 'string') return fallback;
        if (obj[path] !== undefined) return obj[path];
        path = path.replace(/\[(\w+)\]/g, '.$1'); // convert indexes to properties
        path = path.replace(/^\./, ''); // strip a leading dot
        return VuetifyUtils.getNestedValue(obj, path.split('.'), fallback);
    }

    // source: https://github.com/vuetifyjs/vuetify/blob/ec746d37adcabbf30bbbe6112124929c2f3bcb00/packages/vuetify/src/util/helpers.ts#L20
    /** Returns the value of the provided nested path */
    public static getNestedValue(obj: any, path: (string | number)[], fallback?: any): any {
        const last = path.length - 1;

        if (last < 0) return obj === undefined ? fallback : obj;

        for (let i = 0; i < last; i++) {
            if (obj == null) {
                return fallback;
            }
            obj = obj[path[i]];
        }

        if (obj == null) return fallback;

        return obj[path[last]] === undefined ? fallback : obj[path[last]];
    }
}
