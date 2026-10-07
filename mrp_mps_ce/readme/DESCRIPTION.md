# MRP: Master Production Schedule CE

Community Edition port of the `mrp_mps` module.

Master Production Schedule (MPS) lets you plan production and purchase
orders against a sales forecast, before the actual demand exists.

- Forecast-based master planning per product / warehouse.
- Safety stock and min/max supply levels.
- Manual override of the quantity to procure.
- Forecast details and replenishment proposals (wizards).
- Automatic replenishment of schedules via a daily cron.

## Origin

Ported from the upstream `mrp_mps`. The port is
behaviour-preserving: models, views, security and assets are kept as-is;
only the license, the module name and the xmlid/JS namespace were changed.

The module has no technical dependency on proprietary modules — every referenced
model exists in the Community Edition core (`stock.replenish.mixin`,
`mrp.bom`, `report.mrp.report_bom_structure`, `product.document`, ...).
