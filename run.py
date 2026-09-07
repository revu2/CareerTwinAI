import uvicorn
import os
import sys

def main():
    print("=" * 60)
    print("   CareerTwin AI - Multi-Agent Career Digital Twin")
    print("   Starting Local Server at http://127.0.0.1:8000")
    print("=" * 60)
    uvicorn.run(
        "backend.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )

if __name__ == "__main__":
    main()
