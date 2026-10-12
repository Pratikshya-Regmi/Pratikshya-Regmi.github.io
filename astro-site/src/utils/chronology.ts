type DatedEntry = { data: { date?: string; order: number } };
const months = ['january','february','march','april','may','june','july','august','september','october','november','december'];
function key(date = '') {
  const years = [...date.matchAll(/\b(?:19|20)\d{2}\b/g)].map(match => Number(match[0]));
  const year = years.length ? Math.max(...years) : 0;
  const monthMatches = [...date.toLowerCase().matchAll(/\b(jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|may|jun(?:e)?|jul(?:y)?|aug(?:ust)?|sep(?:tember)?|oct(?:ober)?|nov(?:ember)?|dec(?:ember)?)\b/g)];
  const month = monthMatches.length ? months.findIndex(m => m.startsWith(monthMatches.at(-1)![0])) + 1 : 0;
  return { ongoing: /\b(present|current|ongoing)\b/i.test(date), year, month };
}
/** Ongoing first, then latest documented year/month; editorial order breaks ties.
 * Year-only dates retain their existing order after month-specific dates in that year.
 * Missing dates follow dated records; no dates are inferred from image/data years.
 */
export function newestFirst(a: DatedEntry, b: DatedEntry): number {
  const x = key(a.data.date), y = key(b.data.date);
  return Number(y.ongoing) - Number(x.ongoing) || y.year - x.year || y.month - x.month || a.data.order - b.data.order;
}
