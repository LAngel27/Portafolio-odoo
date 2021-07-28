odoo.define("post_stock.SetPricelistButton", function (require) {
    "use strict";

    const SetPricelistButton = require("point_of_sale.SetPricelistButton");
    const { useListener } = require("web.custom_hooks");
    const Registries = require("point_of_sale.Registries");

    const SetPricelistButtonInh = (SetPricelistButton) => class extends SetPricelistButton {};

    Registries.Component.extend(SetPricelistButton, SetPricelistButtonInh);
    return SetPricelistButtonInh;
});
