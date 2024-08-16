import { acceptHMRUpdate, defineStore } from 'pinia';
import { ref, computed } from 'vue';
import type { AssignmentDto, NewClassDto, TextbookDto } from '@/modules/core/services/api/api.models';
import type { TextbookAssignment } from '@/modules/class-planer/models';


export const useClassPlannerStore = defineStore('class-planner-store', () => {
	const date = ref<Date | null>(null);

	const setAssignment = ref(false);

	const textbookAssignments = ref<TextbookAssignment[]>([]);

	const newClass = computed(() => {
		const data: NewClassDto = {
			date: new Date(),
			assignments: textbookAssignments.value
				.filter(a => a.include)
				.map(a => {
					const assignment: AssignmentDto = {
						textbookId: a.id,
						description: a.description,
					};

					return assignment;
				}),
		};

		return data;
	});

	function setFlatTextbookAssignmentsList(list: TextbookDto[]) {
		textbookAssignments.value = list.map(i => {
			const assignment: TextbookAssignment = {
				id: i.id,
				title: i.title,
				description: null,
				include: false,
			};

			return assignment;
		})
	}

	function resetAssignment() {
		setAssignment.value = false;
		textbookAssignments.value.forEach(item => {
			item.description = null;
			item.include = false;
		});
	}

	function restoreClassPlanner(isTutor = false) {
		date.value = null;

		if (isTutor) resetAssignment();
	}

    return {
		date,
		textbookAssignments,
		newClass,
		setAssignment,
		restoreClassPlanner,
		setFlatTextbookAssignmentsList,
    };
});

if (import.meta.hot) {
    import.meta.hot.accept(acceptHMRUpdate(useClassPlannerStore, import.meta.hot));
}
