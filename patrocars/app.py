from fastapi import FastAPI

app = FastAPI()


@app.get("/montadoras")
def montadora_list():
    pass
