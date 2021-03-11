/*jshint esversion: 6 */
odoo.define('cap_levage.materiel_edit_portal', function (require) {
    'use strict';

    let publicWidget = require('web.public.widget');

    publicWidget.registry.CapLevageEditMaterielWidget = publicWidget.Widget.extend({
        selector: '#materiel_edit_form',
        events: {
            "change #materiel_edit_category_select": "_onCategoryChange",
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
            if (selectedVal !== "") {
                let $selectedCategory = this.$categorySelectorOptions.filter('[value=' + selectedVal + ']:first');
                let elementList = ["nombre_brins", "longueur", "cmu", "tmu", "model", "diametre", "grade", "num_lot", "num_commande"];
                elementList.forEach(item => this._showOrHideDiv($selectedCategory, item));
            }
        },

        _showOrHideDiv: function (selectedCategory, nameValue) {
            const divId = "#materiel_".concat(nameValue);
            const inputIdId = "#materiel_input_".concat(nameValue);
            const displayAttr = "data-display_".concat(nameValue);

            let $concernedDiv = this.$(divId);
            let $concernedInput = this.$(inputIdId);
            let showDiv = selectedCategory.attr(displayAttr) !== "true";
            $concernedDiv.attr('hidden', showDiv);
            $concernedInput.attr('disabled', showDiv);
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
    });
    return publicWidget.registry.CapLevageEditMaterielWidget;
});
