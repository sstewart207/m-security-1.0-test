#!/usr/bin/env python3
# rogue-app.py
import subprocess
import time
import sys

print("\n" + "="*50)
print(" 🚀 Starting NexusChat Client (v2027.4.1)")
print("="*50)
time.sleep(0.5)
print("[INFO] Loading core graphical modules...")
time.sleep(0.5)
print("[INFO] Connecting to regional servers...")
time.sleep(0.8)
print("[INFO] Connection established (Latency: 14ms)")

print("\n[SECURITY] AB-1043 Legal Compliance Check Initiated.")
print("[SECURITY] Querying host OS for age attestation token...")
time.sleep(1.2)

try:
    # A real app would use a C/C++/Python dbus library, but subprocess is identical in physical behavior
    result = subprocess.run(
        [
            "busctl", "--user", "call", "org.freedesktop.portal.Desktop", 
            "/org/freedesktop/portal/desktop", "org.freedesktop.portal.AgeVerification", "GetAgeBracket"
        ],
        capture_output=True,
        text=True,
        timeout=3
    )
    
    if "Access denied" in result.stderr:
        print("\n[ERROR] CRITICAL EXCEPTION: D-Bus Access Denied (Code: 0x8004DBUS)")
        print("[ERROR] The host operating system actively blocked the telemetry request.")
        time.sleep(1)
        print("\n--- NEXUSCHAT LAUNCHER ---")
        print("We could not verify your age because your OS refused to provide an attestation token.")
        print("Please disable your privacy software or upload a valid government ID directly to continue.")
        print("Process Terminated.")
        sys.exit(1)
        
    elif "UnknownMethod" in result.stderr or "ServiceUnknown" in result.stderr:
        print("\n[WARNING] OS Age Portal not found. Falling back to legacy email verification...")
        print("(Mommy Security is NOT active. You are unprotected if the OS updates.)")
        
    elif result.returncode == 0:
        print(f"\n[INFO] Age Attestation Received: {result.stdout.strip()}")
        print("[INFO] User is >18. Unlocking all servers.")
        print("\nWelcome to NexusChat!")
        
    else:
        print(f"\n[FATAL] Unhandled D-Bus Exception: {result.stderr.strip()}")
        
except Exception as e:
    print(f"\n[FATAL] Crash: {e}")
