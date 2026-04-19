# Mommy Security v1.0 🐾🖤💖
![Vera, Mommy Security](vera.png)
**Warmth & Protection For Your OS**

---

### 🛡️ What is this?
**Mommy Security** is a native, kernel-level D-Bus blockade designed to protect your privacy against invasive age-verification infrastructure creeping into Linux distributions.

Due to legislation like California AB-1043 and Colorado SB26-051 (effective 2027), OS providers are being pressured to act as age verification gatekeepers. This has led to the implementation of "Parental Control" and "Age Verification" APIs at the core of the Linux desktop stack—specifically:
1. **`systemd` PR #40954** (which quietly added a `birthDate` field to system JSON user records).
2. **`xdg-desktop-portal` PR #1922** (which created a D-Bus API for sandboxed apps to query your age bracket).

**Mommy Security offers zero cooperation.** It is not a spoofing tool that feeds fake "18+" data to apps. It is a pure, uncompromising hard-block that instantly intercepts and destroys any attempt by an application to ask for your age.

---

### ⚙️ How does it work?
Unlike protest projects (like Ageless Linux) that alter your core OS identity or overwrite `/etc/os-release`, Mommy Security acts as a sleek, native security shield. It drops cleanly into any modern Linux OS (like Fedora) without breaking your setup.

It deploys a three-layer defense:
1. **The Portal Trap:** It aggressively claims the `AgeVerification` portal backend across *all* major desktop environments (GNOME, KDE, Cinnamon, Hyprland, sway, etc.). Any app asking the portal for your age is routed directly to us.
2. **The D-Bus Shield:** Using raw XML D-Bus policies (`/etc/dbus-1/session.d/`), Mommy Security instructs the Linux message bus itself to immediately reject age queries. The app gets a hard `org.freedesktop.DBus.Error.AccessDenied` before the message even leaves the sandbox. 
3. **The Scrubber (Nullifier):** A silent background systemd service wakes up daily to scrub any physical `birthDate` fields in `/var/lib/systemd/userdb/` back to the Unix Epoch (`1970-01-01`) and hard-masks the `systemd-userdbd` and `systemd-homed` enforcement sockets.

---

### 🚀 How do I use it?

**1. Install the Shield**
Clone this repository and run the installer as root. It is fully idempotent and safe to run multiple times.
```bash
sudo ./install.sh
```

**2. Manage with `mommyctl`**
Mommy Security comes with a friendly command-line tool to manage your protection.
* `mommyctl status` — Checks if the D-Bus policies are installed, sockets are masked, and timers are active.
* `mommyctl test` — Simulates a rogue application trying to ask for your age over D-Bus to prove the shield is working.
* `sudo mommyctl scrub` — Manually triggers the data scrubber to wipe birth dates.

**3. Uninstall**
If you ever want to remove the shield entirely:
```bash
sudo ./install.sh --uninstall
```

---

### 🛑 What happens when it's active?
It runs entirely silently. There are no pop-ups, no fake prompts, and no logging unless a physical file is scrubbed. 

When a sandboxed app (like a Flatpak browser or game) attempts to query your age:
1. The app asks `xdg-desktop-portal` for your age bracket.
2. The D-Bus daemon intercepts the request because of Mommy Security's policy.
3. The D-Bus daemon instantly throws `Access denied`.
4. **The app receives nothing.** It is forced to either degrade gracefully or block you using its own internal logic—but it gets zero cooperation from your operating system. Your privacy remains intact.
