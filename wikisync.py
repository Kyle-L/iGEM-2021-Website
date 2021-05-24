import os
import igem_wikisync as wikisync
from dotenv import load_dotenv

def sync():
    dirname = os.path.dirname(__file__)

    # Loads environment variables.
    load_dotenv(os.path.join(dirname, '.env'))

    # Sets the src and build directories.
    src_dir = os.path.join(dirname, 'temp/build')
    build_dir = os.path.join(dirname, 'temp/sync')

    # Start syncing the team wiki with the site directory.
    # Note, temp is used as temporary build location for the site.
    wikisync.run(
        team='MiamiU_OH',
        src_dir=src_dir,      
        build_dir=build_dir     
    )

if __name__ == '__main__':
    answer = input("Are you sure you want to sync the wiki (Y/N): ").lower() 
    if answer == "yes" or answer == "y": 
        sync()