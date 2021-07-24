odoo.define("pos_stock.SetWarenhouseStockButton", function (require) {
    "use strict";

    const { Gui } = require("point_of_sale.Gui");
    const PosComponent = require("point_of_sale.PosComponent");
    const Registries = require("point_of_sale.Registries");
    const AbstractAwaitablePopup = require("point_of_sale.AbstractAwaitablePopup");
    const core = require("web.core");
    const _t = core._t;
    const ProductItem = require("point_of_sale.ProductItem");
    const ProductScreen = require("point_of_sale.ProductScreen");

    class SetWarenhouseStockButton extends PosComponent {
        display_popup_warehouse() {
            Gui.showPopup("SelectorWarehouseModal", {
                title: _t("Bodegas Disponibles"),
                confirmText: _t("Confirmar"),
                cancelText: _t("Salir"),
            });
        }
    }

    SetWarenhouseStockButton.template = "SetWarenhouseStockButton";

    ProductScreen.addControlButton({
        component: SetWarenhouseStockButton,
        condition: function () {
            return this.env.pos;
        },
        position: ["before", "SetPricelistButton"],
    });

    Registries.Component.add(SetWarenhouseStockButton);

    return SetWarenhouseStockButton;
});
