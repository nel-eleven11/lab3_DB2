from connector import Neo4jConnector

class Neo4jFunctions:
    def __init__(self):
        self.connector = Neo4jConnector()

    def create_node(self, label, properties):
        """
        Crea un nodo en Neo4j usando MERGE.
        
        :param label: Nombre del label del nodo.
        :param properties: Diccionario con las propiedades del nodo.
        """
        with self.connector.driver.session() as session:
            properties_str = ", ".join(f"{key}: ${key}" for key in properties)
            query = f"MERGE (n:{label} {{{properties_str}}}) RETURN n"
            session.run(query, **properties)
            print(f"Nodo {label} creado o asegurado con MERGE.")

    def create_relationship(self, label1, properties1, label2, properties2, rel_type, rel_properties=None):
        """
        Crea una relación entre dos nodos en Neo4j usando MERGE.

        :param label1: Label del primer nodo.
        :param properties1: Diccionario con las propiedades del primer nodo.
        :param label2: Label del segundo nodo.
        :param properties2: Diccionario con las propiedades del segundo nodo.
        :param rel_type: Tipo de la relación.
        :param rel_properties: Diccionario con las propiedades de la relación (opcional).
        """
        with self.connector.driver.session() as session:
            prop1_str = ", ".join(f"{k}: ${'a_' + k}" for k in properties1)
            prop2_str = ", ".join(f"{k}: ${'b_' + k}" for k in properties2)
            rel_props_str = ", ".join(f"{k}: ${'r_' + k}" for k in rel_properties) if rel_properties else ""

            query = (
                f"MERGE (a:{label1} {{{prop1_str}}}) "
                f"MERGE (b:{label2} {{{prop2_str}}}) "
                f"MERGE (a)-[r:{rel_type} {{{rel_props_str}}}]->(b) "
                "RETURN a, r, b"
            )

            params = {**{f'a_{k}': v for k, v in properties1.items()},
                      **{f'b_{k}': v for k, v in properties2.items()},
                      **({f'r_{k}': v for k, v in rel_properties.items()} if rel_properties else {})}

            session.run(query, **params)
            print(f"Relación {rel_type} creada o asegurada con MERGE.")

    def find_nodes(self, label, filters=None):
        """
        Busca nodos en Neo4j usando MATCH.

        :param label: Label del nodo a buscar.
        :param filters: Diccionario con filtros opcionales.
        :return: Lista de nodos encontrados.
        """
        with self.connector.driver.session() as session:
            if filters:
                filter_str = " AND ".join(f"n.{k} = ${k}" for k in filters)
                query = f"MATCH (n:{label}) WHERE {filter_str} RETURN n"
                results = session.run(query, **filters)
            else:
                query = f"MATCH (n:{label}) RETURN n"
                results = session.run(query)

            nodes = [record["n"] for record in results]
            return nodes

    def find_nodes_with_relationships(self, label, rel_type=None):
        """
        Busca nodos y sus relaciones en Neo4j usando MATCH.

        :param label: Label del nodo a buscar.
        :param rel_type: Tipo de relación opcional.
        :return: Lista de nodos con relaciones.
        """
        with self.connector.driver.session() as session:
            if rel_type:
                query = f"MATCH (n:{label})-[r:{rel_type}]->(m) RETURN n, r, m"
            else:
                query = f"MATCH (n:{label})-[r]->(m) RETURN n, r, m"

            results = session.run(query)
            data = [{"node": record["n"], "relationship": record["r"], "related_node": record["m"]} for record in results]
            return data


if __name__ == "__main__":
    neo4j_func = Neo4jFunctions()

    # Crear un nodo
    neo4j_func.create_node("Person", {"name": "Juan", "age": 30})

    # Crear una relación
    neo4j_func.create_relationship(
        "Person", {"name": "Juan"},
        "Person", {"name": "Maria"},
        "KNOWS",
        {"since": 2022}
    )

    # Buscar nodos
    nodes = neo4j_func.find_nodes("Person", {"name": "Juan"})
    print("Nodos encontrados:", nodes)

    # Buscar nodos con relaciones
    relationships = neo4j_func.find_nodes_with_relationships("Person")
    print("Nodos con relaciones:", relationships)

    neo4j_func.connector.close()



