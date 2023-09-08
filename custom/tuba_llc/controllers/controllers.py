# -*- coding: utf-8 -*-
# from odoo import http


# class TubaLlc(http.Controller):
#     @http.route('/tuba_llc/tuba_llc', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/tuba_llc/tuba_llc/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('tuba_llc.listing', {
#             'root': '/tuba_llc/tuba_llc',
#             'objects': http.request.env['tuba_llc.tuba_llc'].search([]),
#         })

#     @http.route('/tuba_llc/tuba_llc/objects/<model("tuba_llc.tuba_llc"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('tuba_llc.object', {
#             'object': obj
#         })
