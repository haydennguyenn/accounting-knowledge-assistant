from fastapi import APIRouter

router = APIRouter(prefix="/api", tags=["integration"])


@router.get("/n8n-test")
def n8n_test():
    return {
        "status": "ok",
        "message": "FastAPI successfully reached from n8n"
    }
