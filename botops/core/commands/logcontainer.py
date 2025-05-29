import subprocess

def get_container_logs(container_name: str, tail: int = 50) -> str:
    try:
        result = subprocess.run(
            ["docker", "logs", f"--tail={tail}", container_name],
            check=True,
            capture_output=True,
            text=True
        )
        logs = result.stdout.strip()
        if not logs:
            return f"ℹ️ No logs found for `{container_name}`."
        return f"📄 Logs for `{container_name}` (last {tail} lines):\n```\n{logs[-3800:]}\n```"
    except subprocess.CalledProcessError as e:
        return f"❌ Failed to get logs for `{container_name}`:\n```\n{e.stderr.strip()}\n```"
