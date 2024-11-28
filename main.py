from fastapi import FastAPI
from routes.purchase import router

app = FastAPI()

# Include the purchase route module
app.include_router(router)
