odoo.define("pos_stock.ProductScreen", function (require) {
    "use strict";

    const ProductScreen = require("point_of_sale.ProductScreen");
    const Registries = require("point_of_sale.Registries");
    const NumberBuffer = require("point_of_sale.NumberBuffer");

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
                debugger;
                let valuesReject = this.validatorStockAvailable();
                if (this.env.pos.config.show_stock_product_none) {
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
                } else {
                    this.showScreen("PaymentScreen");
                }
            }
            async _clickProduct(event) {
                if (this.env.pos.config.show_stock_product_none) {
                    if (event.detail.quantity_available === 0) {
                        await this.showPopup("ErrorPopup", {
                            title: this.env._t("Error"),
                            body: this.env._t(`El producto que a selecionado ${event.detail.display_name} no tiene una cantidad disponible`),
                        });
                    } else {
                        // pass
                    }
                }
                if (!this.currentOrder) {
                    this.env.pos.add_new_order();
                }
                const product = event.detail;
                let price_extra = 0.0;
                let draftPackLotLines, weight, description, packLotLinesToEdit;

                if (this.env.pos.config.product_configurator && _.some(product.attribute_line_ids, (id) => id in this.env.pos.attributes_by_ptal_id)) {
                    let attributes = _.map(product.attribute_line_ids, (id) => this.env.pos.attributes_by_ptal_id[id]).filter((attr) => attr !== undefined);
                    let { confirmed, payload } = await this.showPopup("ProductConfiguratorPopup", {
                        product: product,
                        attributes: attributes,
                    });

                    if (confirmed) {
                        description = payload.selected_attributes.join(", ");
                        price_extra += payload.price_extra;
                    } else {
                        return;
                    }
                }

                // Gather lot information if required.
                if (["serial", "lot"].includes(product.tracking) && (this.env.pos.picking_type.use_create_lots || this.env.pos.picking_type.use_existing_lots)) {
                    const isAllowOnlyOneLot = product.isAllowOnlyOneLot();
                    if (isAllowOnlyOneLot) {
                        packLotLinesToEdit = [];
                    } else {
                        const orderline = this.currentOrder
                            .get_orderlines()
                            .filter((line) => !line.get_discount())
                            .find((line) => line.product.id === product.id);
                        if (orderline) {
                            packLotLinesToEdit = orderline.getPackLotLinesToEdit();
                        } else {
                            packLotLinesToEdit = [];
                        }
                    }
                    const { confirmed, payload } = await this.showPopup("EditListPopup", {
                        title: this.env._t("Lot/Serial Number(s) Required"),
                        isSingleItem: isAllowOnlyOneLot,
                        array: packLotLinesToEdit,
                    });
                    if (confirmed) {
                        // Segregate the old and new packlot lines
                        const modifiedPackLotLines = Object.fromEntries(payload.newArray.filter((item) => item.id).map((item) => [item.id, item.text]));
                        const newPackLotLines = payload.newArray.filter((item) => !item.id).map((item) => ({ lot_name: item.text }));

                        draftPackLotLines = { modifiedPackLotLines, newPackLotLines };
                    } else {
                        // We don't proceed on adding product.
                        return;
                    }
                }

                // Take the weight if necessary.
                if (product.to_weight && this.env.pos.config.iface_electronic_scale) {
                    // Show the ScaleScreen to weigh the product.
                    if (this.isScaleAvailable) {
                        const { confirmed, payload } = await this.showTempScreen("ScaleScreen", {
                            product,
                        });
                        if (confirmed) {
                            weight = payload.weight;
                        } else {
                            // do not add the product;
                            return;
                        }
                    } else {
                        await this._onScaleNotAvailable();
                    }
                }

                // Add the product after having the extra information.
                this.currentOrder.add_product(product, {
                    draftPackLotLines,
                    description: description,
                    price_extra: price_extra,
                    quantity: weight,
                });

                NumberBuffer.reset();
            }
        };

    Registries.Component.extend(ProductScreen, ProductScreenInh);
    return ProductScreenInh;
});
