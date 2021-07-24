odoo.define("pos_stock.ProductItem", function (require) {
    "use strict";

    const ProductItem = require("point_of_sale.ProductItem");
    const Registries = require("point_of_sale.Registries");

    const StockProductItem = (ProductItem) =>
        class extends ProductItem {
            get stockAvailable() {
                this.props.product.update_quantity();
                // this.props.product.get_config();
                this.props.product.get_stock_Available();
                return this.props.product.qty_available;
            }
        };

    Registries.Component.extend(ProductItem, StockProductItem);
    return StockProductItem;
});
