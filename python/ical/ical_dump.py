# -*- coding: utf-8 -*-
import sys

## It seems that locale will always be C(ascii) when
## mutt call this script via mailcap
reload(sys)
sys.setdefaultencoding('utf-8')

from icalendar import Calendar
import pytz

dst_tz = pytz.timezone('Asia/Shanghai')

def convert_timezone(dt, tz):
    try:
        return dt.astimezone(tz)
    except ValueError:
        return tz.localize(dt)

def dump_summary(event):
    if 'summary' in event:
        return event['summary']

def dump_organizer(event):
    if 'organizer' in event:
        return event['organizer']

def dump_location(event):
    if 'location' in event:
        return event['location']

def dump_attendee(event):
    if 'attendee' in event:
        return ", ".join(event['attendee'])

def dump_dtstart(event):
    if 'dtstart' in event:
        return convert_timezone(event['dtstart'].dt, dst_tz).strftime('%Y/%m/%d %H:%M')

def dump_dtend(event):
    if 'dtend' in event:
        return convert_timezone(event['dtend'].dt, dst_tz).strftime('%Y/%m/%d %H:%M')

def dump_event(event):
    print('Summary : %s' % dump_summary(event))
    print('Organizer : %s' % dump_organizer(event))
    print('Location : %s' % dump_location(event))
    print('Attendee : %s' % dump_attendee(event))
    print('Start : %s' % dump_dtstart(event))
    print('End : %s' % dump_dtend(event))

cal = Calendar.from_ical(sys.stdin.read())

# print(cal)
# print(cal.__dict__)

if hasattr(cal, 'subcomponents'):
    for subcomp in cal.subcomponents:
       dump_event(subcomp)
