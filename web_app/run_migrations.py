import os
import sys
import logging
import traceback

# Set up basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Adjust the path to include the project root
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, PROJECT_ROOT)

def run_migrations():
    logger.info("Starting migrations...")

    # Path to alembic.ini
    alembic_cfg_path = os.path.join(PROJECT_ROOT, 'database', 'alembic.ini')
    logger.info(f"Alembic config path: {alembic_cfg_path}")
    from alembic.config import Config
    alembic_cfg = Config(alembic_cfg_path)

    # Set script_location explicitly
    alembic_cfg.set_main_option('script_location', os.path.join(PROJECT_ROOT, 'database', 'migrations'))
    logger.info(f"Script location set to: {alembic_cfg.get_main_option('script_location')}")

    # Load environment variables if necessary
    from dotenv import load_dotenv
    load_dotenv(os.path.join(PROJECT_ROOT, '.env'))

    # Log the database URL
    database_url = os.environ.get("DATABASE_URL")
    if database_url:
        logger.info(f"DATABASE_URL is set to: {database_url}")
    else:
        logger.error("DATABASE_URL is not set.")
        sys.exit(1)

    try:
        # Remove the stamp command
        # Only run the upgrade command
        from alembic import command

        # Run migrations
        logger.info("Running alembic upgrade head")
        command.upgrade(alembic_cfg, "head")
        logger.info("Migrations completed successfully.")

    except Exception as e:
        logger.exception("Error during migrations:")
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    run_migrations()