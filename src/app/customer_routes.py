from flask import Blueprint, request
import logging

from .config import LOGGER_NAME
from .customer_service import CustomerService
from .customer_repository import CustomerRepository
from .exceptions import CustomerNotFoundException, InvalidCustomerIdException, InvalidPageException


blue_print = Blueprint("customer", __name__)
logger = logging.getLogger(LOGGER_NAME)


@blue_print.get("/customers")
def get_customers():
    page = request.args.get('page', 1, int)
    try:
        customer_service = CustomerService(CustomerRepository())
        result = customer_service.get_customers(page)
        return result
    except InvalidPageException:
        logger.exception(f"Error while fetching customers at page {page}")
        return {"error": "Invalid page"}, 400
    except Exception:
        logger.exception("Error while fetching customers")
        return {"error": "something went wrong"}, 500


@blue_print.post("/customers")
def add_customer():
    try:
        customer_service = CustomerService(CustomerRepository())
        customer_data = request.get_json()
        customer_service.add_customer(customer_data)
        return {"message": "added customer"}, 201
    except InvalidCustomerIdException:
        logger.exception("Invalid customer_id provided")
        return {"error": "please provide valid customer id"}, 400
    except Exception:
        logger.exception("Error while fetching customers")
        return {"error": "something went wrong"}, 500


@blue_print.patch("/customers/<customer_id>")
def update_customer(customer_id):
    try:
        customer_service = CustomerService(CustomerRepository())
        customer_data = request.get_json()
        customer_service.update_customer(customer_id, customer_data)
        return {"message": "updated customer"}, 204
    except CustomerNotFoundException:
        logger.exception(f"customer not found with id {customer_id}")
        return {"error": "please provide valid customer id"}, 400
    except Exception:
        logger.exception("Error while fetching customers")
        return {"error": "something went wrong"}, 500
