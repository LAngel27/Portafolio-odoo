odoo.define("pos_stock.ProductItem", function (require) {
    "use strict";

    const ProductItem = require("point_of_sale.ProductItem");
    const Registries = require("point_of_sale.Registries");
    const { useState } = owl.hooks;

    const StockProductItem = (ProductItem) =>
        class extends ProductItem {
            get stockAvailable() {
                this.props.product.updateQuantity();
                return this.props.product.quantity_available;
            }
            get updateStockChange() {
                this.props.product.updateStockChange();
                return this.props.product.otherStockQuantity;
            }
        };

    Registries.Component.extend(ProductItem, StockProductItem);
    return StockProductItem;
});
