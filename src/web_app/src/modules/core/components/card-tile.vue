<template>
	<v-card height="156" class="card-shadow tile" @click="openView">
		<div class="content mt-5">
			<v-badge :content="componentItemsCount" bordered>
				<v-icon :icon="icon" />
			</v-badge>
		</div>

		<v-card-title class="content">
			<div class="content-title">{{ title }}</div>
		</v-card-title>
		<v-card-text v-if="subTitlePassed" class="content">
			<div class="content-subtitle">{{ subTitle }}</div>
		</v-card-text>
	</v-card>
</template>

<script setup lang="ts">
import {computed, type PropType} from 'vue';
import { StringUtils } from '@/utils/string.utils';
import { useRouter } from 'vue-router';

const props = defineProps({
	buttonText: {
		type: String,
		required: true,
	},
	componentItemsCount: {
		type: Number as PropType<number | undefined>,
		default: undefined,
	},
	icon: {
		type: String,
		default: 'mdi-help',
	},
	params: {
		type: Object,
		default: {},
	},
	query: {
		type: Object,
		default: {},
	},
	subTitle: {
		type: String,
		default: '',
	},
	title: {
		type: String,
		required: true,
	},
	view: {
		type: String,
		required: true,
	},
})

const router = useRouter();

const subTitlePassed = computed(() => StringUtils.isNotEmpty(props.subTitle));

const openView = async () => await router.push({ name: props.view, params: props.params, query: props.query });
</script>

<style lang="scss">
.tile {
    .card-shadow {
        box-shadow: 0 1px 12px #0000000a;
    }

    .v-card-actions {
        padding-top: 3px;
        padding-bottom: 0;
    }

    .content {
        display: flex;
        justify-content: center;
        text-align: center;

        .content-title {
            font-size: 24px;
            color: #001a31;
        }

        .content-subtitle {
            font-size: 12px;
            color: #001a31;
        }
    }

    .v-badge__badge {
        height: 28px;
        font-size: 20px;
        font-weight: 400;
        border-radius: 14px;
        min-width: 28px;
    }

    .v-badge--bordered .v-badge__badge::after {
        border-width: 3px;
        border-color: #ffffff;
    }
}
</style>
