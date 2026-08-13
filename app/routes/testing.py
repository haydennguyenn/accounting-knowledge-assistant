from fastapi import APIRouter

router = APIRouter()

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