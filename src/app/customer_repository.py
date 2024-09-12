from psycopg2 import pool
from typing import List, Dict
from .models import Customer
import logging


class CustomerRepository:


    def __init__(self):
        conn_params = {
            'dbname': 'northwind',
            'host': 'localhost',
            'port': '5433',
            'user': 'yugabyte',
            'password': '',
        }
        self.conn_pool = pool.ThreadedConnectionPool(3, 20, **conn_params)
        self.logger = logging.getLogger("my-app")


    def get_customers(self, page=1, page_size=15) -> List[Customer]:
        if page_size <= 0:
            page_size = 15

        customer_output_attributes = [
            "c.customer_id",
            "c.company_name",
            "c.contact_name",
            "c.contact_title",
            "c.address",
            "c.city",
            "c.region",
            "c.postal_code",
            "c.country",
            "c.phone",
            "c.fax",
        ]
        customer_demographics_output_attributes = [
            "cd.customer_type_id",
            "cd.customer_desc",
        ]
        output_attributes = (customer_output_attributes
                             + customer_demographics_output_attributes)
        select_clause_attributes = ", ".join(output_attributes)

        query = f"""SELECT {select_clause_attributes} FROM customers c
        LEFT JOIN customer_customer_demo ccd ON c.customer_id = ccd.customer_id
        LEFT JOIN customer_demographics cd ON ccd.customer_type_id = cd.customer_type_id
        ORDER BY c.customer_id
        LIMIT %s
        OFFSET %s
        """

        with self.conn_pool.getconn() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (page_size, (page - 1) * page_size))
                results = cursor.fetchall()
            self.conn_pool.putconn(connection)

        return results

    def add_customer(self, customer: Customer):

        query = """INSERT INTO customers
        (customer_id, company_name, contact_name, contact_title, address, city, region, postal_code, country, phone, fax) 
        VALUES
        (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        with self.conn_pool.getconn() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (
                    customer.customer_id,
                    customer.company_name,
                    customer.contact_name,
                    customer.contact_title,
                    customer.address,
                    customer.city,
                    customer.region,
                    customer.postal_code,
                    customer.country,
                    customer.phone,
                    customer.fax
                ))
                connection.commit()
            self.conn_pool.putconn(connection)

    def update_customer(self, customer_id: str, customer_data: Dict[str, str]):
        set_clause = []
        values = []

        keys = [
            'company_name',
            'contact_name',
            'contact_title',
            'address',
            'city',
            'region',
            'postal_code',
            'country',
            'phone',
            'fax'
        ]

        for key in keys:
            if key in customer_data:
                set_clause.append(f"{key} = %s")
                values.append(customer_data[key])

        set_clause_str = ", ".join(set_clause)
        query = f"UPDATE customers SET {set_clause_str} WHERE customer_id = %s"
        values.append(customer_id)

        with self.conn_pool.getconn() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, values)
                connection.commit()
            self.conn_pool.putconn(connection)


    def is_customer_exist(self, customer_id: str) -> bool:
        query = "SELECT 1 FROM customer WHERE customer_id = %s"
        with self.conn_pool.getconn() as connection:
            with connection.cursor() as cursor:
                records = cursor.execute(query, (customer_id,))
            self.conn_pool.putconn(connection)

        return len(records) == 1
