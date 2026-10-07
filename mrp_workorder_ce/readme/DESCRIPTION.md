# MRP: Work Orders CE

Community Edition port of the planning half of the `mrp_workorder` module (MRP II).

## What it provides

- **Planning by Production** — work order Gantt grouped by manufacturing
  order.
- **Planning by Workcenter** — work order Gantt grouped by workcenter,
  with workcenter unavailability shading and a workcenter progress bar
  (planned hours / work hours).
- Both views are also available with **operation dependencies** enabled
  (`blocked_by_workorder_ids` / `needed_by_workorder_ids`), showing the
  dependency connectors between pills.
- **Drag to reschedule** — dragging a pill snaps the work order to the
  first available slot of its workcenter, preserving the duration.

The views are reached from *Manufacturing ▸ Planning ▸ Work Orders*.

## What it does not provide

The **Shop Floor / MES** tablet application is **not** part of this
module. It is step 2 of the change and is blocked by the quality fork
(`quality-ce`). See `openspec/changes/mrp-workorder-ce` in the planning
repository.

## Dependencies

- `mrp` — the work order model, the actions and the planning menu.
- `web_gantt_ce` — the CE Gantt view and its rescheduling hooks
  (`_gantt_reschedule_*`).
- `web_tour`, `barcodes` — as in the upstream module.
- `hr_hourly_cost` — employee hourly cost, as in the upstream module.

## Origin

Ported from the upstream `mrp_workorder`. Only the Gantt views,
the planning menus, the workcenter progress bar / unavailability and the
rescheduling hooks are ported. The upstream rescheduling API
(`_web_gantt_reschedule_*`) is replaced by the `web_gantt_ce` hooks; the
behaviour is preserved:

| Upstream API | Community Edition |
|---|---|
| `_web_gantt_reschedule_is_record_candidate` | `_gantt_reschedule_is_candidate` |
| `_web_gantt_reschedule_compute_dates` | `_gantt_reschedule_compute_dates` |
| `_web_gantt_reschedule_write_new_dates` | `_gantt_reschedule_write_dates` |
| `_web_gantt_reschedule_is_relation_candidate` | `_gantt_reschedule_relations` |

The four `quality.point.test_type` records (`register_consumed_materials`,
`register_production`, `register_byproducts`, `print_label`) are defined in
`mrp_workorder` in the upstream module but belong to the `quality.point.test_type`
model from `quality_ce`. They are loaded by `post_init_hook` only when that
model is registered, so this module installs without the quality fork.
