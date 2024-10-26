<template>
    <v-text-field
        ref="textFieldRef"
        v-model="displayValue"
        :append-inner-icon="menu ? 'mdi-chevron-up' : 'mdi-chevron-down'"
		density="compact"
		variant="outlined"
		readonly
		max-width="200"
		:focused="menu"
		hide-details
    >
        <v-menu v-model="menu" activator="parent" min-width="0" :close-on-content-click="false">
            <v-confirm-edit v-model="classDate" @save="menu = false">
                <template #default="{ actions, model: proxyModel }">
                    <v-date-picker
                        v-model="proxyModel.value"
                        weeks-in-month="dynamic"
                        :hide-header="true"
						@update:model-value="selectDate"
                    >
                    </v-date-picker>
                </template>
            </v-confirm-edit>
        </v-menu>
    </v-text-field>
</template>

<script setup lang="ts">
import { ref, shallowRef, watchEffect } from 'vue';
import { useDate } from 'vuetify';
import { VConfirmEdit, VDatePicker, VTextField } from 'vuetify/components';
import { useScheduleStore } from '@/modules/schedule/services/schedule-store';
import { storeToRefs } from 'pinia';

const adapter = useDate();

const { classDate } = storeToRefs(useScheduleStore());

const textFieldRef = ref<VTextField | null>(null);

const displayValue = ref<string | null>(null);
const menu = shallowRef(false);

function selectDate(value: Date) {
	classDate.value = value;
	menu.value = false;
}

watchEffect(() => {
    displayValue.value = classDate.value == null ? null : adapter.format(classDate.value, 'normalDateWithWeekday');
});
</script>

<style lang="scss">
.v-picker {
	//max-width: 275px;

	.v-picker__body {
		.v-date-picker-controls {
			max-height: 48px;
		}

		.v-date-picker-month__days {

			.v-date-picker-month__day {
				//height: 30px;
				//width: 30px;

				.v-btn {
					//height: 30px;
					//width: 30px;
				}
			}
		}
	}

}
</style>
