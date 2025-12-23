import uvicorn
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from src.api import app
import os

# Serve static files from the 'public' directory
app.mount("/static", StaticFiles(directory="public"), name="static")

@app.get("/")
async def serve_index():
    """Serve the frontend index.html."""
    return FileResponse(os.path.join("public", "index.html"))

if __name__ == "__main__":
    # In a real environment, you might use environment variables for host/port
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
