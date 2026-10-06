import uuid
from pathlib import Path

from fastapi import FastAPI, Request, Form, UploadFile, File
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .database import init_db, add_recommendation
from .models import HomeBudgetInput, PartyBudgetInput
from .recommendations import home, party, jewelry


BASE = Path(__file__).resolve().parent.parent

UPLOADS = BASE / "uploads"
UPLOADS.mkdir(exist_ok=True)

app = FastAPI(
    title="PocketSmart AI",
    version="1.0"
)

app.mount(
    "/static",
    StaticFiles(directory=BASE / "app" / "static"),
    name="static"
)

templates = Jinja2Templates(
    directory=BASE / "app" / "templates"
)

init_db()


def render(request: Request, name, **ctx):
    return templates.TemplateResponse(
        request=request,
        name=name,
        context=ctx
    )


# ---------------------------------------------------------
# HOME PAGE
# ---------------------------------------------------------

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return render(request, "index.html")


# ---------------------------------------------------------
# HOME INTERIOR PLANNER
# ---------------------------------------------------------

@app.get("/home-planner", response_class=HTMLResponse)
async def home_page(request: Request):
    return render(
        request,
        "home_planner.html"
    )


@app.post("/home-budget")
async def home_budget(request: Request):

    data = await request.json()

    d = HomeBudgetInput.model_validate(data)

    result = home(d)

    recommendation_id = str(uuid.uuid4())

    # Save recommendation without requiring a user account
    try:
        add_recommendation(
            recommendation_id,
            "guest",
            "Home Interior",
            f"₹{d.total_budget:,.0f} home budget",
            result
        )
    except Exception:
        pass

    return {
        "id": recommendation_id,
        "result": result
    }


# ---------------------------------------------------------
# PARTY PLANNER
# ---------------------------------------------------------

@app.get("/party-planner", response_class=HTMLResponse)
async def party_page(request: Request):
    return render(
        request,
        "party_planner.html"
    )


@app.post("/party-budget")
async def party_budget(request: Request):

    data = await request.json()

    d = PartyBudgetInput.model_validate(data)

    result = party(d)

    recommendation_id = str(uuid.uuid4())

    try:
        add_recommendation(
            recommendation_id,
            "guest",
            "Party Planning",
            f"₹{d.total_budget:,.0f} "
            f"{d.party_type} party • "
            f"{d.num_guests} guests",
            result
        )
    except Exception:
        pass

    return {
        "id": recommendation_id,
        "result": result
    }


# ---------------------------------------------------------
# JEWELRY PLANNER
# ---------------------------------------------------------

@app.get("/jewelry-planner", response_class=HTMLResponse)
async def jewelry_page(request: Request):
    return render(
        request,
        "jewelry_planner.html"
    )


@app.post("/jewelry-budget")
async def jewelry_budget(
    request: Request,
    total_budget: float = Form(...),
    occasion: str = Form(...),
    jewelry_type: str = Form(...),
    preferences: str = Form(""),
    outfit_image: UploadFile | None = File(None)
):

    path = None

    # Handle optional outfit image
    if outfit_image and outfit_image.filename:

        ext = Path(
            outfit_image.filename
        ).suffix.lower()

        if ext not in {
            ".jpg",
            ".jpeg",
            ".png",
            ".webp"
        }:
            return JSONResponse(
                {
                    "error":
                    "Use JPG, JPEG, PNG or WEBP."
                },
                status_code=400
            )

        if (
            outfit_image.size
            and outfit_image.size > 5 * 1024 * 1024
        ):
            return JSONResponse(
                {
                    "error":
                    "Image must be 5 MB or smaller."
                },
                status_code=400
            )

        path = UPLOADS / (
            uuid.uuid4().hex + ext
        )

        path.write_bytes(
            await outfit_image.read()
        )

    try:

        result = jewelry(
            total_budget,
            occasion,
            jewelry_type,
            preferences,
            path
        )

    finally:

        if path:
            path.unlink(
                missing_ok=True
            )

    recommendation_id = str(uuid.uuid4())

    try:
        add_recommendation(
            recommendation_id,
            "guest",
            "Jewelry Planning",
            f"₹{total_budget:,.0f} "
            f"jewelry budget • {occasion}",
            result
        )
    except Exception:
        pass

    return {
        "id": recommendation_id,
        "result": result
    }


# ---------------------------------------------------------
# HEALTH CHECK
# ---------------------------------------------------------

@app.get("/api/health")
async def health():

    return {
        "status": "ok",
        "app": "PocketSmart AI"
    }