import platform
import subprocess

def run(host: str):
    system = platform.system()

    if system == "Windows":
        cmd = ["ping", "-n", "4", host]
    else:
        cmd = ["ping", "-c", "4", host]

    try:
        print(f"Pinging {host}...\n")
        output = subprocess.check_output(cmd, stderr=subprocess.STDOUT, text=True)
        print(output)

        # Extract average latency
        if system == "Windows":
            if "Average" in output:
                avg_line = [line for line in output.splitlines() if "Average" in line][0]
                print(f"\n⏱️  {avg_line.strip()}")
        else:
            if "rtt min/avg/max" in output:
                stats_line = [line for line in output.splitlines() if "rtt min/avg/max" in line][0]
                avg = stats_line.split('=')[1].split('/')[1].strip()
                print(f"\n⏱️  Average Latency: {avg} ms")
    except subprocess.CalledProcessError as e:
        print(f"❌ Ping failed: {e.output}")
    except Exception as e:
        print(f"⚠️  Unexpected error: {e}")
