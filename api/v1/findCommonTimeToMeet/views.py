import datetime
from datetime import date, timedelta
from rest_framework.response import Response
from rest_framework.views import APIView
import pytz
from findCommonTimeToMeetApp.models import CustomUser
import iso8601
import rfc3339


def check_for_required_params(params):
    users = params.get('users', None)
    duration_mins = params.get('duration_mins', None)
    count = params.get('count', None)
    if not users:
        raise Exception("The required users field is not present")
    users = users.split(',')
    if len(users) != 2:
        raise Exception("Requires exactly two user id")
    if not duration_mins:
        raise Exception("The required duration_mins field is not present")
    duration_mins = int(duration_mins)
    if not count:
        raise Exception("he required count field is not present")
    count = int(count)
    return users, duration_mins, count


def convert_to_utc(time, time_zone):
    time_zone = pytz.timezone(time_zone)
    naive_datetime = datetime.datetime(2010, 10, 31, time.hour, time.minute,
                                       time.second)
    local_datetime = time_zone.localize(naive_datetime, is_dst=None)
    utc_datetime = local_datetime.astimezone(pytz.timezone("Asia/Calcutta"))
    return utc_datetime.time()


def get_date_object(date_string):
    return iso8601.parse_date(date_string)


def get_date_string(date_object):
    return rfc3339.rfc3339(date_object)


def convert_date_to_utc(date_string):
    dt = get_date_object(date_string)
    utc_datetime = dt.astimezone(pytz.timezone("Asia/Calcutta"))
    return utc_datetime.time()


def get_user_preference_list(users):
    user_preference_list = []
    for user in users:
        user_obj = CustomUser.objects.get(id=int(user))
        preference_time = user_obj.timing_preferences
        time_zone = preference_time.time_zone
        start_time = preference_time.day_start_time
        utc_start_time = convert_to_utc(start_time, time_zone)
        end_time = preference_time.day_end_time
        utc_end_time = convert_to_utc(end_time, time_zone)
        user_preference_list.append((utc_start_time, utc_end_time))
    return user_preference_list


def common_work_time_interval(users):
    user_preference_list = get_user_preference_list(users)
    user_preference_list.sort()
    start_common_interval = user_preference_list[-1][0]
    user_preference_list.sort(key=lambda x: x[1])
    end_common_interval = user_preference_list[0][1]
    if end_common_interval < start_common_interval:
        raise Exception("No common interval found for given users")
    return start_common_interval, end_common_interval


def get_blocked_time_interval_list(body, users):
    blocked_time_interval_list = []
    dt = get_date_object(body[users[0]]['calendars']['primary']['busy'][0]['start'])
    for user in users:
        calendar_info = body.get(user, None)
        if not calendar_info:
            raise Exception(f"Not able to fetch the calendar information for "
                            f"{user}")
        busy_list = calendar_info['calendars']['primary']['busy']
        for busy in busy_list:
            utc_start_time = convert_date_to_utc(busy['start'])
            utc_end_time = convert_date_to_utc(busy['end'])
            blocked_time_interval_list.append((utc_start_time, utc_end_time))
    return blocked_time_interval_list, dt


def find_clash(start_time, end_time, busy_intervals):
    found_clash = False
    for interval in busy_intervals:
        if interval[0] <= start_time < interval[1]:
            found_clash = True
            break
        elif interval[0] < end_time < interval[1]:
            found_clash = True
            break
        elif start_time <= interval[0] < end_time:
            found_clash = True
            break
        elif start_time < interval[1] < end_time:
            found_clash = True
            break
    return found_clash


def convert_interval_to_date(free_interval_list, time_format):
    slots = []
    for time_interval in free_interval_list:
        slot = {"start": get_date_string(time_format.replace(
                            hour=time_interval[0].hour,
                            minute=time_interval[0].minute
                            )),
                "end": get_date_string(time_format.replace(
                    hour=time_interval[1].hour,
                    minute=time_interval[1].minute
                    ))
                }
        slots.append(slot)
    return slots


def get_common_free_intervals(body, users, duration_mins):
    start_common_interval, end_common_interval = \
        common_work_time_interval(users)
    busy_intervals, time_format = get_blocked_time_interval_list(body, users)
    start_time = start_common_interval

    dt = datetime.datetime.combine(date.today(), start_time) + \
        timedelta(minutes=duration_mins)
    end_time = dt.time()
    free_interval_list = []
    while end_time <= end_common_interval:
        if not find_clash(start_time, end_time, busy_intervals):
            free_interval_list.append((start_time, end_time))
        start_time = end_time
        dt = datetime.datetime.combine(date.today(), start_time) + \
            timedelta(minutes=duration_mins)
        end_time = dt.time()
    return free_interval_list, time_format


class FindCommonTimeToMeetAPIView(APIView):
    @staticmethod
    def post(request, *args, **kwargs):
        try:
            body = request.data
            params = request.GET
            users, duration_mins, count = check_for_required_params(params)
            free_interval_list, time_format = \
                get_common_free_intervals(body, users, duration_mins)
            slots = convert_interval_to_date(free_interval_list, time_format)
            return Response(slots,
                            status=200,
                            content_type="application/json")
        except Exception as e:
            return Response({"message": str(e)},
                            status=400,
                            content_type="application/json")
