"""
  created by IAmFiveHigh on 2020-01-03
 """
from flask import Blueprint


class RedPrint:
    def __init__(self, name):
        self.name = name
        self.mound = []

    def route(self, rule, **options):
        def decorator(f):
            self.mound.append((rule, f, options))
            return f
        return decorator

    def register(self, bp: Blueprint, url_prefix=None):
        if url_prefix is None:
            url_prefix = '/' + self.name
        for rule, f, options in self.mound:
            endpoint = options.pop('endpoint', f.__name__)
            bp.add_url_rule(url_prefix + rule, endpoint, f, **options)
