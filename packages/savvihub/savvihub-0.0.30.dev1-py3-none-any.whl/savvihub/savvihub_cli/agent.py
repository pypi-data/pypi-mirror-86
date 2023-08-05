import subprocess
import json
import time

import typer

from savvihub import Context
from savvihub.common.constants import DEBUG

agent_app = typer.Typer()


@agent_app.callback(hidden=True)
def main():
    return


@agent_app.command()
def collect_system_metrics(
    metrics_collector_binary: str = typer.Option("system-metrics-collector", "--collector-binary"),
    prometheus_url: str = typer.Option(..., "--prometheus-url"),
    volumes: str = typer.Option(None, "--volumes"),
    collect_period: int = typer.Option(5, "--collect-period", min=5),
):
    context = Context(experiment_required=True)
    client = context.authorized_client

    while True:
        time.sleep(collect_period)

        args = [
            "-prometheus-url",
            prometheus_url,
            "-experiment",
            context.experiment.slug,
        ]
        if volumes:
            args.extend(['-volumes', volumes])

        p = subprocess.Popen([
            metrics_collector_binary,
            *args,
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = p.communicate()

        if not stdout:
            continue

        metrics = {}
        rows = json.loads(stdout)
        if not rows:
            continue

        for row in rows:
            metrics[row['name']] = [{
                'timestamp': float(row['timestamp']),
                'value': row['value'],
            }]

        if DEBUG:
            print(stderr)

        client.experiment_system_metrics_update(context.experiment.id, metrics)
