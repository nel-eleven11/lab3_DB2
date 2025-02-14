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

    def find_nodes_with_relationships(self, label1, filters1=None, label2=None, filters2=None, rel_type=None, rel_filters=None):
        """
        Busca nodos con relaciones en Neo4j usando MATCH.
        
        :param label1: Label del primer nodo.
        :param filters1: Diccionario con filtros para el primer nodo (opcional).
        :param label2: Label del segundo nodo (opcional).
        :param filters2: Diccionario con filtros para el segundo nodo (opcional).
        :param rel_type: Tipo de relación (opcional).
        :param rel_filters: Diccionario con filtros para la relación (opcional).
        :return: Lista de resultados con nodos y relaciones.
        """
        with self.connector.driver.session() as session:
            where_clauses = []
            params = {}

            # Construcción del primer nodo
            node1_filter_str = ", ".join(f"{k}: ${'a_' + k}" for k in filters1) if filters1 else ""
            node1_match = f"(a:{label1} {{{node1_filter_str}}})" if node1_filter_str else f"(a:{label1})"

            # Construcción del segundo nodo
            node2_match = ""
            if label2:
                node2_filter_str = ", ".join(f"{k}: ${'b_' + k}" for k in filters2) if filters2 else ""
                node2_match = f"(b:{label2} {{{node2_filter_str}}})" if node2_filter_str else f"(b:{label2})"

            # Construcción de la relación
            rel_match = ""
            if rel_type:
                rel_filter_str = ", ".join(f"{k}: ${'r_' + k}" for k in rel_filters) if rel_filters else ""
                rel_match = f"-[r:{rel_type} {{{rel_filter_str}}}]->" if rel_filter_str else f"-[r:{rel_type}]->"

            # Construcción de WHERE
            if filters1:
                where_clauses += [f"a.{k} = $a_{k}" for k in filters1]
                params.update({f'a_{k}': v for k, v in filters1.items()})
            if filters2:
                where_clauses += [f"b.{k} = $b_{k}" for k in filters2]
                params.update({f'b_{k}': v for k, v in filters2.items()})
            if rel_filters:
                where_clauses += [f"r.{k} = $r_{k}" for k in rel_filters]
                params.update({f'r_{k}': v for k, v in rel_filters.items()})

            where_clause = f" WHERE {' AND '.join(where_clauses)}" if where_clauses else ""

            # Construcción final de la consulta
            query = f"MATCH {node1_match}{rel_match}{node2_match} {where_clause} RETURN a, r, b"

            results = session.run(query, **params)
            data = [{"node1": record["a"], "relationship": record["r"], "node2": record["b"]} for record in results]
            return data



