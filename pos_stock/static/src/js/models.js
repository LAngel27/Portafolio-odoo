odoo.define("pos_stock.models", function (require) {
    "use strict";

    var models = require("point_of_sale.models");
    var modules = models.PosModel.prototype.models;
    var rpc = require("web.rpc");

    models.load_fields("product.product", ["qty_available", "type", "stock_quant_ids"]);
    models.load_fields("stock.picking.type", ["warehouse_id", "default_location_src_id"]);

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
            this.quantity_available = this.quantity_available || 0;
            this.otherStockQuantity = this.otherStockQuantity || 0;
        },
        updateQuantity: function () {
            // let self = [this];
            // let configWarehouse = this.pos.picking_type.warehouse_id;
            let configLocation = this.pos.picking_type.default_location_src_id;
            let stockFilter = this.pos.stock.filter((item) => item.location_id[0] === configLocation[0] && this.id === item.product_id[0]);
            if (stockFilter.length >= 1) {
                stockFilter.forEach((item) => {
                    this.quantity_available = item.available_quantity;
                });
            } else {
                // pass
            }
        },
        updateStockChange: function () {
            let configWarehouse = this.pos.picking_type.warehouse_id;
            let configLocation = this.pos.picking_type.default_location_src_id;
            let warehouseChange = this.pos.config.warehouse_change;
            if (warehouseChange) {
                if (warehouseChange.id != configWarehouse[0]) {
                    let warehouseFilter = this.pos.warehouse.filter((item) => item.id === warehouseChange.id && item.active);
                    let stockFilter = this.pos.stock.filter((item) => item.location_id[0] === warehouseFilter[0].lot_stock_id[0] && this.id === item.product_id[0]);
                    if (stockFilter.length === 1) {
                        this.otherStockQuantity = stockFilter[0].available_quantity;
                    } else {
                        this.otherStockQuantity = 0;
                    }
                } else {
                    this.otherStockQuantity = 0;
                }
            } else {
                // pass
            }
        },
        // get_stock_Available: function () {
        //     let self = this;
        //     return rpc
        //         .query({
        //             model: "product.product",
        //             method: "calculate_qty_sale_available",
        //             args: [[self.id], self.pos.config_id],
        //         })
        //         .then(function (result) {
        //             self.quantity_available = parseInt(result);
        //         });
        // },
    });
});
