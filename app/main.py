from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(
    title="E-Commerce DevOps Application",
    description="Basic E-Commerce API for DevOps Automation Project",
    version="1.0"
)

# -------------------------
# Models
# -------------------------

class Product(BaseModel):
    id: int
    name: str
    price: float
    stock: int


class Customer(BaseModel):
    id: int
    name: str
    email: str


class Order(BaseModel):
    id: int
    customer_id: int
    product_id: int
    quantity: int


# -------------------------
# Temporary Database
# -------------------------

products = []
customers = []
orders = []


# -------------------------
# Home API
# -------------------------

@app.get("/")
def home():
    return {
        "message": "E-Commerce DevOps Application is running",
        "status": "success"
    }


# -------------------------
# Product APIs
# -------------------------

@app.post("/products")
def create_product(product: Product):
    products.append(product)
    return {
        "message": "Product added successfully",
        "product": product
    }


@app.get("/products")
def get_products():
    return products


@app.get("/products/{product_id}")
def get_product(product_id: int):

    for product in products:
        if product.id == product_id:
            return product

    raise HTTPException(
        status_code=404,
        detail="Product not found"
    )


# -------------------------
# Customer APIs
# -------------------------

@app.post("/customers")
def create_customer(customer: Customer):
    customers.append(customer)
    return {
        "message": "Customer added successfully",
        "customer": customer
    }


@app.get("/customers")
def get_customers():
    return customers


@app.get("/customers/{customer_id}")
def get_customer(customer_id: int):

    for customer in customers:
        if customer.id == customer_id:
            return customer

    raise HTTPException(
        status_code=404,
        detail="Customer not found"
    )


# -------------------------
# Order APIs
# -------------------------

@app.post("/orders")
def create_order(order: Order):

    customer_exists = any(
        customer.id == order.customer_id
        for customer in customers
    )

    product = next(
        (product for product in products
         if product.id == order.product_id),
        None
    )

    if not customer_exists:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    if product.stock < order.quantity:
        raise HTTPException(
            status_code=400,
            detail="Insufficient stock"
        )

    product.stock -= order.quantity

    orders.append(order)

    total = product.price * order.quantity

    return {
        "message": "Order created successfully",
        "order": order,
        "total_amount": total
    }


@app.get("/orders")
def get_orders():
    return orders