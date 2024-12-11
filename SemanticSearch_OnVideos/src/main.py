from fastapi import FastAPI
from inference import Inference

app = FastAPI()
inference = Inference()

@app.post("/process_query")
async def process_query(query: str):
    response = inference.llm_ans(query)
    return {"response": response}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)
