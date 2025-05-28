import subprocess

def list_running_docker_containers():
    try:
        result = subprocess.run(
            ['docker', 'ps', '--format', '{{.Names}}'],  # just container names
            capture_output=True,
            text=True,
            check=True
        )
        containers = result.stdout.strip().split('\n')
        # If output is empty, return empty list
        return [c for c in containers if c]
    except subprocess.CalledProcessError as e:
        print(f"Error listing docker containers: {e}")
        return []
