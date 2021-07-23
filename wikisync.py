import os
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
