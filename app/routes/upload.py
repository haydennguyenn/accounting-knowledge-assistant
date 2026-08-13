from fastapi import APIRouter

router = APIRouter()

@router.get("/upload")
def upload_page():
    return {"message": "Template for file upload endpoint."}

# Examples
# @router.get("/upload")
# def upload_page():
#     ...

# @router.post("/upload")
# def upload_document():
#     ...