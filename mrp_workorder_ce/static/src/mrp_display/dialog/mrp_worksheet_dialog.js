/** @odoo-module */

import { ConfirmationDialog } from "@web/core/confirmation_dialog/confirmation_dialog";
import DocumentViewer from '@mrp_workorder_ce/components/viewer';

export class MrpWorksheetDialog extends ConfirmationDialog {
    static props = {
        ...ConfirmationDialog.props,
        body: { optional: true },
        worksheetData: [Object, Boolean],
        worksheetText: Object,
    };
    static template = "mrp_workorder_ce.MrpWorksheetDialog";
    static components = {
        ...ConfirmationDialog.components,
        DocumentViewer,
    };
}
