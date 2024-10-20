import { type DateTimeFormatOptions } from '@intlify/core-base';

export interface CmplDateTimeFormats extends Record<string, DateTimeFormatOptions> {
    day: DateTimeFormatOptions;
    minutes: DateTimeFormatOptions;
    seconds: DateTimeFormatOptions;
}

export const enFormats: CmplDateTimeFormats = {
    day: {
        year: 'numeric',
        month: 'numeric',
        day: 'numeric',
    },
    minutes: {
        year: 'numeric',
        month: 'numeric',
        day: 'numeric',
        hour: 'numeric',
        minute: 'numeric',
    },
    seconds: {
        year: 'numeric',
        month: 'numeric',
        day: 'numeric',
        hour: 'numeric',
        minute: 'numeric',
        second: 'numeric',
    },
};

export const plFormats: CmplDateTimeFormats = {
    day: {
        dateStyle: 'short',
    },
    minutes: {
        year: 'numeric',
        month: 'numeric',
        day: 'numeric',
        hour: 'numeric',
        minute: 'numeric',
    },
    seconds: {
        year: 'numeric',
        month: 'numeric',
        day: 'numeric',
        hour: 'numeric',
        minute: 'numeric',
        second: 'numeric',
    },
};
