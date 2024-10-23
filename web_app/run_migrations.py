import os
import sys

# Adjust the path to include the project root
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, PROJECT_ROOT)

from alembic import command
from alembic.config import Config

# Import DATABASE_URL to ensure environment variables are loaded
from shared.utils import DATABASE_URL

def run_migrations():
    # Path to your alembic.ini file in the migrations directory
    alembic_cfg = Config(os.path.join(PROJECT_ROOT, 'database', 'alembic.ini'))
    command.upgrade(alembic_cfg, "head")

if __name__ == "__main__":
    run_migrations()