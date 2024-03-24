/** @odoo-module */

import { DocumentsInspector } from "@documents/views/inspector/documents_inspector";
import { patch } from "@web/core/utils/patch";
import { useService } from "@web/core/utils/hooks";
import { FormViewDialog } from '@web/views/view_dialogs/form_view_dialog';
import { session } from "@web/session";
import { Dialog } from "@web/core/dialog/dialog";
import { _t } from "@web/core/l10n/translation";


patch(DocumentsInspector.prototype, {

    async onSharedUsers(ev){
        ev.preventDefault();
        ev.stopPropagation();

        if (!this.props.selection.length) {
            return;
        }

        if (this.props.selection.length > 1){
            Dialog.alert(this, _t('Please select just one document.'));
            return;
        }
        
        if (this.props.selection[0].data.owner_id[0] != session.uid){
            Dialog.alert(this, _t('Sharing document belonging to others is prohibited.'));
            return;
        }

        if (!this.resIds[0]){
            return;
        }

        const record = this.props.selection[0];
        this.dialogService.add(FormViewDialog, {
            title: this.env._t('Share a file with another user'),
            resModel: 'documents.document',
            resId: this.resIds[0],
            context: {
                form_view_ref: 'documents_portal_management_ee.document_view_form_shared_users',
            },
            onRecordSaved: async (result) => await record.model.load(),
        });
    }
});