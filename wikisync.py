import os
import igem_wikisync as sync
from dotenv import load_dotenv

dirname = os.path.dirname(__file__)

# Loads environment variables.
load_dotenv(os.path.join(dirname, '.env'))

# Sets the src and build directories.
src_dir = os.path.join(dirname, 'site')
build_dir = os.path.join(dirname, 'temp')

# Start syncing the team wiki with the site directory.
# Note, temp is used as temporary build location for the site.
sync.run(
    team='MiamiU_OH',
    src_dir=src_dir,      
    build_dir=build_dir     
)