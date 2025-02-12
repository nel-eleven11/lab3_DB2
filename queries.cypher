//Para incisos 1 a 3
//Crear un usuario

MERGE (u:user {name: 'name', userId: 1}) RETURN u;

//Crear una pelicula

MERGE (m:movie {title: 'movie', movieId: 1, year: 1, plot: 'plot'}) RETURN m;


//Crear una relacion entre un usuario y una pelicula

MERGE (u:user {name: 'name', userId: '1'}) MERGE (u)-[r: RATED {rating: 5, timestamp: 0}]-> (m: movie {title: 'movie', movieId: '1', year: 0, plot: 'plot'}) RETURN u, r, m;

//Buscar un usuario, una película y un usuario con su relación rate a película

MATCH (u:user {name: 'name', userId: '1'}) MATCH (m:movie {title: 'movie', movieId: '1', year: 0, plot: 'plot'}) MATCH (u)-[r:RATED {rating: 5, timestamp: 0}]->(m) RETURN u, r, m;

//Para inciso 4

