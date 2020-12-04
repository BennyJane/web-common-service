# !/usr/bin/env python
# -*-coding:utf-8 -*-
# PROJECT    : web-common-service
# Time       ：2020/12/4 11:09
# Warning：The Hard Way Is Easier

# from flask import request, jsonify
# from flask_restful.reqparse import RequestParser
#
# from webAPi.constant import ReqJson
#
#
# class Reqparse(RequestParser):
#     def parse_args(self, req=None, strict=False, http_error_code=400):
#         """Parse all arguments from the provided request and return the results
#         as a Namespace
#
#         :param req: Can be used to overwrite request from Flask
#         :param strict: if req includes args not in parser, throw 400 BadRequest exception
#         :param http_error_code: use custom error code for `flask_restful.abort()`
#         """
#         if req is None:
#             req = request
#
#         namespace = self.namespace_class()
#
#         # A record of arguments not yet parsed; as each is found
#         # among self.args, it will be popped out
#         req.unparsed_arguments = dict(self.argument_class('').source(req)) if strict else {}
#         errors = {}
#         for arg in self.args:
#             value, found = arg.parse(req, self.bundle_errors)
#             if isinstance(value, ValueError):
#                 errors.update(found)
#                 found = None
#             if found or arg.store_missing:
#                 namespace[arg.dest or arg.name] = value
#         if errors:
#             req = ReqJson(code=1, msg='{}'.format(errors.values()[0]))
#             return jsonify(req.result)
#
#         if strict and req.unparsed_arguments:
#             raise Exception('Unknown arguments: %s'
#                             % ', '.join(req.unparsed_arguments.keys()))
#         return namespace
