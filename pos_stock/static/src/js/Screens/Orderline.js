odoo.define("pos_stock.OrderlineDetails", function (require) {
    "use strict";

    const OrderlineDetails = require("point_of_sale.OrderlineDetails");
    const Registries = require("point_of_sale.Registries");

    const CodeOrderlineDetails = (OrderlineDetails) => class extends OrderlineDetails {};

    Registries.Component.extend(OrderlineDetails, CodeOrderlineDetails);
    return CodeOrderlineDetails;
});
