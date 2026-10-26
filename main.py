from fastapi import FastAPI, Request, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from database import add_product_to_db, get_all_products, sell_product , delete_product,get_sales_summary
from database import add_product_to_db, get_all_products

app = FastAPI(title="KK Clothes Shop")

# static & templates folders
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/")
def home(request: Request, search: str = "", category: str = ""):
    products = get_all_products(search=search, category=category)

    total_items = len(products)
    total_quantity = sum(p["quantity"] for p in products)
    total_investment = sum(p["cost_price"] * p["quantity"] for p in products)

    sales_data = get_sales_summary()

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "products": products,
            "total_items": total_items,
            "total_quantity": total_quantity,
            "total_investment": round(total_investment, 2),
            "total_sales_count": sales_data["total_sales_count"],
            "total_profit": round(sales_data["total_profit"], 2),
            "search": search,  # Keep the search term in the search bar
            "category": category,      # Keep the selected category in the dropdown
        },
    )

@app.post("/add-product")
def add_product(
    request: Request,
    item_name: str = Form(...),
    category: str = Form(...),
    size: str = Form(...),
    cost_price: float = Form(...),
    selling_price: float = Form(...),
    quantity: int = Form(...)
):
    print(f"\n>>> RECEIVED: {item_name} | {category} | Qty: {quantity} <<<", flush=True)
    # Add product to the database
    add_product_to_db(item_name, category, size, cost_price, selling_price, quantity)
    products = get_all_products()
    total_items = len(products)
    total_quantity = sum(p["quantity"] for p in products)
    total_investment = sum(p["cost_price"] * p["quantity"] for p in products)

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "message": f"'{item_name}' added successfully!",
            "products": products,
            "total_items": total_items,
            "total_quantity": total_quantity,
            "total_investment": round(total_investment, 2),
        },
    )

@app.post("/sell/{product_id}")
def sell(product_id: int):
    sell_product(product_id)
    return RedirectResponse(url ="/", status_code=303)

@app.post("/delete/{product_id}")
def delete(product_id: int):
    delete_product(product_id)
    return RedirectResponse(url ="/", status_code=303)