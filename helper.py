from datetime import datetime, timedelta, timezone
def get_time_range(time_range):
    time_range = int(time_range)
    current_time = datetime.now(timezone(timedelta(hours=8)))
    time_end = current_time.isoformat()
    time_start = current_time - timedelta(minutes=time_range)
    time_start = time_start.isoformat()
    return time_start, time_end

def is_valid_key(_json, _key):
    return _key in _json and _json[_key] is not None

def sort_dict(_dict):
    return sorted(_dict.items(), key=lambda item: item[1], reverse=True)