from fastapi import APIRouter

router = APIRouter()
#TODO: connect HTML template to return value 2, make index.html with navigation pages included: testing.pyç, upload.py, chainlit_app.py
@router.get("/testing")
def testing_page():
    return {"message": "Template for LLM testing endpoint."}


# Examples
# @router.get("/testing")
# def testing_page():
#     ...

# @router.post("/testing")
# def run_test():
#     ...