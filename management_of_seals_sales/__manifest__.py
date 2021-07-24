# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

{
    "name": "Management of seals sales",

    "author": "LAngel Cartaya",

    "summary": "Modulo creado para gestion de precintos en el modulo de ventas de la empresa soloalfombras",

    "description": "Creacion y gestion",

    "depends": ['base', 'sale', 'project'],


    "data": [
        'security/seals_security.xml',
        'wizard/sequence_creator_view.xml',
        'views/sale_order_inh_view.xml',
        'views/seal_management_view.xml',
        'views/project_task_inh_view.xml',
        'security/ir.model.access.csv',
    ],


    "installable": True,

}
