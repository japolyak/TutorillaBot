// NOTE: all vuetify types were copied from the vuetify source code, from "3.5.3" tag

export type SortItem = { key: string; order?: boolean | 'asc' | 'desc' };

// This interface was created based on the computed property in VDataTable/composables/options.ts
export interface DataTablePagination {
    page: number;
    itemsPerPage: number;
    sortBy: readonly SortItem[];
    groupBy: readonly SortItem[];
    search?: string;
}

export type SelectItemKey<T = Record<string, any>> =
    | boolean
    | null
    | undefined // Ignored
    | string // Lookup by key, can use dot notation for nested objects
    | readonly (string | number)[] // Nested lookup by key, each array item is a key in the next level
    | ((item: T, fallback?: any) => any);

/**
 * - match without highlight
 * - single match (index), length already known
 * - single match (start, end)
 * - multiple matches (start, end), probably shouldn't overlap
 */
export type FilterMatch = boolean | number | [number, number] | [number, number][];
export type FilterFunction = (value: string, query: string, item?: InternalItem) => FilterMatch;

export interface InternalItem<T = any> {
    value: any;
    raw: T;
}

export type DataTableCompareFunction<T = any> = (a: T, b: T) => number;

export type DataTableHeader = {
    key?: 'data-table-group' | 'data-table-select' | 'data-table-expand' | (string & {});
    value?: SelectItemKey;
    title?: string;

    fixed?: boolean;
    align?: 'start' | 'end' | 'center';

    width?: number | string;
    minWidth?: string;
    maxWidth?: string;

    headerProps?: Record<string, any>;
    cellProps?: HeaderCellProps;

    sortable?: boolean;
    sort?: DataTableCompareFunction;
    sortRaw?: DataTableCompareFunction;
    filter?: FilterFunction;

    children?: DataTableHeader[];
};

export type InternalDataTableHeader = Omit<DataTableHeader, 'key' | 'value' | 'children'> & {
    key: string | null;
    value: SelectItemKey | null;
    sortable: boolean;
    fixedOffset?: number;
    lastFixed?: boolean;
    colspan?: number;
    rowspan?: number;
    children?: InternalDataTableHeader[];
};

export interface GroupableItem<T = any> {
    type: 'item';
    raw: T;
}

export interface SelectableItem {
    value: any;
    selectable: boolean;
}

export interface DataTableItem<T = any> extends InternalItem<T>, GroupableItem<T>, SelectableItem {
    key: any;
    index: number;
    columns: {
        [key: string]: any;
    };
}

export interface Group<T = any> {
    type: 'group';
    depth: number;
    id: string;
    key: string;
    value: any;
    items: readonly (T | Group<T>)[];
}

export type GroupHeaderSlot = {
    index: number;
    item: Group;
    columns: InternalDataTableHeader[];
    isExpanded: (item: DataTableItem) => boolean;
    toggleExpand: (item: DataTableItem) => void;
    isSelected: (items: SelectableItem | SelectableItem[]) => boolean;
    toggleSelect: (item: SelectableItem) => void;
    toggleGroup: (group: Group) => void;
    isGroupOpen: (group: Group) => boolean;
};

type ItemSlotBase<T = any> = {
    index: number;
    item: T;
    internalItem: DataTableItem<T>;
    isExpanded: (item: DataTableItem) => boolean;
    toggleExpand: (item: DataTableItem) => void;
    isSelected: (items: SelectableItem | SelectableItem[]) => boolean;
    toggleSelect: (item: SelectableItem) => void;
};

export type ItemSlot<T = any> = ItemSlotBase<T> & {
    columns: InternalDataTableHeader[];
};

export type ItemKeySlot<T = any> = ItemSlotBase<T> & {
    value: any;
    column: InternalDataTableHeader;
};

export type RowProps<T> =
    | Record<string, any>
    | ((data: Pick<ItemKeySlot<T>, 'index' | 'item' | 'internalItem'>) => Record<string, any>);

export type CellProps<T> =
    | Record<string, any>
    | ((data: Pick<ItemKeySlot<T>, 'index' | 'item' | 'internalItem' | 'value' | 'column'>) => Record<string, any>);

export type HeaderCellProps =
    | Record<string, any>
    | ((data: Pick<ItemKeySlot<any>, 'index' | 'item' | 'internalItem' | 'value'>) => Record<string, any>);

export type ValidationResult = string | boolean;
export type ValidationRuleFn = (value: any) => ValidationResult;
export type ValidationRuleAsyncFn = (value: any) => PromiseLike<ValidationResult>;
export type ValidationRule =
    | ValidationResult
    | PromiseLike<ValidationResult>
    | ValidationRuleFn
    | ValidationRuleAsyncFn;

export type ValidateOnValue = 'blur' | 'input' | 'submit';
