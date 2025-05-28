import subprocess

def restart_systemd(service: str):
    try:
        print(f"🔄 Restarting systemd service: {service}...")
        result = subprocess.run(["sudo", "systemctl", "restart", service],
                                capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Successfully restarted systemd service '{service}'.")
        else:
            print(f"❌ Failed to restart '{service}'.\n{result.stderr.strip()}")
    except Exception as e:
        print(f"⚠️  Error: {e}")

def restart_docker(container: str):
    try:
        print(f"🐳 Restarting Docker container: {container}...")
        result = subprocess.run(["docker", "restart", container],
                                capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Successfully restarted Docker container '{container}'.")
        else:
            print(f"❌ Failed to restart container '{container}'.\n{result.stderr.strip()}")
    except FileNotFoundError:
        print("❌ Docker not installed or not in PATH.")
    except Exception as e:
        print(f"⚠️  Error: {e}")

def run(name: str, is_docker: bool = False):
    if is_docker:
        restart_docker(name)
    else:
        restart_systemd(name)
