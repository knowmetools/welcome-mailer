#! /usr/bin/env python

from welcome_mailer import handler


def handle(event, context):
    handler.lambda_handler(event, context)
