from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from chainlit.utils import mount_chainlit

from app.routes.upload import router as upload_router
from app.routes.testing import router as testing_router

app = FastAPI()

# Routers for file upload and LLM testing endpoints
app.include_router(upload_router)
app.include_router(testing_router)

@app.get("/")
def root():
    return RedirectResponse(url="/chat")


# Mount the Chainlit app located at app/chainlit/chainlit_app.py -> needs to be last
mount_chainlit(app=app, target="app/chainlit/chainlit_app.py", path="/chat")
