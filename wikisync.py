import os
import argparse
import igem_wikisync as wikisync
from dotenv import load_dotenv
    

def sync(src_dir, temp_build_dir, team):
    """
    Syncs a source directory with the a team's iGEM Wiki on the iGEM MediaWiki server.
    
    Note: The environmental parameters IGEM_USERNAME and IGEM_PASSWORD must be supplied.

    Args:
        src_dir (str): The directory that is being synced with the wiki.
        temp_build_dir (str): A temporary directory where the src_directory will be rebuilt.
        team (str): The iGEM team for the wiki.
    """

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


if __name__ == '__main__':
    """
    If run as a main file (i.e., `python ./wikisync.py`), syncs a build directory
    to the iGEM team wiki.

    positional arguments:
        build-directory  The path to the directory that is being synced to the wiki.
        temp-directory   The path to a temporary directory. Used to sync the wiki.
        team-name        The iGEM team name.

    """

    parser = argparse.ArgumentParser(description='Syncs a local wiki to the iGEM server.')

    parser.add_argument('Build',
                        metavar='build-directory',
                        type=str,
                        help='The path to the directory that is being synced to the wiki.')

    parser.add_argument('Temp',
                        metavar='temp-directory',
                        type=str,
                        help='The path to a temporary directory. Used to sync the wiki.')

    parser.add_argument('Team',
                        metavar='team-name',
                        type=str,
                        help='The iGEM team name.')

    args = parser.parse_args()

    build_path = args.Build
    temp_sync_path = args.Temp
    team_name = args.Team

    sync(build_path, temp_sync_path, team_name)