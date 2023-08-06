from pagarme.resources import handler_request
from pagarme.resources.routes import payable_routes


def find_all():
    return handler_request.get(payable_routes.GET_ALL_PAYABLES)


def find_by(search_params):
    return handler_request.get(payable_routes.GET_PAYABLE_BY, search_params)
