// Calendar dates as the API sends them: "YYYY-MM-DD", with no time or zone.
// Quarantine and isolation run on whole days, so the UI never turns a date into a moment in
// time; doing so would shift days for anyone west of UTC.

const ISO = /^(\d{4})-(\d{2})-(\d{2})$/;
const MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];

/** Days since 1970-01-01 for a calendar date, validating it. */
export function dayNumber(iso: string): number {
  const m = ISO.exec(iso);
  if (!m) throw new SyntaxError(`"${iso}" is not a date in the form YYYY-MM-DD`);
  const [y, mo, d] = [Number(m[1]), Number(m[2]), Number(m[3])];
  const ms = Date.UTC(y, mo - 1, d);
  const back = new Date(ms);
  if (back.getUTCFullYear() !== y || back.getUTCMonth() !== mo - 1 || back.getUTCDate() !== d) {
    throw new RangeError(`"${iso}" is not a real date`);
  }
  return ms / 86_400_000;
}

/** "2026-03-19" -> "19 Mar 2026". */
export function formatDay(iso: string): string {
  const n = dayNumber(iso);
  const date = new Date(n * 86_400_000);
  return `${date.getUTCDate()} ${MONTHS[date.getUTCMonth()]} ${date.getUTCFullYear()}`;
}

/** Whole days left including the last day itself; 0 once the last day has passed. */
export function daysRemaining(today: string, lastDay: string): number {
  return Math.max(0, dayNumber(lastDay) - dayNumber(today) + 1);
}
