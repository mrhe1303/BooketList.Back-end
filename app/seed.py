import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from app.database import db
from app.models.user import User
from app.models.author import Author
from app.models.book import Book
from app.models.rating import Rating
from app.models.user_library import UserLibrary
import random
from app.models.admin import Admin

app = create_app()

def seed_database():
    with app.app_context():
        print("🗑️ Limpiando base de datos...")
        
        # Limpiar tablas en el orden correcto (respetando foreign keys)
        UserLibrary.query.delete()
        Rating.query.delete()
        Book.query.delete()
        Author.query.delete()
        User.query.delete()
        Admin.query.delete()
        
        # ===== CREAR ADMIN PRINCIPAL =====
        print("👨‍💼 Creando administrador principal...")
        admin = Admin(
            nombre_admin="Administrador Principal",
            email_admin="admin@booketlist.com",
            password_admin="admin123"
        )
        db.session.add(admin)
        db.session.commit()
        print(f"✓ Admin creado - Email: {admin.email_admin}")
        
        print("👥 Creando autores...")
        
        # COMPLETE LIST OF ALL AUTHORS FROM TXT FILE
        autores_data = [
            # Index 0-9: Clásicos Authors
            {"nombre": "Miguel", "apellido": "de Cervantes", "biografia": "Escritor español, autor de Don Quijote de la Mancha."},
            {"nombre": "Jane", "apellido": "Austen", "biografia": "Novelista británica conocida por sus novelas de crítica social y romance."},
            {"nombre": "Fiódor", "apellido": "Dostoyevski", "biografia": "Escritor ruso, uno de los principales novelistas de la literatura universal."},
            {"nombre": "Herman", "apellido": "Melville", "biografia": "Escritor estadounidense, autor de Moby Dick."},
            {"nombre": "Homero", "apellido": "", "biografia": "Poeta griego antiguo, autor de La Ilíada y La Odisea."},
            {"nombre": "Marcel", "apellido": "Proust", "biografia": "Novelista francés, autor de En busca del tiempo perdido."},
            {"nombre": "William", "apellido": "Shakespeare", "biografia": "Dramaturgo y poeta inglés."},
            {"nombre": "Dante", "apellido": "Alighieri", "biografia": "Poeta italiano, autor de La Divina Comedia."},
            {"nombre": "León", "apellido": "Tolstói", "biografia": "Novelista ruso, autor de Guerra y Paz y Anna Karénina."},
            {"nombre": "Charles", "apellido": "Dickens", "biografia": "Escritor británico."},
            # Index 10-17: Additional classic/modern authors
            {"nombre": "James", "apellido": "Joyce", "biografia": "Escritor irlandés, autor de Ulises."},
            {"nombre": "Gustave", "apellido": "Flaubert", "biografia": "Escritor francés, autor de Madame Bovary."},
            {"nombre": "Albert", "apellido": "Camus", "biografia": "Escritor y filósofo francés."},
            {"nombre": "Mark", "apellido": "Twain", "biografia": "Escritor estadounidense."},
            {"nombre": "Charlotte", "apellido": "Brontë", "biografia": "Escritora británica, autora de Jane Eyre."},
            {"nombre": "Franz", "apellido": "Kafka", "biografia": "Escritor checo de habla alemana."},
            {"nombre": "Ovidio", "apellido": "", "biografia": "Poeta romano."},
            {"nombre": "Giovanni", "apellido": "Boccaccio", "biografia": "Escritor italiano del siglo XIV."},
            # Index 18-27: Non-Fiction Authors
            {"nombre": "Yuval Noah", "apellido": "Harari", "biografia": "Historiador y escritor israelí."},
            {"nombre": "Tara", "apellido": "Westover", "biografia": "Escritora estadounidense."},
            {"nombre": "Eckhart", "apellido": "Tolle", "biografia": "Escritor y maestro espiritual."},
            {"nombre": "Daniel", "apellido": "Kahneman", "biografia": "Psicólogo y premio Nobel de Economía."},
            {"nombre": "Stephen", "apellido": "Hawking", "biografia": "Físico teórico británico."},
            {"nombre": "Ana", "apellido": "Frank", "biografia": "Diarista judía víctima del Holocausto."},
            {"nombre": "Viktor", "apellido": "Frankl", "biografia": "Psiquiatra austriaco, sobreviviente del Holocausto."},
            {"nombre": "Stephen R.", "apellido": "Covey", "biografia": "Escritor y consultor empresarial."},
            {"nombre": "James", "apellido": "Clear", "biografia": "Escritor y conferencista sobre hábitos."},
            {"nombre": "Elizabeth", "apellido": "Gilbert", "biografia": "Escritora estadounidense."},
            # Index 28-36: More Non-Fiction
            {"nombre": "Michael", "apellido": "Pollan", "biografia": "Periodista y autor sobre alimentación."},
            {"nombre": "Siddhartha", "apellido": "Mukherjee", "biografia": "Médico y escritor."},
            {"nombre": "Malcolm", "apellido": "Gladwell", "biografia": "Periodista y escritor canadiense."},
            {"nombre": "Carl", "apellido": "Sagan", "biografia": "Astrofísico y divulgador científico."},
            {"nombre": "Christopher", "apellido": "McDougall", "biografia": "Escritor y periodista."},
            {"nombre": "Matthew", "apellido": "Walker", "biografia": "Neurocientífico especialista en sueño."},
            {"nombre": "Daniel", "apellido": "Goleman", "biografia": "Psicólogo y periodista científico."},
            {"nombre": "Charles", "apellido": "Darwin", "biografia": "Naturalista y biólogo."},
            {"nombre": "Jared", "apellido": "Diamond", "biografia": "Geógrafo y biólogo evolutivo."},
            # Index 37-52: Sci-Fi Authors
            {"nombre": "Frank", "apellido": "Herbert", "biografia": "Escritor estadounidense de ciencia ficción."},
            {"nombre": "Isaac", "apellido": "Asimov", "biografia": "Escritor y bioquímico, maestro de la ciencia ficción."},
            {"nombre": "George", "apellido": "Orwell", "biografia": "Escritor británico, autor de 1984."},
            {"nombre": "Aldous", "apellido": "Huxley", "biografia": "Escritor británico."},
            {"nombre": "William", "apellido": "Gibson", "biografia": "Escritor estadounidense-canadiense, padre del cyberpunk."},
            {"nombre": "Orson Scott", "apellido": "Card", "biografia": "Escritor estadounidense de ciencia ficción."},
            {"nombre": "Ray", "apellido": "Bradbury", "biografia": "Escritor estadounidense."},
            {"nombre": "Ursula K.", "apellido": "Le Guin", "biografia": "Escritora estadounidense de ciencia ficción y fantasía."},
            {"nombre": "Stanisław", "apellido": "Lem", "biografia": "Escritor polaco de ciencia ficción."},
            {"nombre": "H.G.", "apellido": "Wells", "biografia": "Escritor británico, pionero de la ciencia ficción."},
            {"nombre": "Philip K.", "apellido": "Dick", "biografia": "Escritor estadounidense de ciencia ficción."},
            {"nombre": "Dan", "apellido": "Simmons", "biografia": "Escritor estadounidense."},
            {"nombre": "Joe", "apellido": "Haldeman", "biografia": "Escritor estadounidense de ciencia ficción."},
            {"nombre": "Richard K.", "apellido": "Morgan", "biografia": "Escritor británico."},
            {"nombre": "Kurt", "apellido": "Vonnegut", "biografia": "Escritor estadounidense."},
            {"nombre": "James S.A.", "apellido": "Corey", "biografia": "Seudónimo de Daniel Abraham y Ty Franck."},
            # Index 53-67: Fiction Authors
            {"nombre": "F. Scott", "apellido": "Fitzgerald", "biografia": "Escritor estadounidense."},
            {"nombre": "Harper", "apellido": "Lee", "biografia": "Escritora estadounidense."},
            {"nombre": "J.D.", "apellido": "Salinger", "biografia": "Escritor estadounidense."},
            {"nombre": "J.R.R.", "apellido": "Tolkien", "biografia": "Escritor británico."},
            {"nombre": "Dan", "apellido": "Brown", "biografia": "Escritor estadounidense."},
            {"nombre": "Suzanne", "apellido": "Collins", "biografia": "Escritora estadounidense."},
            {"nombre": "Carlos", "apellido": "Ruiz Zafón", "biografia": "Escritor español."},
            {"nombre": "J.K.", "apellido": "Rowling", "biografia": "Escritora británica."},
            {"nombre": "Emily", "apellido": "Brontë", "biografia": "Escritora británica."},
            {"nombre": "Oscar", "apellido": "Wilde", "biografia": "Escritor irlandés."},
            {"nombre": "Ken", "apellido": "Follett", "biografia": "Escritor británico."},
            {"nombre": "Margaret", "apellido": "Atwood", "biografia": "Escritora canadiense."},
            {"nombre": "Patrick", "apellido": "Süskind", "biografia": "Escritor alemán."},
            {"nombre": "Patrick", "apellido": "Rothfuss", "biografia": "Escritor estadounidense."},
            {"nombre": "Toni", "apellido": "Morrison", "biografia": "Escritora estadounidense, premio Nobel."},
            # Index 68-82: Latin American Authors
            {"nombre": "Gabriel", "apellido": "García Márquez", "biografia": "Escritor colombiano, premio Nobel."},
            {"nombre": "Isabel", "apellido": "Allende", "biografia": "Escritora chilena."},
            {"nombre": "Julio", "apellido": "Cortázar", "biografia": "Escritor argentino."},
            {"nombre": "Juan", "apellido": "Rulfo", "biografia": "Escritor mexicano."},
            {"nombre": "Mario", "apellido": "Vargas Llosa", "biografia": "Escritor peruano, premio Nobel."},
            {"nombre": "Ernesto", "apellido": "Sabato", "biografia": "Escritor argentino."},
            {"nombre": "Laura", "apellido": "Esquivel", "biografia": "Escritora mexicana."},
            {"nombre": "Jorge Luis", "apellido": "Borges", "biografia": "Escritor argentino."},
            {"nombre": "Roberto", "apellido": "Bolaño", "biografia": "Escritor chileno."},
            {"nombre": "Mario", "apellido": "Benedetti", "biografia": "Escritor uruguayo."},
            {"nombre": "Carlos", "apellido": "Fuentes", "biografia": "Escritor mexicano."},
            {"nombre": "José Eustasio", "apellido": "Rivera", "biografia": "Escritor colombiano."},
            {"nombre": "Alejo", "apellido": "Carpentier", "biografia": "Escritor cubano."},
            {"nombre": "Manuel", "apellido": "Puig", "biografia": "Escritor argentino."},
            {"nombre": "Tomás Eloy", "apellido": "Martínez", "biografia": "Escritor argentino."},
            # Index 83-95: Historia Authors
            {"nombre": "Umberto", "apellido": "Eco", "biografia": "Escritor italiano."},
            {"nombre": "Chimamanda", "apellido": "Ngozi Adichie", "biografia": "Escritora nigeriana."},
            {"nombre": "Stefan", "apellido": "Zweig", "biografia": "Escritor austriaco."},
            {"nombre": "Victor", "apellido": "Hugo", "biografia": "Escritor francés."},
            {"nombre": "Marguerite", "apellido": "Yourcenar", "biografia": "Escritora francesa."},
            {"nombre": "Robert", "apellido": "Graves", "biografia": "Escritor británico."},
            {"nombre": "John", "apellido": "Kennedy Toole", "biografia": "Escritor estadounidense."},
            {"nombre": "Noah", "apellido": "Gordon", "biografia": "Escritor estadounidense."},
            {"nombre": "James", "apellido": "Clavell", "biografia": "Escritor australiano-británico."},
            {"nombre": "James Fenimore", "apellido": "Cooper", "biografia": "Escritor estadounidense."},
            {"nombre": "Ildefonso", "apellido": "Falcones", "biografia": "Escritor español."},
            {"nombre": "Miguel", "apellido": "Delibes", "biografia": "Escritor español."},
            {"nombre": "Arturo", "apellido": "Pérez-Reverte", "biografia": "Escritor español."},
        ]
        
        autores = []
        for autor_data in autores_data:
            autor = Author(
                nombre_autor=autor_data["nombre"],
                apellido_autor=autor_data["apellido"],
                biografia_autor=autor_data["biografia"]
            )
            db.session.add(autor)
            autores.append(autor)
        
        db.session.commit()
        print(f"✓ {len(autores)} autores creados")
        
        print("📚 Creando libros...")
        
        # ALL BOOKS IN A SINGLE LIST (NOT SEPARATED BY GENRE)
        libros_data = [
            # CLÁSICOS (20 books - indices 0-19)
            {"titulo": "Don Quijote de la Mancha", "autor_index": 0, "genero": "Clásicos", "descripcion": "Las aventuras del ingenioso hidalgo que pierde la razón por leer novelas de caballería y sale a desfacer entuertos.", "asin": "8491057536", "portada": "https://m.media-amazon.com/images/I/81-ylKA1wJL._SL1500_.jpg"},
            {"titulo": "Orgullo y Prejuicio", "autor_index": 1, "genero": "Clásicos", "descripcion": "Elizabeth Bennet y Mr. Darcy superan sus prejuicios iniciales en esta brillante sátira sobre el matrimonio y la sociedad inglesa.", "asin": "8491051325", "portada": "https://m.media-amazon.com/images/I/71KZzetNT9L._SL1500_.jpg"},
            {"titulo": "Crimen y Castigo", "autor_index": 2, "genero": "Clásicos", "descripcion": "Raskólnikov asesina a una anciana usurera y enfrenta las consecuencias psicológicas de su acto en la San Petersburgo del siglo XIX.", "asin": "B0DWKBCSL2", "portada": "https://m.media-amazon.com/images/I/71jl4XMVEKL._SL1329_.jpg"},
            {"titulo": "Moby Dick", "autor_index": 3, "genero": "Clásicos", "descripcion": "El capitán Ahab persigue obsesivamente a la ballena blanca que le arrancó una pierna en una travesía hacia la autodestrucción.", "asin": "8491050205", "portada": "https://m.media-amazon.com/images/I/81-jgO4Zm8L._SL1500_.jpg"},
            {"titulo": "La Odisea", "autor_index": 4, "genero": "Clásicos", "descripcion": "El épico viaje de Odiseo de regreso a Ítaca tras la Guerra de Troya, enfrentando monstruos, dioses y su propio destino.", "asin": "8413625173", "portada": "https://m.media-amazon.com/images/I/61O4h3WIM0L._SL1050_.jpg"},
            {"titulo": "Los Hermanos Karamazov", "autor_index": 2, "genero": "Clásicos", "descripcion": "Tres hermanos de personalidades opuestas enfrentan cuestiones de fe, moralidad y libre albedrío tras la muerte de su padre.", "asin": "8491050051", "portada": "https://m.media-amazon.com/images/I/81yq7rUwYmL._SL1500_.jpg"},
            {"titulo": "En Busca del Tiempo Perdido", "autor_index": 5, "genero": "Clásicos", "descripcion": "Monumental exploración de la memoria, el tiempo y la sociedad francesa a través de las reminiscencias del narrador.", "asin": "B09FS9PMKS", "portada": "https://m.media-amazon.com/images/I/61CNCVKq6cL._SL1500_.jpg"},
            {"titulo": "Hamlet", "autor_index": 6, "genero": "Clásicos", "descripcion": "El príncipe de Dinamarca busca vengar el asesinato de su padre mientras lucha contra la duda, la locura y el destino.", "asin": "B0CT1FB5QN", "portada": "https://m.media-amazon.com/images/I/71uz9igbHrL._SL1500_.jpg"},
            {"titulo": "La Divina Comedia", "autor_index": 7, "genero": "Clásicos", "descripcion": "Dante viaja por el Infierno, el Purgatorio y el Paraíso en una obra maestra alegórica sobre el alma y la salvación.", "asin": "1518711375", "portada": "https://m.media-amazon.com/images/I/71WJbXGxPdL._SL1360_.jpg"},
            {"titulo": "Guerra y Paz", "autor_index": 8, "genero": "Clásicos", "descripcion": "Familias aristocráticas rusas viven amores, tragedias y transformaciones durante las guerras napoleónicas en esta épica monumental.", "asin": "B091FMWH1Z", "portada": "https://m.media-amazon.com/images/I/91bx-1HHXGL._SL1500_.jpg"},
            {"titulo": "Ulises", "autor_index": 10, "genero": "Clásicos", "descripcion": "Un día en la vida de Leopold Bloom en Dublín, obra modernista que revolucionó la literatura con su técnica de flujo de conciencia.", "asin": "8466359400", "portada": "https://m.media-amazon.com/images/I/91G1mqR54dS._SL1500_.jpg"},
            {"titulo": "Anna Karenina", "autor_index": 8, "genero": "Clásicos", "descripcion": "La trágica historia de Ana, atrapada entre su pasión por Vronsky y las convenciones sociales de la Rusia aristocrática.", "asin": "8491055185", "portada": "https://m.media-amazon.com/images/I/91Jd4RA0A+L._SL1500_.jpg"},
            {"titulo": "Madame Bovary", "autor_index": 11, "genero": "Clásicos", "descripcion": "Emma Bovary busca romance y pasión fuera de su matrimonio aburrido, llevándola a una espiral de deudas y desilusión.", "asin": "1543018882", "portada": "https://m.media-amazon.com/images/I/61ivxzAGxkL._SL1360_.jpg"},
            {"titulo": "El Extranjero", "autor_index": 12, "genero": "Clásicos", "descripcion": "Meursault, un hombre emocionalmente distante, comete un asesinato absurdo en la Argelia francesa en esta obra existencialista.", "asin": "8439737939", "portada": "https://m.media-amazon.com/images/I/71rWL9HWODL._SL1500_.jpg"},
            {"titulo": "Las Aventuras de Tom Sawyer", "autor_index": 13, "genero": "Clásicos", "descripcion": "Las travesuras de un niño ingenioso en el Mississippi, desde presenciar un asesinato hasta buscar tesoros piratas escondidos.", "asin": "B0CHL3RW8P", "portada": "https://m.media-amazon.com/images/I/61SETni1pyL._SL1331_.jpg"},
            {"titulo": "Jane Eyre", "autor_index": 14, "genero": "Clásicos", "descripcion": "Una huérfana se convierte en institutriz y se enamora de su empleador, Mr. Rochester, cuyo oscuro secreto amenaza su felicidad.", "asin": "B01CDIDB02", "portada": "https://m.media-amazon.com/images/I/71HFFFVN2+L._SL1500_.jpg"},
            {"titulo": "El Proceso", "autor_index": 15, "genero": "Clásicos", "descripcion": "Josef K es arrestado y procesado por un crimen desconocido en un sistema judicial absurdo y burocrático kafkiano.", "asin": "8420678198", "portada": "https://m.media-amazon.com/images/I/71E8PQ0bN6L._SL1500_.jpg"},
            {"titulo": "Grandes Esperanzas", "autor_index": 9, "genero": "Clásicos", "descripcion": "Pip, un huérfano pobre, recibe una misteriosa fortuna que transforma su vida pero desafía sus valores sobre clase y amor.", "asin": "1986946304", "portada": "https://m.media-amazon.com/images/I/816+kfiuWJL._SL1360_.jpg"},
            {"titulo": "Metamorfosis", "autor_index": 16, "genero": "Clásicos", "descripcion": "Colección épica de mitos griegos y romanos sobre transformaciones, desde la creación del mundo hasta la deificación de César.", "asin": "1470156202", "portada": "https://m.media-amazon.com/images/I/71f6hk9pBFL._SL1360_.jpg"},
            {"titulo": "El Decamerón", "autor_index": 17, "genero": "Clásicos", "descripcion": "Diez jóvenes escapan de la peste negra en Florencia y se entretienen contando cien historias de amor, engaño y aventura.", "asin": "153971070X", "portada": "https://m.media-amazon.com/images/I/71nk4Tk9hkL._SL1360_.jpg"},
            
            # NO-FICCIÓN (20 books)
            {"titulo": "Sapiens: De Animales a Dioses", "autor_index": 18, "genero": "No-Ficción", "descripcion": "Una exploración fascinante de la historia de la humanidad desde nuestros orígenes hasta la actualidad y nuestro futuro.", "asin": "841939971X", "portada": "https://m.media-amazon.com/images/I/717sO7vkyUL._SL1500_.jpg"},
            {"titulo": "Una Educación", "autor_index": 19, "genero": "No-Ficción", "descripcion": "Memorias de una mujer criada por fundamentalistas mormones que nunca fue a la escuela hasta obtener un doctorado en Cambridge.", "asin": "B0D1RBR9XW", "portada": "https://m.media-amazon.com/images/I/71JoUjDA0CL._SL1500_.jpg"},
            {"titulo": "El Poder del Ahora", "autor_index": 20, "genero": "No-Ficción", "descripcion": "Guía espiritual para vivir en el momento presente, liberándose del dolor emocional del pasado y la ansiedad del futuro.", "asin": "8484450341", "portada": "https://m.media-amazon.com/images/I/31gCZ3hEQ5L.jpg"},
            {"titulo": "Pensar Rápido, Pensar Despacio", "autor_index": 21, "genero": "No-Ficción", "descripcion": "El premio Nobel de Economía explica los dos sistemas de pensamiento que moldean nuestras decisiones y juicios cotidianos.", "asin": "B085NZ4HVD", "portada": "https://m.media-amazon.com/images/I/71sy-wpVL-L._SL1500_.jpg"},
            {"titulo": "Historia del tiempo: Del big bang a los agujeros negros", "autor_index": 22, "genero": "No-Ficción", "descripcion": "El célebre físico explica los grandes misterios del universo: agujeros negros, el Big Bang y la naturaleza del tiempo.", "asin": "8420651990", "portada": "https://m.media-amazon.com/images/I/71PxtZIcvML._SL1500_.jpg"},
            {"titulo": "El Diario de Ana Frank", "autor_index": 23, "genero": "No-Ficción", "descripcion": "El testimonio auténtico de una adolescente judía escondida durante el Holocausto, símbolo universal de esperanza y resistencia.", "asin": "0525565884", "portada": "https://m.media-amazon.com/images/I/71QANHhE33L._SL1500_.jpg"},
            {"titulo": "Homo Deus: Breve Historia del Mañana", "autor_index": 18, "genero": "No-Ficción", "descripcion": "Explora el futuro de la humanidad en una era donde la tecnología podría convertirnos en dioses o hacernos obsoletos.", "asin": "8499926711", "portada": "https://m.media-amazon.com/images/I/81kZpuvRoFL._SL1500_.jpg"},
            {"titulo": "Armas, Gérmenes y Acero", "autor_index": 36, "genero": "No-Ficción", "descripcion": "Análisis profundo sobre cómo factores geográficos y ambientales determinaron el destino de las civilizaciones humanas.", "asin": "8499928714", "portada": "https://m.media-amazon.com/images/I/81etu+U84iL._SL1500_.jpg"},
            {"titulo": "El Hombre en Busca de Sentido", "autor_index": 24, "genero": "No-Ficción", "descripcion": "El psiquiatra sobreviviente del Holocausto explora cómo encontrar propósito y significado incluso en el sufrimiento extremo.", "asin": "8425451094", "portada": "https://m.media-amazon.com/images/I/61yfWdq5+zL._SL1050_.jpg"},
            {"titulo": "Los Siete Hábitos de la Gente Altamente Efectiva", "autor_index": 25, "genero": "No-Ficción", "descripcion": "Principios fundamentales para el desarrollo personal y profesional que han transformado millones de vidas en todo el mundo.", "asin": "6075695591", "portada": "https://m.media-amazon.com/images/I/617AqnsUdqL._SL1500_.jpg"},
            {"titulo": "Hábitos Atómicos", "autor_index": 26, "genero": "No-Ficción", "descripcion": "Estrategias prácticas para formar buenos hábitos, romper malos y dominar comportamientos que llevan al éxito duradero.", "asin": "6075694129", "portada": "https://m.media-amazon.com/images/I/713PN1USzXL._SL1228_.jpg"},
            {"titulo": "Come, Reza, Ama", "autor_index": 27, "genero": "No-Ficción", "descripcion": "Memorias de una mujer que viaja por Italia, India e Indonesia buscando placer, espiritualidad y equilibrio tras su divorcio.", "asin": "1644732734", "portada": "https://m.media-amazon.com/images/I/71fG+Rte1IL._SL1500_.jpg"},
            {"titulo": "En Defensa de la Comida", "autor_index": 28, "genero": "No-Ficción", "descripcion": "Un manifiesto sobre nutrición que resume la alimentación saludable en siete palabras: Come comida, no mucha, principalmente plantas.", "asin": "0143114964", "portada": "https://m.media-amazon.com/images/I/71NVcW6g3LL._SL1500_.jpg"},
            {"titulo": "El Gen: Una Historia Íntima", "autor_index": 29, "genero": "No-Ficción", "descripcion": "La historia de la genética desde Mendel hasta CRISPR, entrelazada con la historia familiar del autor sobre enfermedades mentales.", "asin": "1476733503", "portada": "https://m.media-amazon.com/images/I/71knXNNQMwL._SL1500_.jpg"},
            {"titulo": "Fuera de Serie", "autor_index": 30, "genero": "No-Ficción", "descripcion": "Explora cómo el éxito excepcional depende más de oportunidades, tiempo de práctica y contexto cultural que del talento puro.", "asin": "B0D6XPJRKZ", "portada": "https://m.media-amazon.com/images/I/71sDcx7hQyL._SL1500_.jpg"},
            {"titulo": "El Mundo y Sus Demonios", "autor_index": 31, "genero": "No-Ficción", "descripcion": "Una defensa apasionada del pensamiento crítico y el método científico contra la pseudociencia y la superstición moderna.", "asin": "8408058193", "portada": "https://m.media-amazon.com/images/I/51b3VxpNhhL._SL1181_.jpg"},
            {"titulo": "Nacidos para Correr", "autor_index": 32, "genero": "No-Ficción", "descripcion": "La búsqueda del autor de los secretos de los Tarahumara, una tribu mexicana de superatletas que corren descalzos.", "asin": "030774129X", "portada": "https://m.media-amazon.com/images/I/812qP+2a1EL._SL1500_.jpg"},
            {"titulo": "Por Qué Dormimos", "autor_index": 33, "genero": "No-Ficción", "descripcion": "Un neurocientífico revela la ciencia del sueño y su impacto crítico en la salud, aprendizaje y esperanza de vida.", "asin": "8412064526", "portada": "https://m.media-amazon.com/images/I/61Xf8V-H2uL._SL1200_.jpg"},
            {"titulo": "Inteligencia Emocional", "autor_index": 34, "genero": "No-Ficción", "descripcion": "Por qué la inteligencia emocional puede importar más que el coeficiente intelectual para el éxito personal y profesional.", "asin": "1947783424", "portada": "https://m.media-amazon.com/images/I/71m4GrUv9VL._SL1500_.jpg"},
            {"titulo": "El Origen de las Especies", "autor_index": 35, "genero": "No-Ficción", "descripcion": "La obra fundamental que introduce la teoría de la evolución por selección natural, revolucionando la biología moderna.", "asin": "B0DYK36QLB", "portada": "https://m.media-amazon.com/images/I/514CvkyD7QL._SL1491_.jpg"},
            
            # CIENCIA FICCIÓN (20 books)
            {"titulo": "Dune", "autor_index": 37, "genero": "Ciencia Ficción", "descripcion": "Paul Atreides debe sobrevivir en el desierto planeta Arrakis, fuente de la sustancia más valiosa del universo: la especia.", "asin": "8466363408", "portada": "https://m.media-amazon.com/images/I/91bNnC0hTFL._SL1500_.jpg"},
            {"titulo": "Fundación", "autor_index": 38, "genero": "Ciencia Ficción", "descripcion": "Hari Seldon predice la caída del Imperio Galáctico y crea la Fundación para preservar el conocimiento y acortar la edad oscura.", "asin": "8497599241", "portada": "https://m.media-amazon.com/images/I/91ktHAuXOCL._SL1500_.jpg"},
            {"titulo": "1984", "autor_index": 39, "genero": "Ciencia Ficción", "descripcion": "Una distopía totalitaria donde el Gran Hermano controla cada aspecto de la vida mediante vigilancia, propaganda y manipulación.", "asin": "6073844328", "portada": "https://m.media-amazon.com/images/I/51GPJUr5v0L._SL1157_.jpg"},
            {"titulo": "Un Mundo Feliz", "autor_index": 40, "genero": "Ciencia Ficción", "descripcion": "En una sociedad futurista donde todos son felices mediante condicionamiento y drogas, un hombre cuestiona este orden perfecto.", "asin": "8466350942", "portada": "https://m.media-amazon.com/images/I/81glRrzOepL._SL1500_.jpg"},
            {"titulo": "Neuromante", "autor_index": 41, "genero": "Ciencia Ficción", "descripcion": "Case, un hacker caído en desgracia, es contratado para el último trabajo: hackear una inteligencia artificial en el ciberespacio.", "asin": "8445070843", "portada": "https://m.media-amazon.com/images/I/81ZE-kY+ynL._SL1500_.jpg"},
            {"titulo": "El Juego de Ender", "autor_index": 42, "genero": "Ciencia Ficción", "descripcion": "Ender Wiggin, un niño genio, es entrenado en una escuela militar espacial para liderar la lucha contra una invasión alienígena.", "asin": "8420434191", "portada": "https://m.media-amazon.com/images/I/91fqbLUmU0L._SL1500_.jpg"},
            {"titulo": "Fahrenheit 451", "autor_index": 43, "genero": "Ciencia Ficción", "descripcion": "En una sociedad donde los libros están prohibidos, el bombero Guy Montag comienza a cuestionar su trabajo de quemar literatura.", "asin": "1644730537", "portada": "https://m.media-amazon.com/images/I/713hU5z9iaL._SL1500_.jpg"},
            {"titulo": "La Mano Izquierda de la Oscuridad", "autor_index": 44, "genero": "Ciencia Ficción", "descripcion": "Un enviado humano debe navegar la política de un planeta helado habitado por seres andróginos en busca de una alianza.", "asin": "6070799895", "portada": "https://m.media-amazon.com/images/I/813AqVVbDLL._SL1500_.jpg"},
            {"titulo": "Yo, Robot", "autor_index": 38, "genero": "Ciencia Ficción", "descripcion": "Historias interconectadas exploran las Tres Leyes de la Robótica y las complejas relaciones entre humanos y máquinas inteligentes.", "asin": "8435021343", "portada": "https://m.media-amazon.com/images/I/71x-U3x5N2L._SL1500_.jpg"},
            {"titulo": "Solaris", "autor_index": 45, "genero": "Ciencia Ficción", "descripcion": "Científicos en una estación espacial estudian un océano viviente que materializa sus memorias más dolorosas y profundas.", "asin": "8445076825", "portada": "https://m.media-amazon.com/images/I/61DC0GVd5LL._SL1181_.jpg"},
            {"titulo": "La Guerra de los Mundos", "autor_index": 46, "genero": "Ciencia Ficción", "descripcion": "Marcianos invaden la Tierra con tecnología superior, pero encuentran un enemigo inesperado en este clásico pionero del género.", "asin": "B0FYNJJ483", "portada": "https://m.media-amazon.com/images/I/71xBSZ9qKTL._SL1500_.jpg"},
            {"titulo": "La Máquina del Tiempo", "autor_index": 46, "genero": "Ciencia Ficción", "descripcion": "Un científico victoriano viaja al año 802,701 y descubre la evolución divergente de la humanidad en dos especies distintas.", "asin": "B0C8R9FN3Q", "portada": "https://m.media-amazon.com/images/I/6137--avcwL._SL1491_.jpg"},
            {"titulo": "Ubik", "autor_index": 47, "genero": "Ciencia Ficción", "descripcion": "Tras un ataque, empleados de una corporación descubren que la realidad se desmorona y retrocede en el tiempo constantemente.", "asin": "8445007378", "portada": "https://m.media-amazon.com/images/I/81IQrIAEIKL._SL1500_.jpg"},
            {"titulo": "Hyperion", "autor_index": 48, "genero": "Ciencia Ficción", "descripcion": "Siete peregrinos viajan a un planeta remoto, cada uno narrando su historia al estilo de los Cuentos de Canterbury futuristas.", "asin": "8466658033", "portada": "https://m.media-amazon.com/images/I/91uTbqdHpnL._SL1500_.jpg"},
            {"titulo": "El Fin de la Eternidad", "autor_index": 38, "genero": "Ciencia Ficción", "descripcion": "Los Eternos manipulan el tiempo para mejorar la humanidad, hasta que un técnico se enamora y cambia todo el destino humano.", "asin": "8491425756", "portada": "https://m.media-amazon.com/images/I/51hbfoLqqhL._SL1050_.jpg"},
            {"titulo": "La Guerra Interminable", "autor_index": 49, "genero": "Ciencia Ficción", "descripcion": "Soldados luchan en una guerra espacial de siglos debido a la dilatación temporal, regresando a una Tierra irreconocible.", "asin": "8490709262", "portada": "https://m.media-amazon.com/images/I/81qGZgzUsuL._SL1500_.jpg"},
            {"titulo": "Contacto", "autor_index": 31, "genero": "Ciencia Ficción", "descripcion": "Una astrónoma recibe una señal extraterrestre que contiene planos para una máquina capaz de contactar con sus creadores.", "asin": "6073166443", "portada": "https://m.media-amazon.com/images/I/71x0CMouHZL._SL1500_.jpg"},
            {"titulo": "Carbono Modificado", "autor_index": 50, "genero": "Ciencia Ficción", "descripcion": "En un futuro donde la conciencia se transfiere entre cuerpos, un ex soldado investiga el asesinato de un hombre rico.", "asin": "8417507477", "portada": "https://m.media-amazon.com/images/I/71Ar10opdgL._SL1500_.jpg"},
            {"titulo": "Matadero Cinco", "autor_index": 51, "genero": "Ciencia Ficción", "descripcion": "Billy Pilgrim viaja en el tiempo sin control, viviendo momentos de su vida, incluyendo el bombardeo de Dresde aleatoriamente.", "asin": "B0BZZ23KMY", "portada": "https://m.media-amazon.com/images/I/81-W5SUCRjL._SL1500_.jpg"},
            {"titulo": "El Despertar del Leviatán", "autor_index": 52, "genero": "Ciencia Ficción", "descripcion": "Un detective y un capitán descubren una conspiración que amenaza la frágil paz entre la Tierra, Marte y el Cinturón.", "asin": "8466660151", "portada": "https://m.media-amazon.com/images/I/810CU9+IGiL._SL1500_.jpg"},
            
            # FICCIÓN (20 books)
            {"titulo": "El Gran Gatsby", "autor_index": 53, "genero": "Ficción", "descripcion": "Jay Gatsby persigue su sueño americano y un amor perdido en el glamuroso y corrupto mundo de Nueva York en los años veinte.", "asin": "8466350969", "portada": "https://m.media-amazon.com/images/I/912jMzwrRQL._SL1500_.jpg"},
            {"titulo": "Matar a un Ruiseñor", "autor_index": 54, "genero": "Ficción", "descripcion": "Scout Finch narra la defensa de su padre de un hombre negro acusado injustamente en el sur de Estados Unidos durante la Depresión.", "asin": "0718076370", "portada": "https://m.media-amazon.com/images/I/81+j6JIEweL._SL1500_.jpg"},
            {"titulo": "El Guardián entre el Centeno", "autor_index": 55, "genero": "Ficción", "descripcion": "Holden Caulfield vaga por Nueva York tras ser expulsado de su escuela, criticando la hipocresía del mundo adulto.", "asin": "8420674206", "portada": "https://m.media-amazon.com/images/I/61fwcnFmmpL._SL1080_.jpg"},
            {"titulo": "El Señor de los Anillos: La Comunidad del Anillo", "autor_index": 55, "genero": "Ficción", "descripcion": "Frodo Bolsón inicia una peligrosa misión para destruir un anillo mágico que amenaza con sumir la Tierra Media en la oscuridad.", "asin": "6070792238", "portada": "https://m.media-amazon.com/images/I/81LYyyLeR5L._SL1500_.jpg"},
            {"titulo": "El Código Da Vinci", "autor_index": 57, "genero": "Ficción", "descripcion": "Robert Langdon descifra símbolos antiguos en una carrera contrarreloj para resolver un misterio que sacudiría los cimientos del cristianismo.", "asin": "8408163159", "portada": "https://m.media-amazon.com/images/I/71cmxCYAntL._SL1003_.jpg"},
            {"titulo": "Los Juegos del Hambre", "autor_index": 58, "genero": "Ficción", "descripcion": "Katniss Everdeen se ofrece como tributo para competir en un brutal reality show donde solo uno de 24 jóvenes sobrevivirá.", "asin": "6073807848", "portada": "https://m.media-amazon.com/images/I/71N9ipxBq-L._SL1500_.jpg"},
            {"titulo": "La Sombra del Viento", "autor_index": 59, "genero": "Ficción", "descripcion": "En la Barcelona de posguerra, Daniel descubre un libro misterioso que lo lleva a desentrañar secretos oscuros del pasado.", "asin": "8408299751", "portada": "https://m.media-amazon.com/images/I/61nVH-yc7-L._SL1050_.jpg"},
            {"titulo": "Harry Potter y la Piedra Filosofal", "autor_index": 60, "genero": "Ficción", "descripcion": "Harry Potter descubre que es un mago y comienza su educación en Hogwarts, donde enfrenta misterios y magia oscura.", "asin": "8478884459", "portada": "https://m.media-amazon.com/images/I/61mEUsasD-L._SL1036_.jpg"},
            {"titulo": "Cumbres Borrascosas", "autor_index": 61, "genero": "Ficción", "descripcion": "La pasión destructiva entre Heathcliff y Catherine se desarrolla en los páramos ingleses en esta oscura historia gótica.", "asin": "8415618891", "portada": "https://m.media-amazon.com/images/I/71z0fG-3LSL._SL1000_.jpg"},
            {"titulo": "El Retrato de Dorian Gray", "autor_index": 62, "genero": "Ficción", "descripcion": "Un joven aristocrata mantiene su belleza mientras su retrato envejece, reflejando la corrupción de su alma hedonista.", "asin": "B0CLJDQB8C", "portada": "https://m.media-amazon.com/images/I/61UA2Ke-HZL._SL1491_.jpg"},
            {"titulo": "Crónica de una Muerte Anunciada", "autor_index": 68, "genero": "Ficción", "descripcion": "Un pueblo entero conoce el inminente asesinato de Santiago Nasar, pero nadie lo previene en este thriller magistral.", "asin": "1400034957", "portada": "https://m.media-amazon.com/images/I/818cJE+RAzL._SL1500_.jpg"},
            {"titulo": "El Cuento de la Criada", "autor_index": 64, "genero": "Ficción", "descripcion": "En una teocracia totalitaria, las mujeres fértiles son forzadas a ser reproductoras en esta distopía feminista inquietante.", "asin": "8498389070", "portada": "https://m.media-amazon.com/images/I/51pmeQKvt4S._SL1500_.jpg"},
            {"titulo": "El Perfume", "autor_index": 65, "genero": "Ficción", "descripcion": "Un genio olfativo sin olor corporal propio obsesionado con crear el perfume perfecto comete asesinatos en la Francia del siglo XVIII.", "asin": "8432225363", "portada": "https://m.media-amazon.com/images/I/91xy8I69j7L._SL1500_.jpg"},
            {"titulo": "El Nombre del Viento", "autor_index": 66, "genero": "Ficción", "descripcion": "Kvothe narra su transformación de niño prodigio a legendario mago y músico en esta épica fantasía contemporánea.", "asin": "8466354026", "portada": "https://m.media-amazon.com/images/I/81Zw8b8QbGL._SL1500_.jpg"},
            {"titulo": "Beloved", "autor_index": 67, "genero": "Ficción", "descripcion": "Una ex esclava es perseguida por el fantasma de su hija muerta en esta poderosa novela sobre el trauma de la esclavitud.", "asin": "8426409377", "portada": "https://m.media-amazon.com/images/I/71A1I-xIAHL._SL1500_.jpg"},
            {"titulo": "El Amor en los Tiempos del Cólera", "autor_index": 68, "genero": "Ficción", "descripcion": "Florentino Ariza espera más de cincuenta años para conquistar a Fermina Daza en esta historia de amor inquebrantable.", "asin": "8439728352", "portada": "https://m.media-amazon.com/images/I/71oUUqtpMiL._SL1500_.jpg"},
            {"titulo": "Las Aventuras de Huckleberry Finn", "autor_index": 13, "genero": "Ficción", "descripcion": "Huck huye por el Mississippi con Jim, un esclavo fugitivo, en esta sátira sobre racismo y libertad en Estados Unidos.", "asin": "8420433934", "portada": "https://m.media-amazon.com/images/I/914RVTaJWGL._SL1500_.jpg"},
            
            # LATINOAMERICANOS (20 books)
            {"titulo": "Cien Años de Soledad", "autor_index": 68, "genero": "Latinoamericano", "descripcion": "La saga de la familia Buendía en el pueblo mítico de Macondo, obra cumbre del realismo mágico latinoamericano.", "asin": "0307474720", "portada": "https://m.media-amazon.com/images/I/81n2i30X+5L._SL1500_.jpg"},
            {"titulo": "La Casa de los Espíritus", "autor_index": 69, "genero": "Latinoamericano", "descripcion": "Tres generaciones de mujeres de la familia Trueba navegan amor, política y poderes sobrenaturales en Chile.", "asin": "0525433473", "portada": "https://m.media-amazon.com/images/I/81sf9LHQcML._SL1500_.jpg"},
            {"titulo": "Rayuela", "autor_index": 70, "genero": "Latinoamericano", "descripcion": "Una novela experimental que puede leerse en múltiples órdenes, explorando el amor y la búsqueda existencial.", "asin": "8437624746", "portada": "https://m.media-amazon.com/images/I/51lnhKqPnQL._SL1050_.jpg"},
            {"titulo": "Pedro Páramo", "autor_index": 71, "genero": "Latinoamericano", "descripcion": "Juan Preciado busca a su padre en Comala, un pueblo habitado por fantasmas y voces del pasado mexicano.", "asin": "080216093X", "portada": "https://m.media-amazon.com/images/I/81IfreXInWL._SL1500_.jpg"},
            {"titulo": "La Ciudad y los Perros", "autor_index": 72, "genero": "Latinoamericano", "descripcion": "Cadetes de un colegio militar en Lima enfrentan violencia, código de honor y corrupción en la sociedad peruana.", "asin": "8420454052", "portada": "https://m.media-amazon.com/images/I/81u8RSD9R7L._SL1500_.jpg"},
            {"titulo": "El Túnel", "autor_index": 73, "genero": "Latinoamericano", "descripcion": "Un pintor obsesionado narra desde prisión el asesinato de la única mujer que comprendió su arte en Buenos Aires.", "asin": "6070784057", "portada": "https://m.media-amazon.com/images/I/715wzJ+wgxL._SL1500_.jpg"},
            {"titulo": "Como Agua para Chocolate", "autor_index": 74, "genero": "Latinoamericano", "descripcion": "Tita expresa emociones prohibidas a través de la cocina, mezclando recetas con realismo mágico en la Revolución Mexicana.", "asin": "0385721234", "portada": "https://m.media-amazon.com/images/I/71ANghTe2rL._SL1200_.jpg"},
            {"titulo": "El Aleph", "autor_index": 75, "genero": "Latinoamericano", "descripcion": "Colección de cuentos metafísicos donde Borges explora infinitos, laberintos y los límites de la realidad y el tiempo.", "asin": "846634683X", "portada": "https://m.media-amazon.com/images/I/81jFjE9rt6L._SL1500_.jpg"},
            {"titulo": "La Fiesta del Chivo", "autor_index": 72, "genero": "Latinoamericano", "descripcion": "La dictadura de Trujillo en República Dominicana vista a través del retorno de una mujer y el asesinato del tirano.", "asin": "8420434647", "portada": "https://m.media-amazon.com/images/I/71lRLtiOAGL._SL1050_.jpg"},
            {"titulo": "Los Detectives Salvajes", "autor_index": 76, "genero": "Latinoamericano", "descripcion": "Jóvenes poetas buscan a una escritora desaparecida en México, explorando la bohemia literaria de los años setenta.", "asin": "8420423939", "portada": "https://m.media-amazon.com/images/I/612e-xhmW9L._SL1050_.jpg"},
            {"titulo": "La Tregua", "autor_index": 77, "genero": "Latinoamericano", "descripcion": "Un viudo montevideano próximo a jubilarse inicia un romance inesperado que transforma sus últimos días de trabajo.", "asin": "8420666882", "portada": "https://m.media-amazon.com/images/I/81QNsNgszYL._SL1500_.jpg"},
            {"titulo": "Aura", "autor_index": 78, "genero": "Latinoamericano", "descripcion": "Un joven historiador acepta un trabajo en una mansión misteriosa y queda atrapado en un hechizo entre dos mujeres.", "asin": "6074451842", "portada": "https://m.media-amazon.com/images/I/91omNHYaPIL._SL1500_.jpg"},
            {"titulo": "La Vorágine", "autor_index": 79, "genero": "Latinoamericano", "descripcion": "Arturo Cova huye con su amante a la selva colombiana donde descubre los horrores de la explotación cauchera amazónica.", "asin": "B006KVKRS8", "portada": "https://m.media-amazon.com/images/I/81tcoRbOtWL._SL1500_.jpg"},
            {"titulo": "El Reino de Este Mundo", "autor_index": 80, "genero": "Latinoamericano", "descripcion": "La revolución haitiana contada a través de Ti Noel, un esclavo que presencia la transformación mágica de su nación.", "asin": "1490981578", "portada": "https://m.media-amazon.com/images/I/71wowhjgMdL._SL1000_.jpg"},
            {"titulo": "Ficciones", "autor_index": 75, "genero": "Latinoamericano", "descripcion": "Colección de cuentos que exploran laberintos, bibliotecas infinitas y realidades alternativas en prosa filosófica brillante.", "asin": "0307950921", "portada": "https://m.media-amazon.com/images/I/61aCU68SLIL._SL1200_.jpg"},
            {"titulo": "La Muerte de Artemio Cruz", "autor_index": 78, "genero": "Latinoamericano", "descripcion": "Un magnate mexicano moribundo recuerda su vida en flashbacks que revelan la corrupción de la Revolución Mexicana.", "asin": "8402070019", "portada": "https://m.media-amazon.com/images/I/61n3mWTfq5L._SL1055_.jpg"},
            {"titulo": "El Beso de la Mujer Araña", "autor_index": 81, "genero": "Latinoamericano", "descripcion": "Dos prisioneros en Argentina desarrollan una amistad inesperada mientras uno narra películas al otro en su celda.", "asin": "B09Z636T3Z", "portada": "https://m.media-amazon.com/images/I/71ZhkXEBl5L._SL1500_.jpg"},
            {"titulo": "Pantaleón y las Visitadoras", "autor_index": 72, "genero": "Latinoamericano", "descripcion": "Un capitán del ejército peruano recibe la misión de organizar un servicio de prostitutas para las tropas en la Amazonía.", "asin": "B01C7T5EM0", "portada": "https://m.media-amazon.com/images/I/710U24aBizL._SL1500_.jpg"},
            {"titulo": "Santa Evita", "autor_index": 82, "genero": "Latinoamericano", "descripcion": "La historia del cadáver embalsamado de Eva Perón y su extraño viaje por Argentina tras la caída de su esposo.", "asin": "0679768149", "portada": "https://m.media-amazon.com/images/I/71S2BTUOJXL._SL1176_.jpg"},
            {"titulo": "El Otoño del Patriarca", "autor_index": 68, "genero": "Latinoamericano", "descripcion": "El retrato de un dictador latinoamericano anciano y su decadencia, narrado en largos pasajes de prosa poética hipnótica.", "asin": "B00SNOFVQI", "portada": "https://m.media-amazon.com/images/I/71ebmlnzRRL._SL1500_.jpg"},
            
            # HISTORIA (20 books)
            {"titulo": "Los Pilares de la Tierra", "autor_index": 63, "genero": "Historia", "descripcion": "La construcción de una catedral gótica en la Inglaterra medieval sirve de telón para intrigas, ambiciones y luchas de poder.", "asin": "8401328519", "portada": "https://m.media-amazon.com/images/I/51SwGPdq3HL.jpg"},
            {"titulo": "El Nombre de la Rosa", "autor_index": 83, "genero": "Historia", "descripcion": "Un fraile franciscano investiga misteriosos asesinatos en una abadía italiana del siglo XIV llena de secretos y herejías.", "asin": "8426403565", "portada": "https://m.media-amazon.com/images/I/816Z+coEZ8L._SL1500_.jpg"},
            {"titulo": "Todos Deberíamos Ser Feministas", "autor_index": 84, "genero": "Historia", "descripcion": "Un ensayo personal que examina la historia y el significado del feminismo en el contexto africano y global contemporáneo.", "asin": "8439730489", "portada": "https://m.media-amazon.com/images/I/71mEPWrODwL._SL1500_.jpg"},
            {"titulo": "El Mundo de Ayer", "autor_index": 85, "genero": "Historia", "descripcion": "Memorias del escritor austriaco sobre la Europa culta anterior a las guerras mundiales y su destrucción por el totalitarismo.", "asin": "B09S68C8WZ", "portada": "https://m.media-amazon.com/images/I/61f6TsIQuvL._SL1491_.jpg"},
            {"titulo": "Los Miserables", "autor_index": 86, "genero": "Historia", "descripcion": "Jean Valjean busca redención en la Francia del siglo XIX, en una épica historia sobre justicia, amor y revolución social.", "asin": "B0CFZFJYKS", "portada": "https://m.media-amazon.com/images/I/71aLbjCBRnL._SL1500_.jpg"},
            {"titulo": "Memorias de Adriano", "autor_index": 88, "genero": "Historia", "descripcion": "El emperador romano Adriano reflexiona sobre su vida, amor por Antínoo y el poder en esta ficción histórica íntima.", "asin": "6073103220", "portada": "https://m.media-amazon.com/images/I/61nfQ-br8QL._SL1291_.jpg"},
            {"titulo": "Yo, Claudio", "autor_index": 90, "genero": "Historia", "descripcion": "Las memorias ficticias del emperador romano Claudio sobre las intrigas, asesinatos y locuras de la dinastía Julio-Claudia.", "asin": "8435005208", "portada": "https://m.media-amazon.com/images/I/91C2BIrY2pL._SL1500_.jpg"},
            {"titulo": "La Conjura de los Necios", "autor_index": 89, "genero": "Historia", "descripcion": "Ignatius J. Reilly, un intelectual medieval atrapado en la Nueva Orleans moderna, causa caos cómico por donde pasa.", "asin": "8433902326", "portada": "https://m.media-amazon.com/images/I/81FZYxOWkrL._SL1500_.jpg"},
            {"titulo": "El Médico", "autor_index": 90, "genero": "Historia", "descripcion": "Un joven inglés del siglo XI viaja a Persia haciéndose pasar por judío para estudiar medicina con Avicena.", "asin": "8415729251", "portada": "https://m.media-amazon.com/images/I/71zuAgyG9TL._SY342_.jpg"},
            {"titulo": "Shogun", "autor_index": 91, "genero": "Historia", "descripcion": "Un navegante inglés náufrago en Japón feudal se ve envuelto en luchas de poder entre señores de la guerra samurái.", "asin": "8466379703", "portada": "https://m.media-amazon.com/images/I/61b5n6pgSnL._SL1050_.jpg"},
            {"titulo": "El Último Mohicano", "autor_index": 92, "genero": "Historia", "descripcion": "Durante la Guerra Franco-India, Hawkeye y sus aliados mohicanos escoltan a dos hermanas en territorio peligroso.", "asin": "B07FMZ4ZJS", "portada": "https://m.media-amazon.com/images/I/81STy77GacS._SL1500_.jpg"},
            {"titulo": "La Catedral del Mar", "autor_index": 93, "genero": "Historia", "descripcion": "Un siervo medieval lucha por su libertad mientras ayuda a construir la iglesia de Santa María del Mar en Barcelona.", "asin": "8425367786", "portada": "https://m.media-amazon.com/images/I/81jRChIWkPL._SL1500_.jpg"},
            {"titulo": "El Hereje", "autor_index": 94, "genero": "Historia", "descripcion": "Cipriano Salcedo, comerciante del siglo XVI en Valladolid, abraza el protestantismo enfrentando la Inquisición española.", "asin": "8423363880", "portada": "https://m.media-amazon.com/images/I/61+1rlrijML._SL1050_.jpg"},
            {"titulo": "La Reina del Sur", "autor_index": 95, "genero": "Historia", "descripcion": "Teresa Mendoza pasa de ser novia de un narcotraficante a convertirse en una poderosa líder del contrabando internacional.", "asin": "1589866177", "portada": "https://m.media-amazon.com/images/I/51RqZIe9wqL.jpg"},
        ]
        
        print(f"   Total de libros a crear: {len(libros_data)}")
        
        libros = []
        for libro_data in libros_data:
            libro = Book(
                titulo_libro=libro_data["titulo"],
                id_autor=autores[libro_data["autor_index"]].id_autor,
                genero_libro=libro_data["genero"],
                descripcion_libros=libro_data["descripcion"],
                enlace_asin_libro=libro_data["asin"],
                enlace_portada_libro=libro_data["portada"]
            )
            db.session.add(libro)
            libros.append(libro)
        
        db.session.commit()
        print(f"✓ {len(libros)} libros creados")
        
        # Crear usuarios de prueba
        print("👤 Creando usuarios de prueba...")
        usuarios_data = [
            {"nombre": "Juan", "apellido": "Pérez", "email": "juan@test.com", "password": "password123"},
            {"nombre": "María", "apellido": "González", "email": "maria@test.com", "password": "password123"},
            {"nombre": "Carlos", "apellido": "Rodríguez", "email": "carlos@test.com", "password": "password123"},
            {"nombre": "Ana", "apellido": "Martínez", "email": "ana@test.com", "password": "password123"},
            {"nombre": "Luis", "apellido": "López", "email": "luis@test.com", "password": "password123"},
        ]
        
        usuarios = []
        for usuario_data in usuarios_data:
            usuario = User(
                nombre_usuario=usuario_data["nombre"],
                apellido_usuario=usuario_data["apellido"],
                email_usuario=usuario_data["email"],
                password_usuario=usuario_data["password"]
            )
            db.session.add(usuario)
            usuarios.append(usuario)
        
        db.session.commit()
        print(f"✓ {len(usuarios)} usuarios creados")
        
        # Crear bibliotecas de usuarios y calificaciones (SIN OVERLAP)
        print("📖 Creando bibliotecas de usuarios y calificaciones...")
        estados_validos = ['quiero_leer', 'leyendo']
        reseñas_ejemplo = [
            "Excelente libro, muy recomendado.",
            "Una obra maestra de la literatura.",
            "Interesante pero un poco largo.",
            "Me encantó, lo leería de nuevo.",
            "Buen desarrollo de personajes.",
            "Lectura obligatoria para todos.",
            "No es mi género favorito pero está bien.",
            "Muy bien escrito y emocionante.",
            "Clásico que todos deberían leer.",
            "Me sorprendió gratamente."
        ]
        
        for usuario in usuarios:
            # Seleccionar libros aleatorios para este usuario
            total_libros_usuario = random.randint(18, 27)  # Total entre biblioteca + leídos
            libros_usuario = random.sample(libros, total_libros_usuario)
            
            # Dividir: algunos para UserLibrary (quiero_leer/leyendo), otros para Rating (leídos)
            num_en_biblioteca = random.randint(10, 15)
            libros_en_biblioteca = libros_usuario[:num_en_biblioteca]
            libros_leidos = libros_usuario[num_en_biblioteca:]  # Los restantes son leídos
            
            # Crear entradas en UserLibrary (quiero_leer/leyendo)
            for libro in libros_en_biblioteca:
                biblioteca = UserLibrary(
                    id_libro=libro.id_libros,
                    id_usuario=usuario.id_usuario,
                    estado_lectura=random.choice(estados_validos)
                )
                db.session.add(biblioteca)
            
            # Crear entradas en Rating (leídos)
            for libro in libros_leidos:
                # Calificación puede ser None (solo marcado como leído) o 1-5
                calificacion_valor = random.choice([None, None, random.randint(3, 5)])
                # Reseña es opcional
                resena_valor = random.choice(reseñas_ejemplo) if random.random() > 0.5 else None
                
                calificacion = Rating(
                    id_libro=libro.id_libros,
                    id_usuario=usuario.id_usuario,
                    calificacion=calificacion_valor,
                    resena=resena_valor
                )
                db.session.add(calificacion)
        
        db.session.commit()
        print("✓ Bibliotecas de usuarios creadas (quiero_leer/leyendo)")
        print("✓ Calificaciones creadas (leídos - sin overlap)")
        
        print("\n🎉 Base de datos poblada con libros REALES!")
        print(f"   - {Admin.query.count()} administradores")
        print(f"   - {len(autores)} autores famosos")
        print(f"   - {len(libros)} libros clásicos y contemporáneos") 
        print(f"   - {len(usuarios)} usuarios de prueba")
        print(f"   - {Rating.query.count()} calificaciones (libros leídos)")
        print(f"   - {UserLibrary.query.count()} elementos en bibliotecas (quiero_leer/leyendo)")
        print("\n📚 Distribución por géneros:")
        generos_count = db.session.query(Book.genero_libro, db.func.count(Book.id_libros)).group_by(Book.genero_libro).all()
        for genero, count in generos_count:
            print(f"   - {genero}: {count} libros")

if __name__ == '__main__':
    seed_database()