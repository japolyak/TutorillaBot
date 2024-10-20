import { dirname, resolve, sep } from 'node:path';
import { fileURLToPath as nodeFileURLToPath } from 'node:url';
import { StringUtils } from './../../utils/string.utils';

const nodePolyfills = ['fs', 'url', 'path', 'source-map-js'] as const;
type NodePolyfills = (typeof nodePolyfills)[number];

export type NodePolyfillsAliasesObject<TPolyfills extends string> = Record<TPolyfills, string>;

export interface AliasArrayElement<T extends string> {
    find: T;
    replacement: string;
}

export type NodePolyfillsAliasesArray<TPolyfills extends string> = AliasArrayElement<TPolyfills>[];

/**
 * Depending on your situation:
 * 1. Provide `metaUrl` and `nodeModulesDirectory` if you installed this library, and the polyfill file is present in the node_modules
 *    * `nodeModulesDirectory` by default will have `./node_modules` value
 * 2. Provide `resolvedPolyfillPath` if such file is not in node_modules directory, but somewhere else.
 */
export interface PolyfillNodePackagesOptions {
    resolvedPolyfillPath?: string;
    metaUrl?: string;
    nodeModulesDirectory?: string;
}

/**
 * The sanitize-html library is producing some warnings in the console related node modules packages.
 *
 * This method will create aliases to polyfill missing node packages. There is an option to provide additional packages,
 * which should be polyfilled.
 *
 * Source of this fix: https://github.com/vitejs/vite/discussions/4479#discussioncomment-5205843
 */
export function getNodePolyfillsAliasesArray<T extends string = never>(
    options: PolyfillNodePackagesOptions,
    extraPolyfills?: T[]
): NodePolyfillsAliasesArray<NodePolyfills | T> {
    const { metaUrl, nodeModulesDirectory = `.${sep}node_modules` } = options;
    let { resolvedPolyfillPath = '' } = options;

    if (StringUtils.isNotEmpty(metaUrl)) {
        resolvedPolyfillPath = resolveFileURL(
            metaUrl,
            nodeModulesDirectory,
            '@cmpl',
            'core',
            'dist',
            'node-package-placeholder.js'
        );
    }

    if (StringUtils.isEmpty(resolvedPolyfillPath)) {
        throw new Error('Neither [resolvedPolyfillPath], nor [metaUrl] options were provided.');
    }

    const polyfills: (NodePolyfills | T)[] = [...nodePolyfills];
    if (extraPolyfills) polyfills.push(...extraPolyfills);

    return polyfills.map(i => ({ find: i, replacement: resolvedPolyfillPath }));
}

/**
 * The sanitize-html library is producing some warnings in the console related node modules packages.
 *
 * This method will create aliases to polyfill missing node packages. There is an option to provide additional packages,
 * which should be polyfilled.
 *
 * Source of this fix: https://github.com/vitejs/vite/discussions/4479#discussioncomment-5205843
 */
export function getNodePolyfillsAliasesObject<T extends string = never>(
    options: PolyfillNodePackagesOptions,
    extraPolyfills?: T[]
): NodePolyfillsAliasesObject<NodePolyfills | T> {
    const polyfillsArray = getNodePolyfillsAliasesArray(options, extraPolyfills);

    const result: any = {};

    polyfillsArray.forEach(i => (result[i.find] = i.replacement));

    return result;
}

/** Create absolute URL from file paths */
export function resolveFileURL(metaUrl: string, ...paths: string[]): string {
    // trailing slash is required for the `resolve` method to correctly create the full path
    const directory = fileURLToDirectory(metaUrl, true);

    return resolve(directory, ...paths);
}

/**
 * Expects the URL in file format, which is then mapped to path to directory.
 *
 * @example
 * input: 'file:///C:/temp/src/main.ts'
 * output: 'C:\temp\src'
 */
export function fileURLToDirectory(fileUrl: string, appendTrailingSlash = false): string {
    let result = dirname(fileURLToPath(fileUrl));
    if (appendTrailingSlash && !result.endsWith(sep)) result += sep;

    return result;
}

/**
 * Expects the URL in file format, which is then mapped to path to the file.
 *
 * @example
 * input: 'file:///C:/temp/src/main.ts'
 * output: 'C:\temp\src\main.ts'
 */
export function fileURLToPath(fileUrl: string | URL): string {
    return nodeFileURLToPath(fileUrl);
}
