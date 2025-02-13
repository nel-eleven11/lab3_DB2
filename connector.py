from neo4j import GraphDatabase
import dotenv
import os

# id: cb9c1ece contraseña nelson: 5NKfsIo-v1iEjtiZS4BV8FN0bk09IgEaQ4Cs4FlxQGM
# id: 0923c3a8 contraseña joaquín: J-c7J6DCItie9-v8r_PsH3ULukxFb2Dq6I4TE_fj_qk

class Neo4jConnector:
    def __init__(self, env_file="creds.txt"):
        if not dotenv.load_dotenv(env_file):
            raise RuntimeError("Environment variables not loaded.")
        
        self.uri = os.getenv("NEO4J_URI")
        self.auth = (os.getenv("NEO4J_USER"), os.getenv("NEO4J_PASSWORD"))

        if not all(self.auth) or not self.uri:
            raise ValueError("Neo4j credentials are not set correctly in the environment.")

        self.driver = GraphDatabase.driver(self.uri, auth=self.auth)

    def test_connection(self):
        try:
            with self.driver.session() as session:
                session.run("RETURN 1") 
            print("Neo4j Connection established.")
        except Exception as e:
            raise RuntimeError(f"Connection failed: {e}")

    def close(self):
        if self.driver:
            self.driver.close()

if __name__ == "__main__":
    connector = Neo4jConnector()
    connector.test_connection()
    connector.close()

