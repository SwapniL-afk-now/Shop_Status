import uvicorn
import os
import nest_asyncio
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from src.api import app

# Apply nest_asyncio to support running in notebook environments like Colab
nest_asyncio.apply()

# Serve static files from the 'public' directory
app.mount("/static", StaticFiles(directory="public"), name="static")

@app.get("/")
async def serve_index():
    """Serve the frontend index.html."""
    return FileResponse(os.path.join("public", "index.html"))

def get_colab_link(port):
    """Generates the Colab proxy link if running in Google Colab."""
    try:
        from google.colab.output import proxy_port
        return f"https://{proxy_port(port)}"
    except ImportError:
        return None

if __name__ == "__main__":
    PORT = 8000
    COLAB_URL = get_colab_link(PORT)
    
    print("\n" + "="*60)
    print(f"🚀 Server is starting...")
    print(f"🏠 Local Access: http://127.0.0.1:{PORT}")
    
    if COLAB_URL:
        print(f"🌐 Colab Access: {COLAB_URL}")
        print("💡 Click the 'Colab Access' link above to open the application.")
    else:
        print(f"💡 If you are on a local machine, use: http://localhost:{PORT}")
    print("="*60 + "\n")
    
    # In Colab/Notebooks, uvicorn.run works best with nest_asyncio
    uvicorn.run(app, host="0.0.0.0", port=PORT, log_level="info")
