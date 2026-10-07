# MRP: PLM CE

Community Edition port of the `mrp_plm` module.

Product Lifecycle Management (PLM) adds Engineering Change Orders (ECO)
on top of the bill of materials and products.

- Versioning of bills of materials and products.
- Configurable approval flows depending on the type of change order.
- ECO stages, types, tags and approval templates.
- BoM and routing changes attached to an ECO.
- Document links on products and BoMs.
- BoM structure report extended with version / ECO columns.

## Origin

Ported from the upstream `mrp_plm`. The port is
behaviour-preserving: models, views, security and assets are kept as-is;
only the license, the module name and the xmlid/JS namespace were changed.

The module has no technical dependency on proprietary modules — every referenced
model exists in the Community Edition core (`mrp.bom`, `mrp.bom.byproduct`,
`report.mrp.report_bom_structure`, `product.document`, ...). The BoM
structure report inherits the core `mrp.report_mrp_bom` view unchanged.
