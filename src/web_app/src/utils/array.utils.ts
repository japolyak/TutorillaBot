export class ArrayUtils {
    /**
     * Insert multiple elements to an array at specified index. The original array is modified.
     */
    public static insertMany(array: any[], index: number, items: any[]): void {
        const subArray = array.slice.call(items);
        // eslint-disable-next-line prefer-spread
        array.splice.apply(array, [index, 0].concat(subArray) as any);
    }

    public static mergeUnique<T>(a: T[], b: T[], predicate: (a: T, b: T) => boolean = (a, b) => a === b): any[] {
        const c = [...a];
        b.forEach(bItem => (c.some(cItem => predicate(bItem, cItem)) ? null : c.push(bItem)));
        return c;
    }

    public static removeItems<T>(array: T[], itemsToRemove: T[]): T[] {
        return array.filter(item => !itemsToRemove.includes(item));
    }
}
