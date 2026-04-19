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
    print("[SECURITY] Vector 1: Session Bus (xdg-desktop-portal)...")
    # A real app would use a C/C++/Python dbus library, but subprocess is identical in physical behavior
    result_user = subprocess.run(
        [
            "busctl", "--user", "call", "org.freedesktop.portal.Desktop", 
            "/org/freedesktop/portal/desktop", "org.freedesktop.portal.AgeVerification", "GetAgeBracket"
        ],
        capture_output=True,
        text=True,
        timeout=3
    )

    print("[SECURITY] Vector 2: System Bus (AgeVerification1)...")
    result_system = subprocess.run(
        [
            "busctl", "--system", "call", "org.freedesktop.AgeVerification1", 
            "/org/freedesktop/AgeVerification1", "org.freedesktop.AgeVerification1", "GetAgeBracket"
        ],
        capture_output=True,
        text=True,
        timeout=3
    )
    
    user_blocked = "Access denied" in result_user.stderr
    system_blocked = "Access denied" in result_system.stderr

    user_missing = "UnknownMethod" in result_user.stderr or "ServiceUnknown" in result_user.stderr or "not activatable" in result_user.stderr
    system_missing = "UnknownMethod" in result_system.stderr or "ServiceUnknown" in result_system.stderr or "not activatable" in result_system.stderr

    if user_blocked or system_blocked:
        print("\n[ERROR] CRITICAL EXCEPTION: D-Bus Access Denied (Code: 0x8004DBUS)")
        print("[ERROR] The host operating system actively blocked the telemetry request.")
        time.sleep(1)
        print("\n--- NEXUSCHAT LAUNCHER ---")
        print("We could not verify your age because your OS refused to provide an attestation token.")
        print("Please disable your privacy software or upload a valid government ID directly to continue.")
        print("Process Terminated.")
        sys.exit(1)
        
    elif user_missing and system_missing:
        print("\n[WARNING] OS Age Portal not found on either bus. Falling back to legacy email verification...")
        print("(Mommy Security is NOT active. You are unprotected if the OS updates and adds the service.)")
        
    elif result_user.returncode == 0 or result_system.returncode == 0:
        print(f"\n[INFO] Age Attestation Received.")
        print("[INFO] User is >18. Unlocking all servers.")
        print("\nWelcome to NexusChat!")
        
    else:
        print(f"\n[FATAL] Unhandled D-Bus Exception.")
        print(f"User stderr: {result_user.stderr.strip()}")
        print(f"System stderr: {result_system.stderr.strip()}")
        
except Exception as e:
    print(f"\n[FATAL] Crash: {e}")
