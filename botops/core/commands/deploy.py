import subprocess

def deploy_container(image_name: str, container_name: str, ports: str = "80:80") -> str:
    try:
        # Pull the latest image
        subprocess.run(["docker", "pull", image_name], check=True)

        # Stop and remove existing container if exists
        subprocess.run(["docker", "rm", "-f", container_name], check=False)

        # Run new container
        subprocess.run([
            "docker", "run", "-d",
            "--name", container_name,
            "-p", ports,
            image_name
        ], check=True)

        return f"✅ Deployed `{container_name}` from `{image_name}` on ports `{ports}`"
    except subprocess.CalledProcessError as e:
        return f"❌ Deployment failed: {e}"
