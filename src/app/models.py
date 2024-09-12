from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List


@dataclass
class CustomerDemographic:
    customer_type_id: str
    customer_desc: str
    customers: Optional[List['Customer']]


@dataclass
class Customer:
    customer_id: str
    company_name: str
    contact_name: str
    contact_title: str
    address: str
    city: str
    region: str
    postal_code: str
    country: str
    phone: str
    fax: str
    customer_demographics: Optional[List[CustomerDemographic]]


@dataclass
class Category:
    category_id: int
    category_name: str
    description: str
    picture: bytes


@dataclass
class Supplier:
    supplier_id: int
    company_name: str
    contact_name: str
    contact_title: str
    address: str
    city: str
    region: str
    postal_code: str
    country: str
    phone: str
    fax: str
    homepage: str


@dataclass
class Product:
    product_id: int
    product_name: str
    supplier_id: int
    category_id: int
    quantity_per_unit: str
    unit_price: float
    units_in_stock: int
    units_on_order: int
    reorder_level: int
    discontinued: int
    category: Category
    supplier: Supplier


@dataclass
class Employee:
    employee_id: int
    last_name: str
    first_name: str
    title: str
    title_of_courtesy: str
    birth_date: datetime
    hire_date: datetime
    address: str
    city: str
    region: str
    postal_code: str
    country: str
    home_phone: str
    extension: str
    photo: bytes
    notes: str
    reports_to: int
    photo_path: str
    manager: 'Employee'
    territories: List['Territory']


@dataclass
class Region:
    region_id: int
    region_description: str


@dataclass
class Territory:
    territory_id: str
    territory_description: str
    region_id: int
    region: Region
    employees: List[Employee]


@dataclass
class Shipper:
    shipper_id: int
    company_name: str
    phone: str


@dataclass
class Order:
    order_id: int
    customer_id: str
    employee_id: int
    order_date: datetime
    required_date: datetime
    shipped_date: datetime
    ship_via: int
    freight: float
    ship_name: str
    ship_address: str
    ship_city: str
    ship_region: str
    ship_postal_code: str
    ship_country: str
    customer: Customer
    employee: Employee
    shipper: Shipper


@dataclass
class OrderDetail:
    order_id: int
    product_id: int
    unit_price: float
    quantity: int
    discount: float
    product: Product
    order: Order
