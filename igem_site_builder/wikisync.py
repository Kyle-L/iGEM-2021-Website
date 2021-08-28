import os
import argparse
import igem_wikisync as wikisync
from dotenv import load_dotenv


class console_colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def sync(src_dir, temp_build_dir, team):
    """
    Syncs a source directory with the a team's iGEM Wiki on the iGEM MediaWiki server.

    Note: The environmental parameters IGEM_USERNAME and IGEM_PASSWORD must be supplied.

    Args:
        src_dir (str): The directory that is being synced with the wiki.
        temp_build_dir (str): A temporary directory where the src_directory will be rebuilt.
        team (str): The iGEM team for the wiki.
    """
    print(console_colors.HEADER +
          f'Syncing the site with the iGEM wiki!' + console_colors.OKBLUE)

    try:
        dirname = os.path.dirname(__file__)

        # Loads environment variables.
        load_dotenv(os.path.join(dirname, '.env'))

        # Start syncing the team wiki with the site directory.
        # Note, temp is used as temporary build location for the site.
        wikisync.run(
            team=team,
            src_dir=src_dir,
            build_dir=temp_build_dir
        )
    except:
        print(console_colors.WARNING +
              f'Something went wrong templating the site!!!' + console_colors.ENDC)

    print(console_colors.OKGREEN + f'Templating done!' + console_colors.ENDC)
