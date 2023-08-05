import sys
import time

import requests
import typer

from savvihub.api.savvihub import SavviHubClient
from savvihub.common.constants import API_HOST, WEB_HOST, DEBUG
from savvihub.common.config_loader import GlobalConfigLoader
from savvihub.savvihub_cli.agent import agent_app
from savvihub.savvihub_cli.dataset import dataset_app
from savvihub.savvihub_cli.experiment import experiment_app
from savvihub.savvihub_cli.volume import volume_app
from savvihub.savvihub_cli.project import project_app

app = typer.Typer()
app.add_typer(agent_app, name="agent")
app.add_typer(project_app, name="project")
app.add_typer(experiment_app, name="experiment")
app.add_typer(dataset_app, name="dataset")
app.add_typer(volume_app, name="volume")
__version__ = '0.0.30-dev2'


def version_callback(value: bool):
    if value:
        typer.echo(f"Savvihub CLI Version: {__version__}")
        raise typer.Exit()


@app.callback()
def main(
    version: bool = typer.Option(None, "--version", callback=version_callback, is_eager=True,
                                 help="Print the current SavviHub CLI version."),
):
    """
    SavviHub Command Line Interface (CLI)
    """
    if DEBUG:
        typer.echo(f"Savvihub CLI Version: {__version__}")

    return


@app.command()
def ping():
    """
    Ping to the SavviHub server
    """
    res = requests.get(API_HOST + '/v1/api/ping/')
    typer.echo(f"Response code: {res.status_code}, Response text: {res.text}")


@app.command()
def init(
    token: str = typer.Option(None, "-t", "--token")
):
    """
    Initialize SavviHub Command Line Interface (CLI)
    """

    def update_token():
        client = SavviHubClient()
        cli_token = client.check_signin_token()
        typer.echo(f'Please continue in below URL.\n{WEB_HOST}/cli/access-token-invocation?cli-token={cli_token}')

        start_time = time.time()
        while True:
            if time.time() - start_time >= 160:
                typer.echo('Login time limit exceeded. Please try again.')
                sys.exit(1)

            signin_success, access_token = client.check_signin(cli_token)
            if not signin_success:
                time.sleep(3)
                continue

            return access_token

    if token is None:
        typer.echo('To continue, you must log in.')
        token = update_token()

    client = SavviHubClient(token=token)
    me = client.get_my_info()
    if me:
        typer.echo(f'Hello {me.username}!')
    else:
        typer.echo('Token expired or invalid token.')
        token = update_token()

    config = GlobalConfigLoader()
    config.set_user(token=token)

    typer.echo(f"Token successfully saved in {config.filename}")
