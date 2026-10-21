from fastapi import FastAPI, Request, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI(title="KK Clothes Shop")

# static & templates folders
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


# 1. GET Route: ಫಾರ್ಮ್ ಡಿಸ್‌ಪ್ಲೇ ಮಾಡಲು
@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(
        request=request, 
        name="index.html", 
        context={"message": None}
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

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"message": f"'{item_name}' added successfully!"}
    )