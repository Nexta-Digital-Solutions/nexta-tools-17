/* @odoo-module */

import { patch } from "@web/core/utils/patch";
import { UserAgent } from "@voip/core/user_agent_service";

patch(UserAgent.prototype, {
    async _onIncomingInvitation(inviteSession) {
        if (this.session && this.session._state == "Terminated"){
            this.session = null;
        }
        if (this.session) {
            inviteSession.reject({ statusCode: 486 /* Busy Here */ });
            return;
        }
        if (this.voip.settings.should_auto_reject_incoming_calls) {
            inviteSession.reject({ statusCode: 488 /* Not Acceptable Here */ });
            return;
        }
        const phoneNumber = inviteSession.remoteIdentity.uri.user;
        const call = await this.callService.create({
            direction: "incoming",
            phone_number: phoneNumber,
            state: "calling",
        });
        this.softphone.selectCorrespondence({ call });
        inviteSession.delegate = this.sessionDelegate;
        inviteSession.incomingInviteRequest.delegate = {
            onCancel: (message) => this._onIncomingInvitationCanceled(message),
        };
        inviteSession.stateChange.addListener((state) => this._onSessionStateChange(state));
        this.session = {
            call,
            isMute: false,
            sipSession: inviteSession,
        };
        this.softphone.show();
        this.ringtoneService.incoming.play();
        // TODO send notification
    }
})   
