from datetime import datetime, timedelta, timezone
def get_time_range(time_range):
    current_time = datetime.now(timezone(timedelta(hours=8)))
    time_end = current_time.isoformat()
    time_start = current_time - timedelta(seconds=time_range)
    time_start = time_start.isoformat()
    return time_start, time_end