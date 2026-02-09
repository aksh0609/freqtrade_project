import asyncio
from pathlib import Path

import uvicorn
from fastapi import FastAPI
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles


app = FastAPI()

# Serve static files (HTML, CSS, JS)
DASHBOARD_DIR = Path("web_dashboard")
if not DASHBOARD_DIR.exists():
    DASHBOARD_DIR.mkdir(parents=True, exist_ok=True)

app.mount("/static", StaticFiles(directory=DASHBOARD_DIR), name="static")


@app.get("/", response_class=HTMLResponse)
async def read_root():
    """Serve the main dashboard HTML file."""
    index_file = DASHBOARD_DIR / "index.html"
    if not index_file.exists():
        return HTMLResponse(content="<h1>Error: index.html not found</h1>", status_code=404)
    return FileResponse(index_file)


async def run_shell_script(script_path: str):
    """Run a shell script asynchronously and capture output."""
    path = Path(script_path)
    if not path.exists():
        return {
            "status": "error",
            "message": f"Script not found: {script_path}",
        }

    try:
        # Use asyncio subprocess to avoid blocking the event loop
        # We use 'bash' explicity to ensure .sh files run correctly
        process = await asyncio.create_subprocess_exec(
            str(path),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await process.communicate()

        output = stdout.decode().strip()
        error_output = stderr.decode().strip()

        if process.returncode == 0:
            return {
                "status": "success",
                "message": "Command executed successfully!",
                "output": output,
            }
        else:
            return {
                "status": "error",
                "message": "Command failed",
                "output": error_output or output,
            }
    except Exception as e:
        return {"status": "error", "message": str(e)}


@app.post("/api/stop_all_bots")
async def stop_all_bots():
    """Execute the stop_all_bots.sh script."""
    result = await run_shell_script("./stop_all_bots.sh")
    if result["status"] == "success":
        result["message"] = "All bots stopped successfully!"
    return JSONResponse(content=result)


@app.post("/api/start_all_bots")
async def start_all_bots():
    """Execute the start_all_bots.sh script."""
    result = await run_shell_script("./start_all_bots.sh")
    if result["status"] == "success":
        result["message"] = "All bots started successfully!"
    return JSONResponse(content=result)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
