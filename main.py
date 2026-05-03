from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

from database import engine, SessionLocal
from models import Product, Base

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


@app.get("/")
def home(request: Request):

    db = SessionLocal()

    products = db.query(Product).all()

    return templates.TemplateResponse(
    request=request,
    name="index.html",
    context={
        "request": request,
        "products": products
    }
)


@app.get("/product/{product_id}")
def product_page(request: Request, product_id: int):

    db = SessionLocal()

    product = db.query(Product).filter(Product.id == product_id).first()

    return templates.TemplateResponse(
        "product.html",
        {
            "request": request,
            "product": product
        }
    )


@app.get("/contact")
def contact(request: Request):

    return templates.TemplateResponse(
        "contact.html",
        {
            "request": request
        }
    )


@app.get("/admin")
def admin_page(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="admin.html",
        context={
            "request": request
        }
    )


@app.post("/add-product")
def add_product(
    name: str = Form(...),
    price: str = Form(...),
    image: str = Form(...),
    description: str = Form(...)
):

    db = SessionLocal()

    new_product = Product(
        name=name,
        price=price,
        image=image,
        description=description
    )

    db.add(new_product)

    db.commit()

    return RedirectResponse(
        url="/",
        status_code=303
    )