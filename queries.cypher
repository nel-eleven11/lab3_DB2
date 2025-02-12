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

//Crear una persona que sea actor, director 
MERGE (pad: personActorDirector {name: 'name', tmdbId: 1, born: 1, died: 1, bornIn: 's', url: '', imdbId: 1, bio: '', poster: ''}) RETURN pad;

//Crear una persona que sea actor
MERGE (pa: personActor {name: 'name', tmdbId: 1, born: 1, died: 1, bornIn: 's', url: '', imdbId: 1, bio: '', poster: ''}) RETURN pa;

//Crear una persona que sea director
MERGE (pd: personDirector {name: 'name', tmdbId: 1, born: 1, died: 1, bornIn: 's', url: '', imdbId: 1, bio: '', poster: ''}) RETURN pd;

//Crear un usuario
MERGE (u:user {name: 'name', userId: 1}) RETURN u;

//Crear una película
MERGE (m: movie {title: '', tmdbld: 1, released: 1, imdbRating: 1, movieId: 1, year: 1, imdbId: 1, runtime: 1, countries: [''], imdbVotes: 1, url: '', revenue: 1, plot: '', poster: '', budget: 1, languages: [''] }) RETURN m;

//Crear un genero
MERGE (g: genre {name: 'name'}) RETURN g;

//Crear una relacion entre una persona que es actor y director y actuó en una película
MERGE (pad: personActorDirector {name: 'name', tmdbId: 1, born: 1, died: 1, bornIn: 's', url: '', imdbId: 1, bio: '', poster: ''}) 
MERGE (pad)-[a: ACTED_IN {role: ''}]->(m: movie {title: '', tmdbld: 1, released: 1, imdbRating: 1, movieId: 1, year: 1, imdbId: 1, runtime: 1, countries: [''], imdbVotes: 1, url: '', revenue: 1, plot: '', poster: '', budget: 1, languages: [''] }) RETURN pad, a, m;

//Crear una relacion entre una persona que es actor y director y dirigió  una película
MERGE (pad: personActorDirector {name: 'name', tmdbId: 1, born: 1, died: 1, bornIn: 's', url: '', imdbId: 1, bio: '', poster: ''}) 
MERGE (pad)-[d: DIRECTED]->(m: movie {title: '', tmdbld: 1, released: 1, imdbRating: 1, movieId: 1, year: 1, imdbId: 1, runtime: 1, countries: [''], imdbVotes: 1, url: '', revenue: 1, plot: '', poster: '', budget: 1, languages: [''] }) RETURN pad, d, m;

//Crear una relacion entre un actor y una película
MERGE (pa: personActor {name: 'name', tmdbId: 1, born: 1, died: 1, bornIn: 's', url: '', imdbId: 1, bio: '', poster: ''})
MERGE (pa)-[a: ACTED_IN {role: ''}]->(m: movie {title: '', tmdbld: 1, released: 1, imdbRating: 1, movieId: 1, year: 1, imdbId: 1, runtime: 1, countries: [''], imdbVotes: 1, url: '', revenue: 1, plot: '', poster: '', budget: 1, languages: [''] }) RETURN pa, a, m;

//Crear una relacion entre un director y una película
MERGE (pd: personDirector {name: 'name', tmdbId: 1, born: 1, died: 1, bornIn: 's', url: '', imdbId: 1, bio: '', poster: ''})
MERGE (pd)-[d: DIRECTED]->(m: movie {title: '', tmdbld: 1, released: 1, imdbRating: 1, movieId: 1, year: 1, imdbId: 1, runtime: 1, countries: [''], imdbVotes: 1, url: '', revenue: 1, plot: '', poster: '', budget: 1, languages: [''] }) RETURN pd, d, m;

//Crear una relacion entre una película y un genero
MERGE (m: movie {title: '', tmdbld: 1, released: 1, imdbRating: 1, movieId: 1, year: 1, imdbId: 1, runtime: 1, countries: [''], imdbVotes: 1, url: '', revenue: 1, plot: '', poster: '', budget: 1, languages: [''] })
MERGE (m)-[i: IN_GENRE]->(g: genre {name: 'name'}) RETURN m, i;
