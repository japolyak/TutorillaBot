import type { Module } from '@/plugins/router/view-definitions';
import type { RouteMeta } from 'vue-router';
import type { Role } from '@/modules/core/services/api/api.models';
import { RouteAuthMeta } from '@/plugins/router/utils/route-auth-meta';


export class RouteMetaBuilder {
	private title: string = '';
	private icon: string | null = null;
	private allowAnonymousFlag = false;
	private module: Module | null = null;
	private readonly requiredRoles: Role[] = [];
	private useDashboardLayoutFlag = true;

	public build(): RouteMeta {
		return {
			title: this.title,
			icon: this.icon,
			module: this.module,
			authGuard: new RouteAuthMeta(
				this.allowAnonymousFlag,
				this.requiredRoles,
			),
			useDashboardLayout: this.useDashboardLayoutFlag,
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

	public withRoles(...roles: Role[]): this {
		this.requiredRoles.push(...roles)
		return this;
	}

	public allowAnonymous(): this {
		this.allowAnonymousFlag = true;
		return this;
	}

	public hideDashboardLayout(): this {
		this.useDashboardLayoutFlag = false;
		return this;
	}
}
