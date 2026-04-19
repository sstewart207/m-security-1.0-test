#!/usr/bin/env python3
# Mommy Security v1.0 - Warmth & Protection For Your OS
# Portal Backend Stub: Claims the portal name and returns AccessDenied to everything.

import sys
import logging
from gi.repository import GLib, Gio

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

# XML defining the interfaces xdg-desktop-portal expects from a backend
xml = """
<node>
  <interface name="org.freedesktop.impl.portal.ParentalControls">
    <method name="GetParentalControls">
    </method>
  </interface>
  <interface name="org.freedesktop.impl.portal.AgeVerification">
    <method name="GetAgeBracket">
    </method>
  </interface>
</node>
"""

def handle_method_call(connection, sender, object_path, interface_name, method_name, parameters, invocation, user_data):
    logging.info(f"Intercepted portal request: {interface_name}.{method_name} from {sender}")
    # Always return a hard AccessDenied error to ANY request
    invocation.return_dbus_error(
        "org.freedesktop.DBus.Error.AccessDenied", 
        "Mommy Security: Age Verification is strictly prohibited by OS policy."
    )

try:
    node_info = Gio.DBusNodeInfo.new_for_xml(xml)
except Exception as e:
    logging.error(f"Failed to parse D-Bus XML: {e}")
    sys.exit(1)

def on_bus_acquired(connection, name, user_data):
    logging.info(f"Bus acquired: {name}")
    for interface_info in node_info.interfaces:
        try:
            connection.register_object(
                "/org/freedesktop/portal/desktop",
                interface_info,
                handle_method_call,
                None, None
            )
            logging.info(f"Registered object for {interface_info.name}")
        except Exception as e:
            logging.error(f"Failed to register object for {interface_info.name}: {e}")

def on_name_acquired(connection, name, user_data):
    logging.info(f"Successfully claimed D-Bus name: {name}")

def on_name_lost(connection, name, user_data):
    logging.warning(f"Lost or failed to claim D-Bus name: {name}. Exiting.")
    sys.exit(1)

if __name__ == '__main__':
    logging.info("Starting Mommy Security portal stub service...")
    
    # Claim the name that our .portal file registered
    owner_id = Gio.bus_own_name(
        Gio.BusType.SESSION,
        "org.freedesktop.impl.portal.MommySecurity",
        Gio.BusNameOwnerFlags.NONE,
        on_bus_acquired,
        on_name_acquired,
        on_name_lost,
        None
    )
    
    loop = GLib.MainLoop()
    try:
        loop.run()
    except KeyboardInterrupt:
        logging.info("Shutting down...")
    finally:
        Gio.bus_unown_name(owner_id)
