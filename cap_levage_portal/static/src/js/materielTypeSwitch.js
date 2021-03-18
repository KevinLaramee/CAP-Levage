/*jshint esversion: 6 */
odoo.define('cap_levage.materiel_edit_portal', function (require) {
    'use strict';

    let publicWidget = require('web.public.widget');

    publicWidget.registry.CapLevageEditMaterielWidget = publicWidget.Widget.extend({
        selector: '#materiel_edit_form',
        events: {
            "change #materiel_edit_category_select": "_onCategoryChange",
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
            this._showCorrectParams();
            return rel;
        },

        //--------------------------------------------------------------------------
        // Private
        //--------------------------------------------------------------------------

        /**
         * @private
         */
        _showCorrectParams: function () {
            let selectedVal = this.$categorySelector.val();
            let elementList = ["nombre_brins", "longueur", "cmu", "tmu", "model", "diametre", "grade", "num_lot", "num_commande"];
            if (selectedVal !== "") {
                let $selectedCategory = this.$categorySelectorOptions.filter('[value=' + selectedVal + ']:first');
                elementList.forEach(item => this._showOrHideDiv($selectedCategory, item));
            }
            else {
                elementList.forEach(item => this._set_divs_attr(item, true));
            }
        },

        _set_divs_attr(nameValue, isHidden){
                const divId = "#materiel_".concat(nameValue);
                const inputIdId = "#materiel_input_".concat(nameValue);
                let $concernedDiv = this.$(divId);
                let $concernedInput = this.$(inputIdId);
                $concernedDiv.attr('hidden', isHidden);
                $concernedInput.attr('disabled', isHidden);
        },

        _showOrHideDiv: function (selectedCategory, nameValue) {
            const displayAttr = "data-display_".concat(nameValue);
            let showDiv = selectedCategory.attr(displayAttr) !== "true";
            this._set_divs_attr(nameValue, showDiv);
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
    });
    return publicWidget.registry.CapLevageEditMaterielWidget;
});
