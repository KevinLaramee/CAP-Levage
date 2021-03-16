/*jshint esversion: 6 */
odoo.define('cap_levage.materiel_edit_portal', function (require) {
    'use strict';

    let publicWidget = require('web.public.widget');

    publicWidget.registry.CapLevageQrCodeScanningWidget = publicWidget.Widget.extend({
        selector: '#qrcodescan',
        events: {
            "click #buttonqrcodescan": "_onQrCodeScan",
            "click #qrcode_popup": "_onStopScanClick",
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
            this.$qrcodePopUp = this.$("#qrcode_popup");
            this.$qrcodePopUp.hide();
            return rel;
        },

        //--------------------------------------------------------------------------
        // Private
        //--------------------------------------------------------------------------

        /**
         * @private
         */

        _launchCamera: function () {
            this.$qrcodePopUp.show();
            Html5Qrcode.getCameras().then(devices => {
                /**
                 * devices would be an array of objects of type:
                 * { id: "id", label: "label" }
                 */
                if (devices && devices.length) {
                    const qrCodeSuccessCallback = qrMessage => {
                        this._stopScanning(html5QrCode);
                        window.location.href = "/cap_levage_portal/materiels?search_in=allid&search=" + qrMessage;
                    };
                    const qrCodeFailureCallback = errorMessage => {
                        // console.error("on_qrcode_scan_error", errorMessage);
                    };
                    const config = {fps: 1, qrbox: 150};
                    const html5QrCode = new Html5Qrcode("reader");
                    html5QrCode.start({ facingMode: "environment" }, config, qrCodeSuccessCallback, qrCodeFailureCallback)
                        .catch(err => {
                            console.error("start_qrcode_scan_error", err);
                            this._stopScanning(html5QrCode);
                        });
                }
            }).catch(err => {
                console.error("get_camera_error", err);
                this._stopScanning(null);
            });
        },

        _stopScanning: function (html5QrCode) {
            this.$qrcodePopUp.hide();
            if (html5QrCode !== null) {
                html5QrCode.stop().then(ignore => {
                    // QR Code scanning is stopped.
                }).catch(err => {
                    // Stop failed, handle it.
                });
            }
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
        /**
         * @private
         */
        _onStopScanClick: function () {
            console.log("stop scan");
            this._stopScanning(null);
        },
    });
    return publicWidget.registry.CapLevageQrCodeScanningWidget;
});
