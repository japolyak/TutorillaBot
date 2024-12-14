import os
import logging
from typing import Optional

from alembic import command as alembic_command
from alembic.config import Config
from alembic.runtime import migration
from alembic.script import ScriptDirectory

from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.schema import CreateSchema
from sqlalchemy_utils import database_exists, create_database

from src.common.config import is_development, connection_string, schema_name
from src.api.src.database.mockdata import insert_mock_data, create_admin


log = logging.getLogger(__name__)


class DBManager:
    __engine: Optional[Engine]
    __session: Optional[sessionmaker]

    @property
    def session(self):
        return self.__session()

    @session.setter
    def session(self, value):
        self.__session = value

    def __init__(self):
        self.__engine = create_engine(connection_string, echo=is_development)
        self.session = sessionmaker(autocommit=False, autoflush=False, bind=self.__engine)

    def initialize_database(self):
        if not self.__engine:
            log.warning(msg="Engine was not created")
            return self

        try:
            if database_exists(connection_string):
                schema_created = self.__create_schema()
                self.__migrate()

                if schema_created: return self
            else:
                log.warning(msg="Database does not exist, attempting to create it.")
                create_database(connection_string)
                log.info(msg="Database successfully created.")

                self.__create_schema()
                self.__migrate()

            create_admin(self.__engine, is_development)
            log.info(msg="Admin successfully created.")

            if is_development:
                insert_mock_data(self.__engine)
                log.info(msg="Mock data inserted.")
            return self
        except Exception as e:
            log.error(msg=f"Error while initializing database: {e}")
            pass

    #region Private methods
    def __create_schema(self) -> bool:
        conn = self.__engine.connect()

        if conn.dialect.has_schema(conn, schema_name): return True

        conn.execute(CreateSchema(schema_name))
        conn.commit()
        log.info(msg="Schema successfully created.")

        return False

    def __is_migration_pending(self, config: Config) -> bool:
        with self.__engine.begin() as conn:
            last_applied_version = migration.MigrationContext.configure(conn).get_current_revision()
            latest_version = ScriptDirectory.from_config(config).get_current_head()

            return last_applied_version != latest_version

    def __migrate(self):
        """Applies alembic migrations."""

        alembic_ini_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        script_location = alembic_ini_path + "/database/migrations"

        alembic_cfg = Config(alembic_ini_path)
        alembic_cfg.set_main_option("script_location", script_location)

        if not self.__is_migration_pending(alembic_cfg):
            return

        alembic_command.upgrade(alembic_cfg, "head")
    #endregion

db_manager = DBManager().initialize_database()
