export type Interval = { start: number; end: number };
export type BookingRequest = { start: number; end: number; now: number; blocked: boolean; bookings: Interval[] };
export function canBook({ start, end, now, blocked, bookings }: BookingRequest): boolean {
  if (!(0 <= start && start < end && end <= 1440)) return false;
  if (!(start > now)) return false;
  if (end - start > 120) return false;
  if (blocked) return false;
  for (const booking of bookings) if (start < booking.end && end > booking.start) return false;
  return true;
}
