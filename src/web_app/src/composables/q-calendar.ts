import { prevDay, getStartOfWeek, parseTimestamp, nextDay, getEndOfWeek } from '@quasar/quasar-ui-qcalendar';
import type { Timestamp, TimestampOrNull } from '@quasar/quasar-ui-qcalendar';


export function useQCalendar() {
	const weekdays = [1, 2, 3, 4, 5, 6, 0];

	function toTimestampString(date: Date): string {
		const isoDate = date.toISOString();
		return `${isoDate.slice(0, 10)} ${isoDate.slice(11, 16)}`;
	}

	function toTimestamp(date: Date): TimestampOrNull {
		const timestampString = toTimestampString(date);

		return parseTimestamp(timestampString);
	}

	function getWeekBorder(date: Date | string, border: 'start' | 'end'): TimestampOrNull {
		if (typeof date !== 'string') date = toTimestampString(date);

		const timestamp = parseTimestamp(date);
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
		getWeekBorder,
		toTimestamp
	};
}
