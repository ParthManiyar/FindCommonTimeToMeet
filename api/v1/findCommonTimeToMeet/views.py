import datetime
from datetime import timedelta
from django.http import Http404
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
    if not duration_mins:
        raise Exception("The required duration_mins field is not present")
    duration_mins = int(duration_mins)
    if 0 >= duration_mins > 86400:
        raise Exception("The duration_mins should be "
                        "positive integer between 0 and 86401 ")
    if not count:
        raise Exception("The required count field is not present")
    count = int(count)
    if count < 0:
        raise Exception("The count field only takes positive integer")
    return users, duration_mins, count


def convert_to_ist(dt, time_zone):
    time_zone = pytz.timezone(time_zone)
    naive_datetime = dt
    local_datetime = time_zone.localize(naive_datetime, is_dst=None)
    ist_datetime = local_datetime.astimezone(pytz.timezone("Asia/Calcutta"))
    return ist_datetime


def get_date_object(date_string):
    return iso8601.parse_date(date_string)


def get_date_string(date_object):
    return rfc3339.rfc3339(date_object)


def get_in_ist_format(date_string):
    dt = get_date_object(date_string)
    ist_datetime = dt.astimezone(pytz.timezone("Asia/Calcutta"))
    return ist_datetime


def get_user_preference_list(dt, users):
    user_preference_list = []
    for user in users:
        try:
            user_obj = CustomUser.objects.get(id=int(user))
        except CustomUser.DoesNotExist:
            raise Http404(f"No User with given id {user} found")

        preference_time = user_obj.timing_preferences
        time_zone = preference_time.time_zone
        start_date_time = \
            datetime.datetime.combine(dt, preference_time.day_start_time)
        ist_start_date_time = convert_to_ist(start_date_time, time_zone)
        end_date_time = \
            datetime.datetime.combine(dt, preference_time.day_end_time)
        ist_end_date_time = convert_to_ist(end_date_time, time_zone)
        user_preference_list.append((ist_start_date_time, ist_end_date_time))
    return user_preference_list


def common_work_time_interval(dt, users):
    user_preference_list = get_user_preference_list(dt, users)
    user_preference_list.sort()
    start_common_interval = user_preference_list[-1][0]
    user_preference_list.sort(key=lambda x: x[1])
    end_common_interval = user_preference_list[0][1]
    if end_common_interval < start_common_interval:
        raise Exception("No common interval found for given users")
    return start_common_interval, end_common_interval


def get_combine_busy_list(calendar_info, users):
    combined_busy_list = []
    given_date = get_date_object(calendar_info[users[0]]['calendars']['primary']
                                 ['busy'][0]['start']).date()

    for user in users:
        cal_info = calendar_info.get(user.strip(), None)
        if not calendar_info:
            raise Exception(f"Not able to fetch the calendar information for "
                            f"user {user.strip()}")
        busy_list = cal_info['calendars']['primary']['busy']
        for busy in busy_list:
            ist_start_date_time = get_in_ist_format(busy['start'])
            ist_end_date_time = get_in_ist_format(busy['end'])
            combined_busy_list.append((ist_start_date_time, ist_end_date_time))
    return combined_busy_list, given_date


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


def get_slot_list(free_interval_list):
    slots = []
    for time_interval in free_interval_list:
        slot = {
            "start": get_date_string(time_interval[0]),
            "end": get_date_string(time_interval[1])
        }
        slots.append(slot)
    return slots


def get_common_free_intervals(calendar_info, users, duration_mins, count):
    busy_intervals, time_format = get_combine_busy_list(calendar_info, users)
    start_common_interval, end_common_interval = \
        common_work_time_interval(time_format, users)
    start_time = start_common_interval

    dt = start_time + timedelta(minutes=duration_mins)
    end_time = dt
    free_interval_list = []
    number_of_interval = 0
    while end_time <= end_common_interval:
        if not find_clash(start_time, end_time, busy_intervals):
            free_interval_list.append((start_time, end_time))
            number_of_interval += 1
            if number_of_interval == count:
                break
        start_time = end_time
        dt = start_time + timedelta(minutes=duration_mins)
        end_time = dt
    return free_interval_list


class FindCommonTimeToMeetAPIView(APIView):
    @staticmethod
    def post(request, *args, **kwargs):
        try:
            calendar_info = request.data
            params = request.GET
            users, duration_mins, count = check_for_required_params(params)
            free_interval_list = get_common_free_intervals(calendar_info,
                                                           users,
                                                           duration_mins,
                                                           count)
            slots = get_slot_list(free_interval_list)
            if len(slots) == 0:
                return Response({"message": "No common time to meet "
                                            "found for given details"},
                                status=200,
                                content_type="application/json")
            return Response({"slots": slots},
                            status=200,
                            content_type="application/json")
        except Exception as e:
            return Response({"message": str(e)},
                            status=400,
                            content_type="application/json")
