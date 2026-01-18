#!/usr/bin/env python3
"""Build script to create standalone executable for Auction TUI.

Works on Windows, macOS, and Linux.
Just run: python build_executable.py
"""

import subprocess
import sys
import os
import platform

def main():
    # Ensure we're in the right directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)

    system = platform.system()
    print(f"Building for: {system} ({platform.machine()})")
    print("=" * 60)

    # Install PyInstaller if not present
    print("\nChecking for PyInstaller...")
    try:
        import PyInstaller
        print("PyInstaller found.")
    except ImportError:
        print("Installing PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])

    # Also ensure dependencies are installed
    print("\nChecking dependencies...")
    dependencies = ["textual", "openpyxl"]
    for dep in dependencies:
        try:
            __import__(dep)
            print(f"  {dep}: OK")
        except ImportError:
            print(f"  {dep}: Installing...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", dep])

    # Determine executable name based on platform
    if system == "Windows":
        exe_name = "AstaFantaciclismo.exe"
    else:
        exe_name = "AstaFantaciclismo"

    # Build the executable
    print("\nBuilding executable...")

    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",                    # Single executable file
        "--name", "AstaFantaciclismo",  # Name of the executable
        "--clean",                      # Clean cache before building
        "--noconfirm",                  # Don't ask for confirmation
        "--console",                    # Console app (needed for TUI)
        "auction_tui.py"
    ]

    subprocess.check_call(cmd)

    # Full path to executable
    exe_path = os.path.join(script_dir, "dist", exe_name)

    print("\n" + "=" * 60)
    print("BUILD COMPLETE!")
    print("=" * 60)
    print(f"\nExecutable: {exe_path}")
    print(f"Size: {os.path.getsize(exe_path) / (1024*1024):.1f} MB")

    print("\n" + "-" * 60)
    print("USAGE:")
    print("-" * 60)
    if system == "Windows":
        print(f'  dist\\AstaFantaciclismo.exe "Lista-UWT-2026.xlsx"')
        print("\nOr double-click the .exe and drag your Excel file onto it.")
    else:
        print(f'  ./dist/AstaFantaciclismo "Lista-UWT-2026.xlsx"')

    print("\n" + "-" * 60)
    print("TO DISTRIBUTE:")
    print("-" * 60)
    print(f"Just copy '{exe_name}' from the 'dist' folder.")
    print("No Python installation needed on the target computer!")


if __name__ == "__main__":
    main()
