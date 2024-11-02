import type { ScheduleEventDto } from '@/modules/core/services/api/api.models';
import type { ScheduleEventModel } from '@/modules/schedule/models';
import { parseDate, type Timestamp } from '@quasar/quasar-ui-qcalendar/src/index.js'

export class ScheduleUtils {
	public static toTimestamp(date: number): Timestamp {
		return parseDate(new Date(date));
	}

	public static eventMapper(event: ScheduleEventDto): ScheduleEventModel {
		const timestamp = ScheduleUtils.toTimestamp(event.date);

		return {
			id: event.id,
			title: `${event.subjectName} | ${event.personName}`,
			date: timestamp.date,
			time: timestamp.time,
			duration: event.duration,
			type: event.type,
		}
	}
}
