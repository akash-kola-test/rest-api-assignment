from typing import List, Dict
import logging
from .config import LOGGER_NAME
from .models import Customer
from .customer_repository import CustomerRepository
from . import customer_mapper
from .exceptions import InvalidPageException, InvalidCustomerIdException, CustomerNotFoundException


class CustomerService:

    def __init__(self, customer_repository: CustomerRepository):
        self.customer_repository = customer_repository
        self.logger = logging.getLogger(LOGGER_NAME)

    def get_customers(self, page) -> List[Customer]:
        self.logger.info("Requested page is: %s", page)
        if page <= 0:
            self.logger.error(f"Not able to access the given page {page}, as it is invalid")
            raise InvalidPageException(f"Not able to access the given page {page}, as it is invalid")

        self.logger.debug("fetching customer records")
        customers_records = self.customer_repository.get_customers(page)
        self.logger.debug("%s records retrieved", len(customers_records))

        self.logger.debug("mapping customer records to customer objects")
        customers = customer_mapper.customer_record_to_object_mapper(customers_records)

        self.logger.info("successfully retrieved customers")
        return customers

    def add_customer(self, customer_data: Dict[str, str]):
        customer_id = customer_data.get('customer_id')
        self.logger.info("Requested to add customer with customer id %s", customer_id)
        if customer_id is None or len(customer_id) == 0:
            self.logger.error("Customer id not available or the provided one is invalid")
            raise InvalidCustomerIdException("Customer id not available or the provided one is invalid")

        self.logger.debug("mapping data to customer object")
        customer = customer_mapper.customer_data_to_object_mapper(customer_data)

        self.logger.debug("Adding customer")
        self.customer_repository.add_customer(customer)
        self.logger.info("Added customer")

    def update_customer(self, customer_id: str, customer_data: Dict[str, str]):
        self.logger.info("Requested to update customer with customer id %s", customer_id)
        if not self.customer_repository.is_customer_exist(customer_id):
            self.logger.error("customer not found with id %s", customer_id)
            raise CustomerNotFoundException(f"customer not found with id {customer_id}")

        self.customer_repository.update_customer(customer_id, customer_data)
        self.logger.info("update request for customer with customer id %s is successful", customer_id)
