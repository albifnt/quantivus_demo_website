from fastapi import FastAPI, Request, Form, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import uvicorn

app = FastAPI()

# Templates directory setup
templates = Jinja2Templates(directory="templates")

# Mount static assets
app.mount("/assets", StaticFiles(directory="assets"), name="assets")

# Predefined credentials
VALID_USERNAME = "admin"
VALID_PASSWORD = "password123"

# Route for the landing page
@app.get("/", include_in_schema=False)
async def read_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Route for the login page
@app.get("/login.html", include_in_schema=False)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

# Route to handle login form submission
@app.post("/login_action", include_in_schema=False)
async def login_action(request: Request, username: str = Form(...), password: str = Form(...)):
    if username == VALID_USERNAME and password == VALID_PASSWORD:
        return RedirectResponse(url="/user.html", status_code=status.HTTP_303_SEE_OTHER)
    else:
        # On failure, reload login page with error message
        return templates.TemplateResponse("login.html", {"request": request, "error": "Invalid credentials, please try again."})

# Route for the user page
@app.get("/user.html", include_in_schema=False)
async def user_page(request: Request):
    return templates.TemplateResponse("user.html", {"request": request})

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
