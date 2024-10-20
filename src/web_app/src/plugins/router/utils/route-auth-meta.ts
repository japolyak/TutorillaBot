import type { Role } from '@/modules/core/services/api/api.models';
import { useUserStore } from '@/modules/core/store/user-store';

type NoAccessReason = 'missingRoles' | 'onlyAnonymous';

export interface AuthCheckResult {
	hasAccess: boolean;
	noAccessReason?: NoAccessReason;
}

export class RouteAuthMeta {
	constructor(
		private readonly allowAnonymous: boolean,
		private readonly requiredRoles: Role[]
	) {}

	public checkAccess(): AuthCheckResult {
		const isAuthenticated = this.isAuthenticated();
		console.log('isAuthenticated', isAuthenticated);

		if (!this.allowAnonymous && !isAuthenticated) {
			return this.createResult('missingRoles');
		} else if (!this.allowAnonymous && isAuthenticated) {
			return this.createResult(true);
		} if (this.allowAnonymous) {
			return this.createResult(true);
		}

		return this.createResult(true);
	}

	private isAuthenticated(): boolean {
		const { userInfo, hasRoles } = useUserStore();

		if (!userInfo) return false;

		return !this.requiredRoles.length ? true : hasRoles(this.requiredRoles);
	}

	private createResult(value: boolean | NoAccessReason): AuthCheckResult {
		if (typeof value === 'boolean') return { hasAccess: value };

		return {
			hasAccess: false,
			noAccessReason: value,
		}
	}
}
