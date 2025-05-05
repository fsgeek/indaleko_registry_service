import uvicorn
from registry_service import app

def main():
    """
    Run the FastAPI registry service using Uvicorn.
    """
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
