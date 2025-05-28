import psutil
import subprocess

# Modify this to point to your container or service name
SERVICE_NAME = "nginx"
CONTAINER_NAME = "botops_container"

def check_system_health():
    cpu = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory().percent
    disk = psutil.disk_usage("/").percent
    return {"cpu": cpu, "memory": memory, "disk": disk}

def auto_remediate(health: dict):
    actions = []

    if health["cpu"] > 90:
        try:
            subprocess.run(["systemctl", "restart", SERVICE_NAME], check=True)
            actions.append(f"🔁 Restarted service: `{SERVICE_NAME}` due to high CPU ({health['cpu']}%)")
        except Exception as e:
            actions.append(f"⚠️ Failed to restart `{SERVICE_NAME}`: {str(e)}")

    if health["memory"] > 90:
        try:
            subprocess.run(["docker", "restart", CONTAINER_NAME], check=True)
            actions.append(f"🔁 Restarted container: `{CONTAINER_NAME}` due to high memory ({health['memory']}%)")
        except Exception as e:
            actions.append(f"⚠️ Failed to restart `{CONTAINER_NAME}`: {str(e)}")

    return actions
