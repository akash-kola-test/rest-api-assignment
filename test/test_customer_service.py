from unittest.mock import Mock

import pytest

from src.app.customer_service import CustomerService
from src.app.customer_repository import CustomerRepository
from src.app.exceptions import *


def test_get_customers():
    page_number = 10
    expected_result = []
    customer_repository_mock = Mock(spec=CustomerRepository)
    customer_repository_mock.get_customers.return_value = expected_result

    customer_service = CustomerService(customer_repository_mock)
    result = customer_service.get_customers(page_number)

    assert result == expected_result
    customer_repository_mock.get_customers.assert_called_once_with(page_number)


def test_invalid_page_raises_exception():
    page_number = -1

    customer_repository_mock = Mock(spec=CustomerRepository)
    customer_service = CustomerService(customer_repository_mock)

    with pytest.raises(InvalidPageException):
        customer_service.get_customers(page_number)

    customer_repository_mock.get_customers.assert_not_called()


def test_creation_of_customer():
    customer_repository_mock = Mock(spec=CustomerRepository)
    customer_repository_mock.is_customer_exist.return_value = False

    customer_service = CustomerService(customer_repository_mock)
    customer_data = {
        "customer_id": "123"
    }

    customer_service.add_customer(customer_data)
    customer_repository_mock.is_customer_exist.assert_called_once_with("123")
    customer_repository_mock.add_customer.assert_called_once()


def test_customer_creation_fails_if_customer_id_exists():
    customer_repository_mock = Mock(spec=CustomerRepository)
    customer_repository_mock.is_customer_exist.return_value = True

    customer_service = CustomerService(customer_repository_mock)
    customer_data = {
        "customer_id": "123"
    }

    with pytest.raises(CustomerIdTakenException):
        customer_service.add_customer(customer_data)


def test_customer_creation_fails_if_customer_id_is_invalid():
    customer_repository_mock = Mock(spec=CustomerRepository)
    customer_repository_mock.is_customer_exist.return_value = False

    customer_service = CustomerService(customer_repository_mock)
    customer_data = {
        "customer_id": ""
    }

    with pytest.raises(InvalidCustomerIdException):
        customer_service.add_customer(customer_data)


def test_customer_update():
    customer_repository_mock = Mock(spec=CustomerRepository)
    customer_repository_mock.is_customer_exist.return_value = True

    customer_service = CustomerService(customer_repository_mock)
    customer_id = "123"
    customer_data = {
        "company_name": "something"
    }

    customer_service.update_customer(customer_id, customer_data)


def test_customer_update_fails_if_customer_id_not_found():
    customer_repository_mock = Mock(spec=CustomerRepository)
    customer_repository_mock.is_customer_exist.return_value = False

    customer_service = CustomerService(customer_repository_mock)
    customer_id = "123"
    customer_data = {
        "company_name": "something"
    }

    with pytest.raises(CustomerNotFoundException):
        customer_service.update_customer(customer_id, customer_data)
