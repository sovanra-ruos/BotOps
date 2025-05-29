import subprocess

def allow_port(port: str) -> str:
    try:
        result = subprocess.run(
            ["sudo", "ufw", "allow", port],
            check=True,
            capture_output=True,
            text=True
        )
        return f"✅ Port `{port}` allowed:\n```\n{result.stdout.strip()}\n```"
    except subprocess.CalledProcessError as e:
        return f"❌ Failed to allow port `{port}`:\n```\n{e.stderr.strip()}\n```"
