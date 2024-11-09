# -*- coding: utf-8 -*-

from odoo import models, fields, api
import datetime


class MaintenanceEquipment(models.Model):
    _inherit = 'maintenance.equipment'

    product_structure_ids=fields.One2many(
      string='Estructura de productos',
      comodel_name='maintenance.product_list',
      inverse_name='maintenance_equipment_id',
      store=True,
      copied=True
    )

    def get_next_working_day(self, date, working_days):
      if date.weekday() not in working_days:
        new_date_interval = 7 - date.weekday() + int(min(working_days))
        return date + datetime.timedelta(days=new_date_interval)
      return date

    def get_date_after_holiday(self, date, working_days, holiday_days):
      for h_day in holiday_days:
        if h_day[0] <= date <= h_day[1]:
          next_day = h_day[1] + datetime.timedelta(days=1)
          date = self.get_valid_date(next_day, working_days, holiday_days)
      return date

    def get_valid_date(self, date, working_days, holiday_days):
      new_date = self.get_next_working_day(date, working_days)
      return self.get_date_after_holiday(new_date, working_days, holiday_days)

    def get_forbidden_days(self, working_calendar):
      working_days = []
      holidays_arr = []
      for element in working_calendar.attendance_ids:
        working_days.append(int(element.dayofweek))
      for element in working_calendar.leave_ids:
        holidays_arr.append((element.date_from.date(), element.date_to.date()))
      return working_days, holidays_arr

    def get_current_calendar(self):
      domain = [("id", "=", self.env.company.resource_calendar_id.id)]
      return self.env["resource.calendar"].search(domain)

    def _create_new_request(self, mtn_plan):
        working_calendar = self.get_current_calendar()
        working_days, holiday_days = self.get_forbidden_days(working_calendar)

        # Compute horizon date adding to today the planning horizon
        horizon_date = fields.Date.today() + mtn_plan.get_relativedelta(
            mtn_plan.maintenance_plan_horizon, mtn_plan.planning_step or "year"
        )
        horizon_date = self.get_valid_date(horizon_date, working_days, holiday_days)
        # We check maintenance request already created and create until
        # planning horizon is met
        start_maintenance_date_plan = mtn_plan.start_maintenance_date
        furthest_maintenance_request = self.env["maintenance.request"].search(
            [
                ("maintenance_plan_id", "=", mtn_plan.id),
                ("request_date", ">=", start_maintenance_date_plan),
            ],
            order="request_date desc",
            limit=1,
        )
        if furthest_maintenance_request:
            next_maintenance_date = (
                furthest_maintenance_request.request_date
                + mtn_plan.get_relativedelta(
                    mtn_plan.interval, mtn_plan.interval_step or "year"
                )
            )
        else:
            next_maintenance_date = mtn_plan.next_maintenance_date
        requests = self.env["maintenance.request"]
        # Create maintenance request until we reach planning horizon
        while next_maintenance_date <= horizon_date:
            next_maintenance_date = self.get_valid_date( next_maintenance_date, working_days, holiday_days)
            if next_maintenance_date >= fields.Date.today():
                curr_time = datetime.datetime.now(datetime.timezone.utc).time()
                vals = self._prepare_request_from_plan(mtn_plan, next_maintenance_date)
                vals['schedule_date'] = datetime.datetime.combine(vals['schedule_date'], curr_time)
                requests |= self.env["maintenance.request"].create(vals)
            next_maintenance_date = next_maintenance_date + mtn_plan.get_relativedelta(
                mtn_plan.interval, mtn_plan.interval_step or "year"
            )
        return requests