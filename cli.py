import requests
import click
import sys

from local_exceptions import IncorrectParametersException
import writers
from platformids import platforms

BASE_URL = "http://challengehuntapp.appspot.com/"
PLATFORM_IDS = platforms

def get_contests_data():
  req = requests.get(BASE_URL)

  if req.status_code == requests.codes.ok:
    return req.json()
  else:
    click.secho("Couldn't get the data", fg="red", bold=True)
    click.secho("Exiting...", fg="red", bold=True)
    sys.exit()


def active_contests(platform):
  contests_data = get_contests_data()
  writers.write_active_contests(contests_data["active"])
  

def upcoming_contests(platform):
  contests_data = get_contests_data()
  writers.write_upcoming_contests(contests_data["pending"])


def get_all_contests():
  contests_data = get_contests_data()
  # writers.all_contests(contests_data)


@click.command()
@click.option('--active', is_flag=True, help="Shows all the active contests")
@click.option('--upcoming', is_flag=True, help="Shows all the upcoming contests")
@click.option('--platform', '-p', type=click.Choice(PLATFORM_IDS.keys()),
              help=("Choose the platform whose fixtures you want to see. "
                "See platform codes for more info"))
@click.option('--time', default=6,
              help="The number of days in the past for which you want to see the contests")
def main(active, upcoming, platform):
  """A CLI for actve and upcoming programming challenges from various platforms"""
  try:
    if active:
    	  active_contests(platform)

    if upcoming:
      upcoming_contests(platform)
      return

    get_all_contests()
  except IncorrectParametersException as e:
    click.secho(e.message, fg="red", bold=True)

if __name__ == '__main__':
  main()
