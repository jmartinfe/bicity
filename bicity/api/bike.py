from fastapi import APIRouter

router = APIRouter(prefix="/bike", tags=["bike"])

@router.get("/health")
def health_check():
    return {"status": "ok"}