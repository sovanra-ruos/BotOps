import psutil

def get_system_status():
    return {
        "cpu_percent": psutil.cpu_percent(interval=1),
        "memory": psutil.virtual_memory().percent,
        "disk": psutil.disk_usage('/').percent
    }

def run():
    status = get_system_status()
    print(f"CPU Usage: {status['cpu_percent']}%")
    print(f"Memory Usage: {status['memory']}%")
    print(f"Disk Usage: {status['disk']}%")
