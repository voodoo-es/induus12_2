# -*- coding: utf-8 -*-
# © 2018 Ingetive - <info@ingetive.com>

import logging
import pytz

from datetime import datetime, timedelta
from dateutil import parser
from odoo import models, fields, api

_logger = logging.getLogger(__name__)


class GoogleCalendar(models.AbstractModel):
    _inherit = 'google.calendar'

    def update_from_google(self, event, single_event_dict, type):
        """ Update an event in Odoo with information from google calendar
            :param event : record od calendar.event to update
            :param single_event_dict : dict of google cal event data
        """
        CalendarEvent = self.env['calendar.event'].with_context(no_mail_to_attendees=True)
        ResPartner = self.env['res.partner']
        CalendarAlarm = self.env['calendar.alarm']
        attendee_record = []
        alarm_record = set()
        partner_record = [(4, self.env.user.partner_id.id)]
        result = {}

        if self.get_need_synchro_attendee():
            for google_attendee in single_event_dict.get('attendees', []):
                partner_email = google_attendee.get('email')
                if type == "write":
                    for oe_attendee in event['attendee_ids']:
                        if oe_attendee.email == google_attendee['email']:
                            oe_attendee.write({'state': google_attendee['responseStatus'],
                                               'google_internal_event_id': single_event_dict.get('id')})
                            google_attendee['found'] = True
                            continue

                if google_attendee.get('found'):
                    continue

                attendee = ResPartner.search([('email', '=ilike', google_attendee['email']), ('user_ids', '!=', False)],
                                             limit=1)
                if not attendee:
                    attendee = ResPartner.search([('email', '=ilike', google_attendee['email'])], limit=1)
                if not attendee:
                    data = {
                        'email': partner_email,
                        'customer': False,
                        'is_company': False,
                        'name': google_attendee.get("displayName", False) or partner_email
                    }
                    attendee = ResPartner.create(data)
                attendee = attendee.read(['email'])[0]
                partner_record.append((4, attendee.get('id')))
                attendee['partner_id'] = attendee.pop('id')
                attendee['state'] = google_attendee['responseStatus']
                attendee_record.append((0, 0, attendee))
        for google_alarm in single_event_dict.get('reminders', {}).get('overrides', []):
            alarm = CalendarAlarm.search(
                [
                    ('type', '=', google_alarm['method'] if google_alarm['method'] == 'email' else 'notification'),
                    ('duration_minutes', '=', google_alarm['minutes'])
                ], limit=1
            )
            if not alarm:
                data = {
                    'type': google_alarm['method'] if google_alarm['method'] == 'email' else 'notification',
                    'duration': google_alarm['minutes'],
                    'interval': 'minutes',
                    'name': "%s minutes - %s" % (google_alarm['minutes'], google_alarm['method'])
                }
                alarm = CalendarAlarm.create(data)
            alarm_record.add(alarm.id)

        UTC = pytz.timezone('UTC')
        if single_event_dict.get('start') and single_event_dict.get('end'):  # If not cancelled

            if single_event_dict['start'].get('dateTime', False) and single_event_dict['end'].get('dateTime', False):
                date = parser.parse(single_event_dict['start']['dateTime'])
                stop = parser.parse(single_event_dict['end']['dateTime'])
                date = str(date.astimezone(UTC))[:-6]
                stop = str(stop.astimezone(UTC))[:-6]
                allday = False
            else:
                date = single_event_dict['start']['date']
                stop = single_event_dict['end']['date']
                d_end = fields.Date.from_string(stop)
                allday = True
                d_end = d_end + timedelta(days=-1)
                stop = fields.Date.to_string(d_end)

            update_date = datetime.strptime(single_event_dict['updated'], "%Y-%m-%dT%H:%M:%S.%fz")
            result.update({
                'start': date,
                'stop': stop,
                'allday': allday
            })
        result.update({
            'attendee_ids': attendee_record,
            'partner_ids': list(set(partner_record)),
            'alarm_ids': [(6, 0, list(alarm_record))],

            'name': single_event_dict.get('summary', 'Event'),
            'description': single_event_dict.get('description', False),
            'location': single_event_dict.get('location', False),
            'privacy': single_event_dict.get('visibility', 'public'),
            'oe_update_date': update_date,
        })

        if single_event_dict.get("recurrence", False):
            rrule = [rule for rule in single_event_dict["recurrence"] if rule.startswith("RRULE:")][0][6:]
            result['rrule'] = rrule
        if type == "write":
            res = CalendarEvent.browse(event['id']).write(result)
        elif type == "copy":
            result['recurrency'] = True
            res = CalendarEvent.browse([event['id']]).write(result)
        elif type == "create":
            res = CalendarEvent.create(result).id

        if self.env.context.get('curr_attendee'):
            self.env['calendar.attendee'].with_context(no_mail_to_attendees=True).browse(
                [self.env.context['curr_attendee']]).write(
                {'oe_synchro_date': update_date, 'google_internal_event_id': single_event_dict.get('id', False)})
        return res
