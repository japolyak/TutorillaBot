import os
from typing import Optional

from alembic import command as alembic_command
from alembic.config import Config
from alembic.runtime import migration
from alembic.script import ScriptDirectory

from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.schema import CreateSchema
from sqlalchemy_utils import database_exists, create_database

from src.api.src.database.mockdata import insert_mock_data, create_admin
from src.core.config import is_development, connection_string, schema_name
from src.core.logger import log


class DBManager:
    _engine: Optional[Engine]
    _session_factory: Optional[sessionmaker]

    @property
    def session(self) -> Optional[sessionmaker]:
        """Returns a new session instance."""

        if not self._session_factory:
            log.error("Session factory is not initialized.")
            raise RuntimeError("Session factory is not initialized.")

        return self._session_factory()

    def __init__(self):
        self._engine = create_engine(connection_string, echo=is_development)
        self._session_factory = sessionmaker(autocommit=False, autoflush=False, bind=self._engine)

    def initialize_database(self):
        """Initialize the database by creating schema, running migrations, and populating data."""

        if not self._engine:
            log.warning(msg="Engine was not created.")
            return self

        try:
            if database_exists(connection_string):
                schema_created = self._create_schema()
                self._run_migrations()

                if schema_created: return self
            else:
                log.warning(msg="Database does not exist. Creating database...")
                create_database(connection_string)
                log.info(msg="Database created successfully.")

                self._create_schema()
                self._run_migrations()

            create_admin(self._engine, is_development)
            log.info(msg="Admin account created.")

            if is_development:
                insert_mock_data(self._engine)
                log.info(msg="Mock data inserted successfully.")

            return self
        except Exception as e:
            log.error(msg="Error while initializing database.", exc_info=True)
        finally:
            return self

    #region Private methods
    def _create_schema(self) -> bool:
        log.info("already exists.")
        with self._engine.connect() as conn:
            if conn.dialect.has_schema(conn, schema_name):
                log.info(f"Schema '{schema_name}' already exists.")
                return True

            conn.execute(CreateSchema(schema_name))
            conn.commit()
            print("created successfully")
            log.info(f"Schema '{schema_name}' created successfully.")
            return False

    def _is_migration_pending(self, config: Config) -> bool:
        """Checks if there are pending migrations."""
        with self._engine.begin() as conn:
            last_applied_version = migration.MigrationContext.configure(conn).get_current_revision()
            latest_version = ScriptDirectory.from_config(config).get_current_head()

            return last_applied_version != latest_version

    def _run_migrations(self):
        """Applies Alembic migrations if there are any pending."""

        alembic_ini_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        script_location = alembic_ini_path + "/database/migrations"

        alembic_cfg = Config(alembic_ini_path)
        alembic_cfg.set_main_option("script_location", script_location)

        if not self._is_migration_pending(alembic_cfg):
            log.info("No pending migrations.")
            return

        log.info("Applying migrations...")
        alembic_command.upgrade(alembic_cfg, "head")
    #endregion

db_manager = DBManager().initialize_database()
