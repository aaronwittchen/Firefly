import dayjs from "dayjs";
import relativeTime from "dayjs/plugin/relativeTime";

dayjs.extend(relativeTime);

export function useDayjs() {
  const formatDate = (date: string | Date | null | undefined, format = "MMM D, YYYY") => {
    if (!date) return "-";
    return dayjs(date).format(format);
  };

  const formatDateTime = (date: string | Date | null | undefined) => {
    if (!date) return "-";
    return dayjs(date).format("MMM D, YYYY h:mm A");
  };

  const formatRelative = (date: string | Date | null | undefined) => {
    if (!date) return "-";
    return dayjs(date).fromNow();
  };

  return {
    dayjs,
    formatDate,
    formatDateTime,
    formatRelative,
  };
}
