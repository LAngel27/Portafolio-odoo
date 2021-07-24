odoo.define("pos_stock.models", function (require) {
    "use strict";

    var models = require("point_of_sale.models");
    var modules = models.PosModel.prototype.models;
    var rpc = require("web.rpc");

    models.load_fields("product.product", ["qty_available", "type", "stock_quant_ids"]);

    models.load_models({
        model: "stock.warehouse",
        fields: [],
        loaded: function (self, warehouse) {
            let warehouses = [];
            self.warehouse = warehouses;
            for (let wh of warehouse) {
                self.warehouse.push(wh);
            }
        },
    });

    models.load_models({
        model: "stock.quant",
        fields: [],
        loaded: function (self, stock) {
            let stocks = [];
            self.stock = stocks;
            for (let stk of stock) {
                self.stock.push(stk);
            }
        },
    });

    var _super_order = models.Order.prototype;
    models.Order = models.Order.extend({
        initialize: function (attr, options) {
            _super_order.initialize.call(this, attr, options);
        },
    });

    var OrderlineSuper = models.Orderline.prototype;
    models.Orderline = models.Orderline.extend({
        get_full_product_name: function () {
            if (this.full_product_name) {
                return this.full_product_name;
            }
            var full_name = this.product.display_name;
            if (this.description) {
                full_name += ` (${this.description})`;
            }
            if (this.product.default_code) {
                var code = this.product.default_code;
                return "[" + code + "] " + full_name;
            }
            return full_name;
        },
    });

    var ProductSuper = models.Product.prototype;
    models.Product = models.Product.extend({
        initialize: function (attr, options) {
            ProductSuper.initialize.call(this, attr, options);
        },
        update_quantity: function () {
            debugger;
            let warehouses = this.pos.config.warehouse_ids;
            if (!warehouses.lenght < 1) {
                // pass
            } else {
                for (let wh of warehouses) {
                    console.log(wh);
                }
            }
        },
        // get_stock_available: function () {
        //     let self = this;
        //     return rpc
        //         .query({
        //             model: "product.product",
        //             method: "calculate_qty_sale_available",
        //             args: [[self.id], self.pos.config_id],
        //         })
        //         .then(function (result) {});
        // },
        // get_warehouse_default: function () {
        //     return rpc
        //         .query({
        //             model: "pos.config",
        //             method: "get_warehouse",
        //             args: [self.id],
        //         })
        //         .then(function (result) {
        //             debugger;
        //             console.log(result);
        //         });
        // },
        get_stock_Available: function () {
            let self = this;
            return rpc
                .query({
                    model: "product.product",
                    method: "calculate_qty_sale_available",
                    args: [[self.id], self.pos.config_id],
                })
                .then(function (result) {
                    self.quantity_available = parseInt(result);
                });
        },
    });
});
