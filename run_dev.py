#!/usr/bin/env python3
"""
Development startup script for Thai Legal GraphRAG system
"""

import os
import sys
import subprocess
import threading
import time
from pathlib import Path

def run_backend():
    """Run the FastAPI backend"""
    print("🔧 Starting FastAPI backend...")
    try:
        subprocess.run([sys.executable, "main.py"], check=True)
    except KeyboardInterrupt:
        print("\n🛑 Backend stopped")
    except Exception as e:
        print(f"❌ Backend error: {e}")

def run_frontend():
    """Run the React frontend"""
    print("⚛️ Starting React frontend...")
    try:
        subprocess.run(["npm", "run", "dev"], check=True, shell=True)
    except KeyboardInterrupt:
        print("\n🛑 Frontend stopped")
    except Exception as e:
        print(f"❌ Frontend error: {e}")

def check_requirements():
    """Check if all requirements are installed"""
    print("📋 Checking requirements...")
    
    # Check Python packages
    try:
        import fastapi
        import uvicorn
        import sentence_transformers
        import faiss
        import networkx
        print("✅ Python packages OK")
    except ImportError as e:
        print(f"❌ Missing Python package: {e}")
        print("💡 Run: pip install -r requirements.txt")
        return False
    
    # Check Node.js packages
    if not Path("node_modules").exists():
        print("❌ Node.js packages not installed")
        print("💡 Run: npm install")
        return False
    print("✅ Node.js packages OK")
    
    # Check .env file
    if not Path(".env").exists():
        print("❌ .env file not found")
        print("💡 Copy .env.example to .env and configure")
        return False
    print("✅ Environment configuration OK")
    
    return True

def main():
    """Main development startup function"""
    print("🚀 Thai Legal GraphRAG Development Server")
    print("=" * 50)
    
    if not check_requirements():
        print("\n❌ Requirements check failed. Please fix the issues above.")
        return
    
    print("\n🎯 Choose startup mode:")
    print("1. Full stack (Backend + Frontend)")
    print("2. Backend only")
    print("3. Frontend only")
    
    try:
        choice = input("\nEnter choice (1-3): ").strip()
        
        if choice == "1":
            print("\n🚀 Starting full stack...")
            # Start backend in a separate thread
            backend_thread = threading.Thread(target=run_backend, daemon=True)
            backend_thread.start()
            
            # Wait a moment for backend to start
            time.sleep(3)
            
            # Start frontend (this blocks)
            run_frontend()
            
        elif choice == "2":
            print("\n🔧 Starting backend only...")
            run_backend()
            
        elif choice == "3":
            print("\n⚛️ Starting frontend only...")
            run_frontend()
            
        else:
            print("❌ Invalid choice")
            
    except KeyboardInterrupt:
        print("\n\n👋 Development server stopped")

if __name__ == "__main__":
    main()