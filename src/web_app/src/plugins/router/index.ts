import { createRouter, createWebHistory } from 'vue-router';
import PlanClassView from '@/modules/class-planer/views/plan-class-view.vue';
import TestView from '@/modules/dev/test-view.vue';
import Dashboard from '@/modules/core/components/dashboard.vue';
import { telegramUserAuthentication } from 'src/plugins/router/telegram-validation'

const router = createRouter({
    history: createWebHistory(),
    routes: [
		{
			path: '/',
			component: Dashboard,
            children: [
                {
                    path: '/private-course/:privateCourseId',
                    name: 'PlanClassView',
                    component: PlanClassView,
                },
				{
					path: 'test',
					name: 'Test',
					component: TestView,
				}
            ],
		},

    ],
});

router.beforeEach(async (to, from, next) => await telegramUserAuthentication(window.Telegram.WebApp.initData, next));

export default router;
