# -*- coding: utf-8 -*-
# Copyright (C) 2026 Vertel AB
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from collections import defaultdict
from datetime import datetime, timedelta

from pytz import utc

from odoo import api, fields, models, _
from odoo.addons.resource.models.utils import Intervals, sum_intervals


class MrpWorkorder(models.Model):
    """Work order planning (Gantt) on Community Edition.

    Ported from the planning half of the upstream ``mrp_workorder``.
# The rescheduling hooks are the Community Edition equivalents
    from ``web_gantt_ce``: ``_gantt_reschedule_is_candidate``,
    ``_gantt_reschedule_compute_dates``, ``_gantt_reschedule_write_dates``
    and ``_gantt_reschedule_relations``.
    """

    _name = 'mrp.workorder'
    _inherit = ['mrp.workorder', 'gantt.mixin']

    def _gantt_reschedule_is_candidate(self, date_start_field, date_stop_field):
        return self.state not in ['progress', 'done', 'cancel'] \
            and super()._gantt_reschedule_is_candidate(date_start_field, date_stop_field)

    def _gantt_reschedule_compute_dates(self, date_candidate, search_forward,
                                        date_start_field, date_stop_field,
                                        reschedule_method=None):
        from_date, to_date = self.workcenter_id._get_first_available_slot(
            date_candidate, self.duration_expected,
            forward=search_forward, leaves_to_ignore=self.leave_id,
        )
        return from_date, to_date

    def _gantt_reschedule_write_dates(self, start, stop, date_start_field, date_stop_field):
        return super(
            MrpWorkorder,
            self.with_context(bypass_duration_calculation=True),
        )._gantt_reschedule_write_dates(start, stop, date_start_field, date_stop_field)

    def _gantt_reschedule_relations(self, dependency_field, dependency_inverted_field,
                                    search_forward, reschedule_method=None):
        field_name = dependency_inverted_field if search_forward else dependency_field
        return self[field_name] if field_name else self.browse()

    def _gantt_progress_bar_workcenter_id(self, res_ids, start, stop):
        """Planned hours per workcenter, against the workcenter work hours.

        ``value`` is the time the open work orders of the workcenter overlap
        the visible range, ``max_value`` is the workcenter's own work hours
        in that range.
        """
        self.env['mrp.workorder'].check_access('read')
        workcenters = self.env['mrp.workcenter'].search([('id', 'in', res_ids)])
        workorders = self.env['mrp.workorder'].search([
            ('workcenter_id', 'in', res_ids),
            ('state', 'not in', ['done', 'cancel']),
            ('date_start', '<=', stop.replace(tzinfo=None)),
            ('date_finished', '>=', start.replace(tzinfo=None)),
        ])
        planned_hours = defaultdict(float)
        workcenters_work_intervals, dummy = workcenters.resource_id._get_valid_work_intervals(start, stop)
        for workorder in workorders:
            max_start = max(start, utc.localize(workorder.date_start))
            min_finished = min(stop, utc.localize(workorder.date_finished))
            interval = Intervals([(max_start, min_finished, self.env['resource.calendar.attendance'])])
            work_intervals = interval & workcenters_work_intervals[workorder.workcenter_id.resource_id.id]
            planned_hours[workorder.workcenter_id] += sum_intervals(work_intervals)
        work_hours = {
            id: sum_intervals(work_intervals) for id, work_intervals in workcenters_work_intervals.items()
        }
        return {
            workcenter.id: {
                'value': planned_hours[workcenter],
                'max_value': work_hours.get(workcenter.resource_id.id, 0.0),
            }
            for workcenter in workcenters
        }

    @api.model
    def _gantt_progress_bar(self, field, res_ids, start, stop):
        start, stop = utc.localize(start), utc.localize(stop)
        today = datetime.now(utc).replace(hour=0, minute=0, second=0, microsecond=0)
        start = max(start, today)
        if field == 'workcenter_id':
            return dict(
                self._gantt_progress_bar_workcenter_id(res_ids, start, stop),
                warning=_("This workcenter isn't expected to have open workorders during this period. Work hours :"),
            )
        raise NotImplementedError("This Progress Bar is not implemented.")

    @api.model
    def _gantt_unavailability(self, field, res_ids, start, stop, scale):
        """Workcenter availability is shown as unavailability in the Gantt."""
        if field != 'workcenter_id':
            return super()._gantt_unavailability(field, res_ids, start, stop, scale)

        workcenters = self.env['mrp.workcenter'].browse(res_ids)
        unavailability_mapping = workcenters._get_unavailability_intervals(start, stop)

        result = {}
        for workcenter in workcenters:
            result[workcenter.id] = [
                {'start': interval[0], 'stop': interval[1]}
                for interval in unavailability_mapping[workcenter.id]
            ]
        return result

    @api.model
    def action_mrp_workorder_dependencies(self, action_name):
        """Open the work order planning action with the dependency Gantt.

        The Gantt view with ``dependency_field`` is only used when the user
        belongs to ``mrp.group_mrp_workorder_dependencies``; otherwise the
        action keeps the plain Gantt that ``mrp_workorder_ce`` puts first.
        """
        action = self.env['ir.actions.act_window']._for_xml_id(
            'mrp.action_mrp_workorder_%s' % action_name)
        ref = 'mrp_workorder_ce.workcenter_line_gantt_production_dependencies' \
            if action_name == 'production' \
            else 'mrp_workorder_ce.mrp_workorder_view_gantt_dependencies'

        if self.env.user.has_group('mrp.group_mrp_workorder_dependencies'):
            action['views'] = [(self.env.ref(ref).id, 'gantt')] + [
                (id, kind) for id, kind in action['views'] if kind != 'gantt'
            ]
        return action
