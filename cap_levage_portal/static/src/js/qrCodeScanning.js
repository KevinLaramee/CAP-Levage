/*jshint esversion: 6 */
odoo.define('cap_levage.materiel_edit_portal', function (require) {
    'use strict';

    let publicWidget = require('web.public.widget');

    publicWidget.registry.CapLevageQrCodeScanningWidget = publicWidget.Widget.extend({
        selector: '#qrcodescan',
        events: {
            "click #buttonqrcodescan": "_onQrCodeScan",
        },

        /**
         * @override
         * @param {Object} [options]
         * @param {Object} [options.examples]
         */
        init: function (parent, options) {
            this._super(parent);
        },
        /**
         * @override
         */
        start: function () {
            let rel = this._super.apply(this, arguments);
            return rel;
        },

        //--------------------------------------------------------------------------
        // Private
        //--------------------------------------------------------------------------

        /**
         * @private
         */

        _launchCamera: function () {
            function onScanSuccess(qrMessage) {
                // handle the scanned code as you like
                window.location.href = "/cap_levage_portal/materiels?search_in=allid&search="+qrMessage;
            }

            function onScanFailure(error) {
            }

            let html5QrcodeScanner = new Html5QrcodeScanner(
                "reader", {fps: 10, qrbox: 250}, /* verbose= */ true);
            html5QrcodeScanner.render(onScanSuccess, onScanFailure);
        },

        //--------------------------------------------------------------------------
        // Handlers
        //--------------------------------------------------------------------------

        /**
         * @private
         */
        _onQrCodeScan: function () {
            this._launchCamera();
        },
    });
    return publicWidget.registry.CapLevageQrCodeScanningWidget;
});
