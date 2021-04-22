/*jshint esversion: 6 */
odoo.define('cap_levage_portal.materiel_edit_portal', function (require) {
    'use strict';

    let publicWidget = require('web.public.widget');

    publicWidget.registry.CapLevageEditMaterielWidget = publicWidget.Widget.extend({
        selector: '#materiel_edit_form',
        events: {
            "change #materiel_edit_category_select": "_onCategoryChange",
            "click #materiel_submit_button": "_onSubmitClick",
        },
        read_events: {
            "click #upload_certificat_fabrication_files": "_onUploadDocClick",
            "click #upload_certificat_controle_files": "_onUploadDocClick",
            "click #upload_certificat_destruction_files": "_onUploadDocClick",
            "change input[name='upload_certificat_fabrication_files']": "_onUploadChange",
            "change input[name='upload_certificat_controle_files']": "_onUploadChange",
            "change input[name='upload_certificat_destruction_files']": "_onUploadChange",
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
            this.$categorySelector = this.$('select[name="category_id"]');
            this.$categorySelectorOptions = this.$categorySelector.find('option');
            this._showCorrectParams(true);
            return rel;
        },

        //--------------------------------------------------------------------------
        // Private
        //--------------------------------------------------------------------------

        /**
         * @private
         */
        _showCorrectParams: function (firstSet = false) {
            let selectedVal = this.$categorySelector.val();
            let elementList = ["nombre_brins", "longueur", "cmu", "tmu", "model", "diametre", "grade", "num_lot", "num_commande"];
            if (selectedVal !== "") {
                let $selectedCategory = this.$categorySelectorOptions.filter('[value=' + selectedVal + ']:first');
                elementList.forEach(item => this._showOrHideDiv($selectedCategory, item, firstSet));
            } else {
                elementList.forEach(item => this._set_divs_attr(item, true, 0, firstSet));
            }
        },

        _set_divs_attr(nameValue, isHidden, periodeValue, firstSet) {
            const divId = "#materiel_".concat(nameValue);
            const inputIdId = "#materiel_input_".concat(nameValue);
            const periodeDivId = "#periode";
            let $concernedDiv = this.$(divId);
            let $concernedInput = this.$(inputIdId);
            let $periodeInput = this.$(periodeDivId);
            $concernedDiv.attr('hidden', isHidden);
            $concernedInput.attr('disabled', isHidden);
            if (periodeValue !== 0) {
                if (!firstSet) {
                    $periodeInput.attr('value', periodeValue);
                }
                $periodeInput.attr('required', false);
            } else {
                $periodeInput.attr('value', "");
                $periodeInput.attr('required', true);

            }
        },

        _showOrHideDiv: function (selectedCategory, nameValue, firstSet) {
            const displayAttr = "data-display_".concat(nameValue);
            let showDiv = selectedCategory.attr(displayAttr) !== "true";
            let periodeValue = selectedCategory.attr("data-periode");
            this._set_divs_attr(nameValue, showDiv, periodeValue, firstSet);
        },

        //--------------------------------------------------------------------------
        // Handlers
        //--------------------------------------------------------------------------

        /**
         * @private
         */
        _onCategoryChange: function () {
            this._showCorrectParams();
        },
        _onUploadDocClick: function (ev) {
            ev.preventDefault();
            $(ev.currentTarget).closest('div[name="uploadDiv"]').find('input').trigger('click');
        },
        _onUploadChange: function (ev) {
            if (!ev.currentTarget.files.length) {
                return;
            }
            let $div = $(ev.currentTarget).closest('div[name="uploadDiv"]');
            $div.find('span[name="uploadFileName"]').text(ev.currentTarget.files[0].name);
        },
        _onSubmitClick: function (ev) {
            $('input:invalid').each(function () {
                // Find the tab-pane that this element is inside, and get the id
                var $closest = $(this).closest('.tab-pane');
                var id = $closest.attr('id');

                // Find the link that corresponds to the pane and have it show
                $('.nav a[href="#' + id + '"]').tab('show');

                // Only want to do it once
                return false;
            });
            $('select:invalid').each(function () {
                // Find the tab-pane that this element is inside, and get the id
                var $closest = $(this).closest('.tab-pane');
                var id = $closest.attr('id');

                // Find the link that corresponds to the pane and have it show
                $('.nav a[href="#' + id + '"]').tab('show');

                // Only want to do it once
                return false;
            });
        }
    });
    return publicWidget.registry.CapLevageEditMaterielWidget;
});
