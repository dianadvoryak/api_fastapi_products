from shift_assignment.router import router as router_shift_assignment

from fastapi import FastAPI


app = FastAPI(
    title="App"
)

app.include_router(router_shift_assignment)

@app.get("/")
def unprotected_route():
    return f"Hello, anonym"

