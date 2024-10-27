import type { ScheduleEventDto } from '@/modules/core/services/api/api.models';
import type { ScheduleEventModel } from '@/modules/schedule/models';
import { parseDate, type Timestamp } from '@quasar/quasar-ui-qcalendar/src/index.js'

export function eventMapper(event: ScheduleEventDto): ScheduleEventModel {
	const timestamp: Timestamp = parseDate(new Date(event.date));

	return {
		id: event.id,
		title: event.title,
		date: timestamp.date,
		time: timestamp.time,
		duration: event.duration,
		type: event.type,
	}
}
