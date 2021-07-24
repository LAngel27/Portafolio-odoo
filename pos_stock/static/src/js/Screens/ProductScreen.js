odoo.define("pos_stock.ProductScreen", function (require) {
    "use strict";

    const ProductScreen = require("point_of_sale.ProductScreen");
    const Registries = require("point_of_sale.Registries");

    const ProductScreenInh = (ProductScreen) =>
        class extends ProductScreen {
            validatorStockAvailable() {
                let orderLinesReject = [];
                let orderList = this.env.pos.get_order_list();
                for (const order of orderList) {
                    for (const line of order.orderlines.models) {
                        if (line.quantity <= line.product.quantity_available) {
                            // pass
                        } else {
                            let lineOrderObj = {
                                name: line.product.display_name,
                                quantityOrder: line.quantity,
                                quantityAvailableStock: line.product.quantity_available,
                            };
                            orderLinesReject.push(lineOrderObj);
                        }
                    }
                }
                return orderLinesReject;
            }
            _onClickPay() {
                let valuesReject = this.validatorStockAvailable();

                if (valuesReject.length >= 1) {
                    const getProducts = () => {
                        let products = [];
                        for (const value of valuesReject) {
                            products.push(value.name);
                        }
                        return products;
                    };
                    this.showPopup("ErrorPopup", {
                        title: this.env._t("Error"),
                        body: this.env._t(`En los siguientes productos a  ha sobrepasado la cantidad de stock disponible:  \n ${getProducts().join(",")}`),
                    });
                } else {
                    this.showScreen("PaymentScreen");
                }
            }
        };

    Registries.Component.extend(ProductScreen, ProductScreenInh);
    return ProductScreenInh;
});
