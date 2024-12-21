import { prevDay, getStartOfWeek, nextDay, getEndOfWeek } from '@quasar/quasar-ui-qcalendar';
import type { Timestamp, TimestampOrNull } from '@quasar/quasar-ui-qcalendar';
import { ScheduleUtils } from '@/modules/schedule/services/mappers';


export function useQCalendar() {
	const weekdays = [1, 2, 3, 4, 5, 6, 0];

	function getWeekBorder(date: Date | string, border: 'start' | 'end'): TimestampOrNull {
		const timestamp = ScheduleUtils.toTimestamp(date);
		if (!timestamp) return null;

		return border === 'start'
			? getStartOfWeek(timestamp, weekdays)
			: getEndOfWeek(timestamp, weekdays);
	}

	function getStartOfNextWeek(date: string): TimestampOrNull {
		const end = getWeekBorder(date, 'end');
		if (!end) return null;

		const day: Timestamp = nextDay(end);

		day.date = `${day.year}-${day.month}-${day.day}`

		return day;
	}

	function getStartOfPrevWeek(date: string): TimestampOrNull {
		const start = getWeekBorder(date, 'start');
		if (!start) return null;

		let day: TimestampOrNull = prevDay(start);
		day.date = `${day.year}-${day.month}-${day.day}`;

		day = getWeekBorder(day.date, 'start');
		if (!day) return null;

		day.date = `${day.year}-${day.month}-${day.day}`;

		return day;
	}

	return {
		weekdays,
		getStartOfNextWeek,
		getStartOfPrevWeek,
		getWeekBorder
	};
}
