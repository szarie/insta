from fastapi import APIRouter
from fastapi.responses import JSONResponse

from .extractors import ExtractionError, extract_description
from .models import ExtractRequest, ExtractResponse

router = APIRouter()


@router.post("/extract", response_model=ExtractResponse)
def extract(request: ExtractRequest) -> ExtractResponse | JSONResponse:
    try:
        platform, description = extract_description(request.url)
    except ExtractionError as exc:
        return JSONResponse(status_code=422, content={"detail": str(exc)})
    return ExtractResponse(
        platform=platform, url=request.url.strip(), description=description
    )