if __name__ == "__main__":
    neo4j_func = Neo4jFunctions()

    #hacer menu de incisos

    opcion = 0

    while opcion != 5:
        print("1. Crear nodos")
        print("2. Crear relaciones")
        print("3. Buscar")
        print("4. Crear grafor de usuarios y películas")
        print("5. Salir")

        opcion = int(input("Opción: "))

        if opcion == 1:
            print("Creando nodos...")
            neo4j_func.create_node("User", {"name": "Juan", "userId": 1})
            neo4j_func.create_node("User", {"name": "Maria", "userId": 2})
            neo4j_func.create_node("User", {"name": "Pedro", "userId": 3})
            neo4j_func.create_node("User", {"name": "Jose", "userId": 4})
            neo4j_func.create_node("User", {"name": "Carlos", "userId": 5})
            neo4j_func.create_node("Movie", {"title": "Matrix", "movieId": 1, "year": 1999, "plot": "A computer hacker learns from mysterious rebels about the true nature of his reality."})
            neo4j_func.create_node("Movie", {"title": "Star Wars", "movieId": 2, "year": 1977, "plot": "Luke Skywalker joins forces with a Jedi Knight."})
        elif opcion == 2:
            print("Creando relaciones...")
            neo4j_func.create_relationship("User", {"name": "Juan", "userId": 1}, "Movie", {"movieId": 1}, "RATED", {"rating": 5, "timestamp": 123456})
            neo4j_func.create_relationship("User", {"name": "Carlos", "userId": 5}, "Movie", {"title": "Star Wars", "movieId": 2}, "RATED", {"rating": 4, "timestamp": 123457})
        elif opcion == 3:
            print("Buscando...\n")
            users = neo4j_func.find_nodes("User", {"name": "Juan", "userId": 1})
            print("Usuarios encontrados:\n")
            print(users)
            print("\n")
            movies = neo4j_func.find_nodes("Movie", {"title": "Matrix", "movieId": 1})
            print("Películas encontradas:\n")
            print(movies)
            print("\n")
            data = neo4j_func.find_nodes_with_relationships("User", {"name": "Juan", "userId": 1}, "Movie", {"movieId": 1}, "RATED", {"rating": 5})
            print("Relación encontrada:\n")
            print(data)
            print("\n")
        elif opcion == 4:   
            print("Creando grafo de usuarios y películas...")
            neo4j_func.create_node("User", {"name": "Nelson", "userId": 6})
            neo4j_func.create_node(
                label="Person:Actor:Director",
                properties={
                    "name": "Chadwick Boseman",
                    "tmdbId": 12345,
                    "born": "1976-11-29T00:00:00",
                    "died": "2020-08-28T00:00:00",
                    "bornIn": "Anderson, South Carolina, USA",
                    "url": "https://www.themoviedb.org/person/12345",
                    "imdbId": 67890,
                    "bio": "American actor known for playing Black Panther.",
                    "poster": "https://image.tmdb.org/t/p/original/poster.jpg"
                }
            )
            neo4j_func.create_node(
                label="Person:Actor",
                properties={
                    "name": "Keanu Reeves",
                    "tmdbId": 23456,
                    "born": "1964-09-02T00:00:00",
                    "died": None,
                    "bornIn": "Beirut, Lebanon",
                    "url": "https://www.themoviedb.org/person/23456",
                    "bio": "Canadian actor known for playing Neo in The Matrix.",
                    "poster": "https://image.tmdb.org/t/p/original/poster.jpg"
                }
            )
            neo4j_func.create_node(
                label="Person:Director",
                properties={
                    "name": "Lana Wachowski",
                    "tmdbId": 34567,
                    "born": "1965-06-21T00:00:00",
                    "died": None,
                    "bornIn": "Chicago, Illinois, USA",
                    "url": "https://www.themoviedb.org/person/34567",
                    "bio": "American film director known for co-directing The Matrix trilogy.",
                    "poster": "https://image.tmdb.org/t/p/original/poster.jpg"
                }
            )
            neo4j_func.create_node("Genre", {"name": "Action"})
            neo4j_func.create_node(
                label="Movie",
                properties={
                    "title": "Black Panther",
                    "tmdbId": 284054,
                    "released": "2018-02-16T00:00:00",
                    "imdbRating": 7.3,
                    "movieId": 3,
                    "year": 2018,
                    "imdbId": 1825683,
                    "runtime": 134,
                    "countries": ["USA"],
                    "imdbVotes": 690000,
                    "url": "https://www.themoviedb.org/movie/284054",
                    "revenue": 1346913161,
                    "plot": "T'Challa, the King of Wakanda, rises to the throne in the isolated, technologically advanced African nation...",
                    "poster": "https://image.tmdb.org/t/p/original/poster.jpg",
                    "budget": 200000000,
                    "languages": ["English", "Spanish", "Korean"]
                }
            )
            neo4j_func.create_relationship("Person:Actor:Director", {"name": "Chadwick Boseman", "tmdbId": 12345}, "Movie", {"title": "Black Panther", "tmdbId": 284054}, "ACTED_IN", {"role": "T'Challa / Black Panther"})
            neo4j_func.create_relationship("Person:Actor:Director", {"name": "Chadwick Boseman", "tmdbId": 12345}, "Movie", {"title": "Black Panther", "tmdbId": 284054}, "DIRECTED")
            neo4j_func.create_relationship("Person:Actor", {"name": "Keanu Reeves", "tmdbId": 23456}, "Movie", {"title": "Black Panther", "tmdbId": 284054}, "ACTED_IN", {"role": "Neo"})
            neo4j_func.create_relationship("Person:Director", {"name": "Lana Wachowski", "tmdbId": 34567}, "Movie", {"title": "Black Panther", "tmdbId": 284054}, "DIRECTED", {"role": "Director"})
            neo4j_func.create_relationship("User", {"name": "Nelson", "userId": 6}, "Movie", {"title": "Black Panther", "tmdbId": 284054}, "RATED", {"rating": 5, "timestamp": 123458})
            neo4j_func.create_relationship("Movie", {"title": "Black Panther", "tmdbId": 284054}, "Genre", {"name": "Terror"}, "IN_GENRE")



    neo4j_func.connector.close()