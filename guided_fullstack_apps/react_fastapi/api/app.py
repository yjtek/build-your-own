from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from models import (
    supplier_pydantic,
    supplier_pydanticIn,
    Supplier,
    product_pydanticIn,
    product_pydantic,
    Products
)

# Email
from typing import List

from fastapi import BackgroundTasks, FastAPI
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from pydantic import BaseModel, EmailStr
from starlette.responses import JSONResponse

from dotenv import dotenv_values
from fastapi.middleware.cors import CORSMiddleware

## uvicorn app:app --reload

creds: dict = dotenv_values(".env")

class EmailSchema(BaseModel):
    email: List[EmailStr]

class EmailContent(BaseModel):
    message: str
    subject: str

conf = ConnectionConfig(
    MAIL_USERNAME =creds.get("EMAIL", ''),
    MAIL_PASSWORD = creds.get("PASSWORD", ''),
    MAIL_FROM = creds.get("EMAIL", ''),
    MAIL_PORT = 465, 
    MAIL_SERVER = "smtp.gmail.com",
    MAIL_STARTTLS = False,
    MAIL_SSL_TLS = True,
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = True
)

app = FastAPI()

origins = [
    'http://localhost:3000',
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_headers=['*'],
    allow_methods=['*']
) 

@app.post('email/{product_id}')
async def send_email(product_id: int, content: EmailContent):
    product = await Products.get(id = product_id)
    supplier = await product.supplied_by
    supplier_email = [supplier.email]
   
    html = """
        <p>Thanks for using Fastapi-mail</p> 
        <p>{content.subject}</p>
        <p>{content.message}</p>
    """

    message = MessageSchema(
        subject="Fastapi-Mail module",
        recipients=supplier_email,
        body=html,
        subtype=MessageType.html
    )

    fm = FastMail(conf)
    await fm.send_message(message)
    return {'status': 'ok'}

@app.get('/')
def index():
    return {"Msg": 'Go to /docs or /redoc for API documentation'}

@app.post('/supplier')
async def add_supplier(supplier_info: supplier_pydanticIn):
    supplier_obj = await Supplier.create(**supplier_info.dict(exclude_unset=True))
    response = await supplier_pydantic.from_tortoise_orm(supplier_obj)
    return {"status": "ok", "data": response}

@app.get('/supplier')
async def get_all_suppliers():
    response = await supplier_pydantic.from_queryset(Supplier.all())
    return {"status": "ok", "data": response}

@app.get('/supplier/{supplier_id}')
async def get_specific_supplier(supplier_id: int):
    response = await supplier_pydantic.from_queryset_single(Supplier.get(id=supplier_id))
    return {"status": "ok", "data": response}

@app.put('/supplier/{supplier_id}')
async def update_supplier(supplier_id: int, update_info: supplier_pydanticIn):
    supplier = await Supplier.get(id=supplier_id)
    update_info = update_info.dict(exclude_unset=True)
    supplier.name = update_info.get("name")
    supplier.company = update_info.get("company")
    supplier.phone = update_info.get("phone")
    supplier.email = update_info.get("email")
    await supplier.save()

    response = await supplier_pydantic.from_tortoise_orm(supplier)
    return {"status": "ok", "data": response}

@app.delete('/supplier/{supplier_id}')
async def delete_supplier(supplier_id: int):
    await Supplier.get(id=supplier_id).delete()
    return {'status': 'ok'}

@app.post('/product/{supplier_id}')
async def add_product(supplier_id: int, products_details: product_pydanticIn):
    supplier = await Supplier.get(id=supplier_id)
    product = products_details.dict(exclude_unset=True)
    product["revenue"] += product.get('quantity_sold', 1) * product.get('unit_price', 1)
    product_obj = await Products.create(**product, supplied_by=supplier)
    response = await product_pydantic.from_tortoise_orm(product_obj)
    return {'status': 'ok', "data": response}

@app.get('/product')
async def all_products():
    response = await product_pydantic.from_queryset(Products.all())
    return {'status': 'ok', 'data': response}

@app.get('/product/{id}')
async def specific_product(id: int):
    response = await product_pydantic.from_queryset_single(Products.get(id=id))
    return {'status': 'ok', 'data': response}

@app.put('/product/{id}')
async def update_product(id: int, update_info: product_pydanticIn):
    product = await Products.get(id=id)
    update_info = update_info.dict(exclude_unset=True)
    product.name = update_info['name']
    product.quantity_in_stock = update_info['quantity_in_stock']
    product.revenue += update_info['quantity_sold'] * update_info['unit_price']
    product.quantity_sold += update_info['quantity_sold'] 
    product.unit_price += update_info['unit_price']

    await product.save()
    response = await product_pydantic.from_tortoise_orm(product)
    return {'status': 'ok', 'data': response}

@app.delete('/product/{id}')
async def delete_product(id: int):
    await Products.filter(id=id).delete()
    return {'status': 'ok'}

register_tortoise(
    app,
    db_url="sqlite://database.sqlite3",
    modules={"models": ["models"]},
    generate_schemas=True,
    add_exception_handlers=True
)