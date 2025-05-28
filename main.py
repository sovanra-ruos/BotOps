# main.py
import click
from botops.commands import status, ping, restart, log

@click.group()
def cli():
    pass

@cli.command()
def system():
    """Show CPU, RAM, and Disk usage"""
    status.run()

@cli.command()
@click.argument('host')
def pinghost(host):
    """Ping a host"""
    ping.run(host)

@cli.command()
@click.argument('service')
@click.option('--docker', is_flag=True, help="Restart a Docker container instead of systemd service.")
def restart_service(service, docker):
    """Restart a service or Docker container"""
    restart.run(service, is_docker=docker)


@cli.command()
@click.argument('service')
@click.option('--docker', is_flag=True, help="View Docker container logs.")
@click.option('--lines', default=20, help="Number of log lines to show.")
def view_log(service, docker, lines):
    """View logs for a systemd service or Docker container"""
    log.run(service, is_docker=docker, lines=lines)


if __name__ == "__main__":
    cli()
