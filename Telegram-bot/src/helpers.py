from datetime import datetime

def convert_unixtime_to_timestamp(unix_time):
    if unix_time:
        return datetime.utcfromtimestamp(unix_time).strftime('%Y-%m-%dT%H:%M:%SZ')