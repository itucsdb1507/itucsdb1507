import psycopg2 as dbapi2

class StatisticT:
    def __init__(self, statistic_id, season, teamName, touchdowns, rushingYards):
        self.statistic_id = statistic_id
        self.season = season
        self.teamName = teamName
        self.touchdowns = touchdowns
        self.rushingYards = rushingYards

class StatisticsT:
    def __init__(self, app):
        self.app = app

    def initialize_tables(self):
        with dbapi2.connect(self.app.config['dsn']) as connection:
                cursor = connection.cursor()
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS STATISTICST
                    (
                    STATISTIC_ID SERIAL NOT NULL PRIMARY KEY,
                    SEASON_ID INTEGER NOT NULL REFERENCES SEASONS(SEASON_ID),
                    TEAM_ID INTEGER NOT NULL REFERENCES TEAMS(TEAM_ID),
                    touchdowns INTEGER NOT NULL,
                    rushingYards INTEGER NOT NULL
                    )
                    """)
                connection.commit()

    def get_statistics_team(self):
        with dbapi2.connect(self.app.config['dsn']) as connection:
            cursor = connection.cursor()
            query="""SELECT S.STATISTIC_ID, SS.YEAR, T.NAME, S.TOUCHDOWNS, S.RUSHINGYARDS
                        FROM STATISTICST S
                        LEFT JOIN SEASONS SS ON (S.SEASON_ID = SS.SEASON_ID)
                        LEFT JOIN TEAMS T ON (S.TEAM_ID = T.TEAM_ID)
                        ORDER BY SS.YEAR ASC"""
            cursor.execute(query)
            connection.commit()

            statisticst = [(key, season, team, touchdowns, rushingYards)
                        for key, season, team, touchdowns, rushingYards in cursor]
            return statisticst

    def add_statistic_team(self, season_id, team_id, touchdowns, rushingYards):
        with dbapi2.connect(self.app.config['dsn']) as connection:
                cursor = connection.cursor()
                query = """ INSERT INTO STATISTICST (SEASON_ID, TEAM_ID, touchdowns, rushingYards) VALUES (%s, %s, %s, %s) """
                cursor.execute(query, (season_id, team_id, touchdowns, rushingYards))
                connection.commit()

    def delete_statistic_team(self, id):
        with dbapi2.connect(self.app.config['dsn']) as connection:
                cursor = connection.cursor()
                cursor.execute("""
                    DELETE FROM STATISTICST
                    WHERE STATISTIC_ID = %s""",
                    id)
                connection.commit()

    def update_statistic_team(self, statistic_id, season_id, team_id, touchdowns, rushingYards):
        with dbapi2.connect(self.app.config['dsn']) as connection:
                cursor = connection.cursor()
                query = """ UPDATE STATISTICST
                        SET SEASON_ID = %s,
                        TEAM_ID = %s,
                        TOUCHDOWNS = %s,
                        RUSHINGYARDS = %s
                        WHERE STATISTIC_ID = %s"""
                cursor.execute(query, (season_id, team_id, touchdowns, rushingYards, statistic_id))
                connection.commit()

    def search_statistic_team(self, id):
        with dbapi2.connect(self.app.config['dsn']) as connection:
            cursor = connection.cursor()
            query="""SELECT STATISTIC_ID, SEASONS.YEAR, TEAMS.NAME, TOUCHDOWNS, RUSHINGYARDS
                    FROM STATISTICST
                    INNER JOIN SEASONS ON SEASONS.SEASON_ID=STATISTICST.SEASON_ID
                    INNER JOIN TEAMS ON TEAMS.TEAM_ID=STATISTICST.TEAM_ID
                    WHERE TEAMS.NAME LIKE '%s'""" % ('%'+id+'%')
            cursor.execute(query)
            connection.commit()

            result = cursor.fetchall()
            return result