import subprocess

def tail_systemd_logs(service: str, lines: int = 20):
    try:
        print(f"📄 Fetching logs for systemd service: {service}...\n")
        result = subprocess.run(
            ["journalctl", "-u", service, "-n", str(lines), "--no-pager"],
            capture_output=True, text=True
        )

        if result.returncode == 0:
            print(result.stdout)
        else:
            print(f"❌ Failed to fetch logs:\n{result.stderr.strip()}")
    except FileNotFoundError:
        print("❌ journalctl not found. Are you on a systemd-based system?")
    except Exception as e:
        print(f"⚠️  Error: {e}")

def tail_docker_logs(container: str, lines: int = 20):
    try:
        print(f"🐳 Fetching logs for Docker container: {container}...\n")
        result = subprocess.run(
            ["docker", "logs", "--tail", str(lines), container],
            capture_output=True, text=True
        )

        if result.returncode == 0:
            print(result.stdout)
        else:
            print(f"❌ Failed to fetch Docker logs:\n{result.stderr.strip()}")
    except FileNotFoundError:
        print("❌ Docker not found.")
    except Exception as e:
        print(f"⚠️  Error: {e}")

def run(name: str, is_docker: bool = False, lines: int = 20):
    if is_docker:
        tail_docker_logs(name, lines)
    else:
        tail_systemd_logs(name, lines)
