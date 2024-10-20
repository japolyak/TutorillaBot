import type { Module } from '@/plugins/router/view-definitions';
import type { RouteMeta } from 'vue-router';


export class RouteMetaBuilder {
	private title: string = '';
	private icon: string | null = null;
	private module: Module | null = null;

	public build(): RouteMeta {
		return {
			title: this.title,
			icon: this.icon,
			module: this.module,
		}
	}

	public withTitle(title: string): this {
		this.title = title;
		return this;
	}

	public withIcon(icon: string): this {
		this.icon = icon;
		return this;
	}

	public partOfModule(module: Module): this {
		this.module = module;
		return this;
	}
}
