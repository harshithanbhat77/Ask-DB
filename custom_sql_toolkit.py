from langchain_community.utilities import SQLDatabase
from langchain_community.tools.sql_database.tool import (
    QuerySQLDatabaseTool,
    InfoSQLDatabaseTool,
    ListSQLDatabaseTool,
)
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit


class CustomSQLToolkit(SQLDatabaseToolkit):
    """Custom SQL toolkit compatible with LangChain 0.4.x, optimized for performance."""

    def __init__(self, db: SQLDatabase, llm):
       
        super().__init__(db=db, llm=llm)

        object.__setattr__(self, "db", db)
        object.__setattr__(self, "llm", llm)

        if not hasattr(db, "table_info"):
            db.table_info = lambda: db.get_table_info(db.get_usable_table_names())

        tools = self._create_optimized_tools()
        object.__setattr__(self, "_optimized_tools", tools)

        object.__setattr__(self, "_dialect", db.dialect)

    @property
    def dialect(self):
        """Expose SQL dialect for agent creation."""
        return self._dialect

    @property
    def tools(self):
        """Expose custom optimized tools."""
        return self._optimized_tools

    def _create_optimized_tools(self):
        """Define optimized tools for complex queries."""
        return [
            QuerySQLDatabaseTool(
                db=self.db,
                name="optimized_query_sql_db",
                description="Run optimized SQL queries using joins, filters, and aggregations.",
            ),
            InfoSQLDatabaseTool(db=self.db),
            ListSQLDatabaseTool(db=self.db),
        ]
