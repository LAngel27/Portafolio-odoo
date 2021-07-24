odoo.define("pos_stock.SelectorWarehouseModal", function (require) {
    "use strict";

    const AbstractAwaitablePopup = require("point_of_sale.AbstractAwaitablePopup");
    const Registries = require("point_of_sale.Registries");
    // const { useState } = owl.hooks;
    // const ControlButtonsMixin = require("point_of_sale.ControlButtonsMixin");
    // const NumberBuffer = require("point_of_sale.NumberBuffer");
    // const { useListener } = require("web.custom_hooks");
    // const { onChangeOrder, useBarcodeReader } = require("point_of_sale.custom_hooks");

    class SelectorWarehouseModal extends AbstractAwaitablePopup {
        constructor() {
            super(...arguments);
        }
        get currentOrder() {
            return this.env.pos.get_order();
        }
        close() {
            this.confirm();
        }
        selectItem(itemId, itemName) {
            debugger;
            console.log(itemId);
            console.log(itemName);
            this.confirm();
        }
    }

    // SelectorWarehouseModal.dontShow = false;
    SelectorWarehouseModal.template = "SelectorWarehouseModal";
    SelectorWarehouseModal.defaultProps = {
        confirmText: "",
        cancelText: "",
        títle: "Bodegas disponibles",
    };

    Registries.Component.add(SelectorWarehouseModal);

    return SelectorWarehouseModal;
});
