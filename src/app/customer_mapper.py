from typing import List, Dict
from .models import Customer, CustomerDemographic


def customer_record_to_object_mapper(records) -> List[Customer]:
    customer_map = {}
    for record in records:
        customer_id = record[0]
        if customer_id not in customer_map:
            customer_map[customer_id] = Customer(
                customer_id=customer_id,
                company_name=record[1],
                contact_name=record[2],
                contact_title=record[3],
                address=record[4],
                city=record[5],
                region=record[6],
                postal_code=record[7],
                country=record[8],
                phone=record[9],
                fax=record[10],
                customer_demographics=[]
            )

        customer_demographic = CustomerDemographic(
            customer_type_id=record[11],
            customer_desc=record[12],
            customers=None
        )

        if customer_demographic.customer_type_id:
            customer_map[customer_id].customer_demographics.append(customer_demographic)

    return list(customer_map.values())


def customer_data_to_object_mapper(data: Dict[str, str]) -> Customer:
    return Customer(
        customer_id=data.get('customer_id'),
        company_name=data.get('company_name'),
        contact_name=data.get('contact_name'),
        contact_title=data.get('contact_title'),
        address=data.get('address'),
        city=data.get('city'),
        region=data.get('region'),
        postal_code=data.get('postal_code'),
        country=data.get('country'),
        phone=data.get('phone'),
        fax=data.get('fax'),
        customer_demographics=None
    )
