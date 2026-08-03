from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class VocabularyItem:
    id: str
    german: str
    spanish: str
    pronunciation: str
    example_de: str
    example_es: str
    tip: str = ""


@dataclass(frozen=True)
class ReadingQuestion:
    prompt: str
    options: tuple[str, str, str, str]
    answer: str
    explanation: str


@dataclass(frozen=True)
class Lesson:
    id: str
    category: str
    title_de: str
    title_es: str
    level: str
    minutes: int
    paragraphs: tuple[str, ...]
    spanish_help: tuple[str, ...]
    grammar_note: str
    vocabulary: tuple[VocabularyItem, ...]
    questions: tuple[ReadingQuestion, ...]


def V(
    item_id: str,
    german: str,
    spanish: str,
    pronunciation: str,
    example_de: str,
    example_es: str,
    tip: str = "",
) -> VocabularyItem:
    return VocabularyItem(item_id, german, spanish, pronunciation, example_de, example_es, tip)


def Q(
    prompt: str,
    options: Iterable[str],
    answer: str,
    explanation: str,
) -> ReadingQuestion:
    values = tuple(options)
    if len(values) != 4:
        raise ValueError("Cada pregunta debe tener exactamente cuatro alternativas.")
    return ReadingQuestion(prompt, values, answer, explanation)


LESSONS: tuple[Lesson, ...] = (
    Lesson(
        id="begrussung",
        category="Conversación",
        title_de="Hallo! Ich bin Lula",
        title_es="Saludos y presentación",
        level="A1",
        minutes=12,
        paragraphs=(
            "Lula ist neu in einem Deutschkurs. Am Morgen kommt sie in das Klassenzimmer. Sie sagt: „Guten Morgen! Ich heiße Lula. Ich komme aus Chile.“",
            "Ein Schüler heißt Jonas. Er sagt: „Hallo Lula! Ich wohne in Berlin. Wie geht es dir?“ Lula antwortet: „Danke, gut. Und dir?“",
            "Die Lehrerin heißt Frau Weber. Am Ende sagt Lula: „Auf Wiedersehen, Frau Weber!“",
        ),
        spanish_help=(
            "Lula es nueva en un curso de alemán y se presenta al entrar a la sala.",
            "Jonas vive en Berlín y le pregunta cómo está. Lula responde que está bien.",
            "Al terminar, Lula se despide de la profesora Weber.",
        ),
        grammar_note="En alemán, «ich heiße…» significa «me llamo…». Para decir de dónde vienes, usa «ich komme aus…».",
        vocabulary=(
            V("hallo", "Hallo", "hola", "já-lo", "Hallo, Mia!", "¡Hola, Mia!"),
            V("guten_morgen", "Guten Morgen", "buenos días", "gú-ten mór-guen", "Guten Morgen, Frau Weber.", "Buenos días, señora Weber."),
            V("heissen", "heißen", "llamarse", "jái-sen", "Ich heiße Lula.", "Me llamo Lula.", "La letra ß suena como una s fuerte."),
            V("kommen", "kommen", "venir", "kó-men", "Ich komme aus Chile.", "Vengo de Chile."),
            V("wohnen", "wohnen", "vivir / residir", "vó-nen", "Ich wohne in Santiago.", "Vivo en Santiago."),
            V("wie_gehts", "Wie geht es dir?", "¿cómo estás?", "ví guet es dír", "Hallo! Wie geht es dir?", "¡Hola! ¿Cómo estás?"),
            V("danke", "Danke", "gracias", "dán-ke", "Danke, gut.", "Gracias, bien."),
            V("gut", "gut", "bien / bueno", "guut", "Mir geht es gut.", "Estoy bien."),
            V("und", "und", "y", "unt", "Und dir?", "¿Y tú?"),
            V("auf_wiedersehen", "Auf Wiedersehen", "hasta luego", "auf ví-der-ze-en", "Auf Wiedersehen, Frau Weber!", "¡Hasta luego, señora Weber!"),
        ),
        questions=(
            Q("¿Dónde está Lula?", ("En un curso de alemán", "En una estación", "En un restaurante", "En su casa"), "En un curso de alemán", "Al comienzo se cuenta que Lula acaba de entrar a un curso de alemán."),
            Q("¿A qué hora del día llega Lula?", ("Por la mañana", "Al mediodía", "Por la tarde", "Por la noche"), "Por la mañana", "«Am Morgen» significa «por la mañana»."),
            Q("¿Qué dice Lula al entrar?", ("Guten Morgen", "Gute Nacht", "Tschüss", "Entschuldigung"), "Guten Morgen", "Lula saluda con «Guten Morgen», es decir, «buenos días»."),
            Q("¿De qué país viene Lula?", ("Chile", "Alemania", "España", "Austria"), "Chile", "Lula dice «Ich komme aus Chile»."),
            Q("¿Cómo se llama el estudiante?", ("Jonas", "Weber", "Lukas", "Felix"), "Jonas", "El compañero se llama Jonas."),
            Q("¿Dónde vive Jonas?", ("En Berlín", "En Hamburgo", "En Santiago", "En Viena"), "En Berlín", "Jonas dice «Ich wohne in Berlin»."),
            Q("¿Qué le pregunta Jonas a Lula?", ("Cómo está", "Qué edad tiene", "Qué estudia", "Dónde trabaja"), "Cómo está", "«Wie geht es dir?» significa «¿cómo estás?»."),
            Q("¿Cómo está Lula?", ("Bien", "Cansada", "Enferma", "Enojada"), "Bien", "Lula responde «Danke, gut»."),
            Q("¿Quién es Frau Weber?", ("La profesora", "La hermana de Lula", "Una médica", "Una vecina"), "La profesora", "El texto la presenta como «die Lehrerin», la profesora."),
            Q("¿Qué hace Lula al final?", ("Se despide", "Pide comida", "Sale a correr", "Llama por teléfono"), "Se despide", "Dice «Auf Wiedersehen», una despedida formal."),
        ),
    ),
    Lesson(
        id="alltag",
        category="Vida diaria",
        title_de="Ein normaler Morgen",
        title_es="Una mañana normal",
        level="A1",
        minutes=12,
        paragraphs=(
            "Lula steht um sieben Uhr auf. Sie öffnet das Fenster und trinkt ein Glas Wasser. Danach macht sie das Bett.",
            "Um halb acht frühstückt sie. Sie isst Brot mit Käse und trinkt Tee. Dann putzt sie die Zähne und zieht eine Jacke an.",
            "Um acht Uhr verlässt Lula das Haus. Der Bus kommt um acht Uhr zehn. Heute ist sie pünktlich.",
        ),
        spanish_help=(
            "Lula se levanta a las siete, abre la ventana, toma agua y hace la cama.",
            "A las siete y media desayuna pan con queso y té. Después se lava los dientes y se pone una chaqueta.",
            "Sale de la casa a las ocho y toma un bus diez minutos después. Llega a tiempo.",
        ),
        grammar_note="Los verbos separables se dividen: «aufstehen» se convierte en «Lula steht … auf». No necesitas dominarlo todavía; reconoce las dos partes.",
        vocabulary=(
            V("aufstehen", "aufstehen", "levantarse", "áuf-shte-en", "Ich stehe um sieben Uhr auf.", "Me levanto a las siete."),
            V("fenster", "das Fenster", "la ventana", "das féns-ter", "Das Fenster ist offen.", "La ventana está abierta."),
            V("wasser", "das Wasser", "el agua", "das vá-ser", "Ich trinke Wasser.", "Tomo agua."),
            V("bett", "das Bett", "la cama", "das bet", "Ich mache das Bett.", "Hago la cama."),
            V("fruhstucken", "frühstücken", "desayunar", "frú-shtü-ken", "Wir frühstücken um acht.", "Desayunamos a las ocho."),
            V("brot", "das Brot", "el pan", "das brot", "Ich esse Brot.", "Como pan."),
            V("kase", "der Käse", "el queso", "der ké-se", "Das Brot ist mit Käse.", "El pan es con queso."),
            V("zahne", "die Zähne", "los dientes", "di tsé-ne", "Ich putze die Zähne.", "Me lavo los dientes."),
            V("jacke", "die Jacke", "la chaqueta", "di yá-ke", "Die Jacke ist schwarz.", "La chaqueta es negra."),
            V("punktlich", "pünktlich", "puntual", "púnkt-lij", "Heute bin ich pünktlich.", "Hoy soy puntual."),
        ),
        questions=(
            Q("¿A qué hora se levanta Lula?", ("A las siete", "A las seis", "A las ocho", "A las nueve"), "A las siete", "«Um sieben Uhr» significa «a las siete»."),
            Q("¿Qué abre primero?", ("La ventana", "La puerta", "El refrigerador", "Un libro"), "La ventana", "Después de levantarse, abre la ventana."),
            Q("¿Qué bebe antes de desayunar?", ("Agua", "Café", "Leche", "Jugo"), "Agua", "Toma un vaso de agua antes del desayuno."),
            Q("¿Qué hace con la cama?", ("La hace", "La mueve", "La vende", "Se vuelve a dormir"), "La hace", "«Sie macht das Bett» significa que hace la cama."),
            Q("¿A qué hora desayuna?", ("A las siete y media", "A las siete", "A las ocho y media", "A las nueve"), "A las siete y media", "«Um halb acht» equivale a las 7:30 en alemán."),
            Q("¿Qué come?", ("Pan con queso", "Arroz con pollo", "Yogur con fruta", "Solo una manzana"), "Pan con queso", "En el desayuno aparece «Brot mit Käse», que significa «pan con queso»."),
            Q("¿Qué bebida acompaña el desayuno?", ("Té", "Café", "Agua mineral", "Chocolate"), "Té", "Lula bebe té."),
            Q("¿Qué se pone Lula?", ("Una chaqueta", "Un vestido", "Un sombrero", "Un uniforme"), "Una chaqueta", "«Sie zieht eine Jacke an» significa que se pone una chaqueta."),
            Q("¿A qué hora llega el bus?", ("A las 8:10", "A las 7:50", "A las 8:30", "A las 9:10"), "A las 8:10", "El bus llega «um acht Uhr zehn»."),
            Q("¿Lula llega tarde?", ("No, llega puntual", "Sí, llega diez minutos tarde", "No se sabe", "Pierde el bus"), "No, llega puntual", "La última frase dice que hoy está puntual."),
        ),
    ),
    Lesson(
        id="universitat",
        category="Universidad",
        title_de="Ein Tag an der Universität",
        title_es="Un día en la universidad",
        level="A1",
        minutes=13,
        paragraphs=(
            "Lula studiert an einer Universität. Am Montag hat sie zwei Kurse: Deutsch und Mathematik. Der Deutschkurs beginnt um neun Uhr.",
            "In der Pause geht Lula mit ihrer Freundin Ana in die Mensa. Sie essen Suppe und sprechen über die Hausaufgaben.",
            "Am Nachmittag lernt Lula in der Bibliothek. Um fünf Uhr fährt sie nach Hause.",
        ),
        spanish_help=(
            "Lula estudia en una universidad y el lunes tiene Alemán y Matemáticas.",
            "Durante el recreo va al casino universitario con Ana. Comen sopa y hablan de la tarea.",
            "En la tarde estudia en la biblioteca y regresa a casa a las cinco.",
        ),
        grammar_note="«an einer Universität» usa dativo, pero en A1 basta con aprender la expresión completa: «Ich studiere an einer Universität».",
        vocabulary=(
            V("universitat", "die Universität", "la universidad", "di uni-ver-si-tét", "Ich studiere an der Universität.", "Estudio en la universidad."),
            V("kurs", "der Kurs", "el curso / ramo", "der kurs", "Der Kurs beginnt um neun.", "El curso comienza a las nueve."),
            V("montag", "der Montag", "el lunes", "der món-tag", "Am Montag habe ich Deutsch.", "El lunes tengo Alemán."),
            V("beginnen", "beginnen", "comenzar", "be-guí-nen", "Die Klasse beginnt jetzt.", "La clase comienza ahora."),
            V("pause", "die Pause", "la pausa / recreo", "di páu-se", "Wir haben eine Pause.", "Tenemos una pausa."),
            V("mensa", "die Mensa", "el casino universitario", "di mén-sa", "Wir essen in der Mensa.", "Comemos en el casino universitario."),
            V("hausaufgabe", "die Hausaufgabe", "la tarea", "di jáus-auf-ga-be", "Die Hausaufgabe ist leicht.", "La tarea es fácil."),
            V("bibliothek", "die Bibliothek", "la biblioteca", "di bi-blio-ték", "Sie lernt in der Bibliothek.", "Ella estudia en la biblioteca."),
            V("lernen", "lernen", "aprender / estudiar", "lér-nen", "Ich lerne Deutsch.", "Estudio alemán."),
            V("nach_hause", "nach Hause", "a casa", "naj jáu-se", "Ich fahre nach Hause.", "Voy a casa."),
        ),
        questions=(
            Q("¿Qué hace Lula?", ("Estudia en una universidad", "Trabaja en un hotel", "Vive en una biblioteca", "Enseña matemáticas"), "Estudia en una universidad", "La primera frase dice que Lula estudia en una universidad."),
            Q("¿Qué día ocurre la historia?", ("Lunes", "Martes", "Viernes", "Domingo"), "Lunes", "El texto comienza su horario con «Am Montag»."),
            Q("¿Cuántos cursos tiene?", ("Dos", "Uno", "Tres", "Cuatro"), "Dos", "Tiene Alemán y Matemáticas."),
            Q("¿Qué cursos tiene?", ("Alemán y Matemáticas", "Historia y Física", "Inglés y Música", "Economía y Química"), "Alemán y Matemáticas", "Son los dos cursos mencionados."),
            Q("¿A qué hora empieza Alemán?", ("A las nueve", "A las ocho", "A las diez", "A las cinco"), "A las nueve", "«beginnt um neun Uhr» significa que empieza a las nueve."),
            Q("¿Con quién va a la Mensa?", ("Con Ana", "Con Jonas", "Con la profesora", "Sola"), "Con Ana", "Va con su amiga Ana."),
            Q("¿Qué comen?", ("Sopa", "Pan", "Pasta", "Ensalada"), "Sopa", "La frase «Sie essen Suppe» significa que comen sopa."),
            Q("¿De qué hablan?", ("De la tarea", "Del clima", "De un viaje", "De una película"), "De la tarea", "Hablan sobre «die Hausaufgaben»."),
            Q("¿Dónde estudia en la tarde?", ("En la biblioteca", "En la Mensa", "En el bus", "En casa de Ana"), "En la biblioteca", "El texto lo indica directamente."),
            Q("¿A qué hora vuelve a casa?", ("A las cinco", "A las cuatro", "A las seis", "A las siete"), "A las cinco", "«Um fünf Uhr» significa «a las cinco»."),
        ),
    ),
    Lesson(
        id="arbeit",
        category="Trabajo",
        title_de="Der erste Arbeitstag",
        title_es="El primer día de trabajo",
        level="A1",
        minutes=13,
        paragraphs=(
            "Heute ist Lulas erster Tag in einem kleinen Büro. Ihr Chef heißt Herr Klein. Er zeigt ihr den Arbeitsplatz und den Computer.",
            "Lula schreibt eine kurze E-Mail und telefoniert mit einer Kundin. Um zwölf Uhr macht das Team Mittagspause.",
            "Am Nachmittag hat Lula eine Besprechung. Der Arbeitstag endet um vier Uhr. Lula ist müde, aber zufrieden.",
        ),
        spanish_help=(
            "Es el primer día de Lula en una oficina pequeña. Su jefe le muestra su puesto y el computador.",
            "Escribe un correo, habla por teléfono con una clienta y almuerza al mediodía con el equipo.",
            "En la tarde tiene una reunión. Termina a las cuatro, cansada pero satisfecha.",
        ),
        grammar_note="Los sustantivos alemanes comienzan con mayúscula: Büro, Chef, Computer, E-Mail y Besprechung.",
        vocabulary=(
            V("buro", "das Büro", "la oficina", "das bü-ró", "Das Büro ist klein.", "La oficina es pequeña."),
            V("chef", "der Chef", "el jefe", "der shef", "Mein Chef heißt Herr Klein.", "Mi jefe se llama señor Klein."),
            V("arbeitsplatz", "der Arbeitsplatz", "el puesto de trabajo", "der ár-baits-plats", "Das ist mein Arbeitsplatz.", "Este es mi puesto de trabajo."),
            V("computer", "der Computer", "el computador", "der kom-piú-ter", "Der Computer ist neu.", "El computador es nuevo."),
            V("email", "die E-Mail", "el correo electrónico", "di í-meil", "Ich schreibe eine E-Mail.", "Escribo un correo electrónico."),
            V("telefonieren", "telefonieren", "hablar por teléfono", "te-le-fo-ní-ren", "Sie telefoniert mit einer Kundin.", "Ella habla por teléfono con una clienta."),
            V("kundin", "die Kundin", "la clienta", "di kún-din", "Die Kundin hat eine Frage.", "La clienta tiene una pregunta."),
            V("mittagspause", "die Mittagspause", "la pausa de almuerzo", "di mí-tags-páu-se", "Um zwölf ist Mittagspause.", "A las doce es la pausa de almuerzo."),
            V("besprechung", "die Besprechung", "la reunión", "di be-shpré-jung", "Wir haben eine Besprechung.", "Tenemos una reunión."),
            V("zufrieden", "zufrieden", "satisfecha/o", "tsu-frí-den", "Lula ist zufrieden.", "Lula está satisfecha."),
        ),
        questions=(
            Q("¿Qué día es para Lula?", ("Su primer día de trabajo", "Su último día de clases", "Su cumpleaños", "Un día de vacaciones"), "Su primer día de trabajo", "«Erster Tag» significa «primer día», y la escena ocurre en la oficina."),
            Q("¿Dónde trabaja?", ("En una oficina pequeña", "En una escuela", "En un hospital", "En una tienda"), "En una oficina pequeña", "Trabaja en «einem kleinen Büro»."),
            Q("¿Cómo se llama su jefe?", ("Herr Klein", "Herr Weber", "Herr Jonas", "Herr Schmidt"), "Herr Klein", "El jefe se llama Herr Klein."),
            Q("¿Qué le muestra el jefe?", ("El puesto y el computador", "La cocina y el auto", "La biblioteca y el bus", "El uniforme y el teléfono"), "El puesto y el computador", "Le muestra «den Arbeitsplatz und den Computer»."),
            Q("¿Qué escribe Lula?", ("Un correo breve", "Una carta larga", "Un libro", "Una tarea"), "Un correo breve", "Escribe «eine kurze E-Mail»."),
            Q("¿Con quién habla por teléfono?", ("Con una clienta", "Con Ana", "Con su profesora", "Con su madre"), "Con una clienta", "El texto usa «mit einer Kundin»."),
            Q("¿A qué hora almuerza el equipo?", ("A las doce", "A las once", "A la una", "A las dos"), "A las doce", "La pausa es «um zwölf Uhr»."),
            Q("¿Qué tiene en la tarde?", ("Una reunión", "Un examen", "Una cita médica", "Una clase de alemán"), "Una reunión", "Tiene «eine Besprechung»."),
            Q("¿A qué hora termina?", ("A las cuatro", "A las tres", "A las cinco", "A las seis"), "A las cuatro", "El día laboral termina a las cuatro."),
            Q("¿Cómo se siente al final?", ("Cansada pero satisfecha", "Enojada y enferma", "Aburrida y triste", "Con mucha energía"), "Cansada pero satisfecha", "La frase final es «müde, aber zufrieden»."),
        ),
    ),
    Lesson(
        id="reisen",
        category="Viajes",
        title_de="Am Bahnhof",
        title_es="En la estación de tren",
        level="A1",
        minutes=12,
        paragraphs=(
            "Lula möchte nach Hamburg fahren. Am Bahnhof kauft sie eine Fahrkarte. Der Zug fährt um zehn Uhr von Gleis drei ab.",
            "Lula hat einen kleinen Koffer und einen Rucksack. Sie sucht Gleis drei und fragt einen Mitarbeiter: „Entschuldigung, wo ist Gleis drei?“",
            "Der Mitarbeiter zeigt nach links. Lula findet den Zug und steigt ein. Sie sitzt am Fenster.",
        ),
        spanish_help=(
            "Lula quiere viajar a Hamburgo. Compra un pasaje y su tren sale a las diez desde el andén tres.",
            "Lleva una maleta pequeña y una mochila. Le pregunta a un trabajador dónde está el andén.",
            "El trabajador señala a la izquierda. Lula encuentra el tren, sube y se sienta junto a la ventana.",
        ),
        grammar_note="Para preguntar ubicación, usa «Wo ist…?» (¿Dónde está…?). Para pedir ayuda con cortesía, comienza con «Entschuldigung».",
        vocabulary=(
            V("bahnhof", "der Bahnhof", "la estación de tren", "der bán-hof", "Der Bahnhof ist groß.", "La estación es grande."),
            V("fahrkarte", "die Fahrkarte", "el pasaje / billete", "di fár-kar-te", "Ich kaufe eine Fahrkarte.", "Compro un pasaje."),
            V("zug", "der Zug", "el tren", "der tsuuk", "Der Zug kommt um zehn.", "El tren llega a las diez."),
            V("gleis", "das Gleis", "el andén / vía", "das glais", "Der Zug fährt von Gleis drei.", "El tren sale del andén tres."),
            V("koffer", "der Koffer", "la maleta", "der kó-fer", "Mein Koffer ist klein.", "Mi maleta es pequeña."),
            V("rucksack", "der Rucksack", "la mochila", "der rúk-sak", "Der Rucksack ist schwarz.", "La mochila es negra."),
            V("suchen", "suchen", "buscar", "sú-jen", "Ich suche Gleis drei.", "Busco el andén tres."),
            V("entschuldigung", "Entschuldigung", "disculpe / perdón", "ent-shúl-di-gung", "Entschuldigung, wo ist der Bahnhof?", "Disculpe, ¿dónde está la estación?"),
            V("links", "links", "a la izquierda", "links", "Der Eingang ist links.", "La entrada está a la izquierda."),
            V("einsteigen", "einsteigen", "subir (a transporte)", "áin-shtai-guen", "Lula steigt in den Zug ein.", "Lula sube al tren."),
        ),
        questions=(
            Q("¿A qué ciudad quiere viajar Lula?", ("Hamburgo", "Berlín", "Múnich", "Viena"), "Hamburgo", "Quiere ir «nach Hamburg»."),
            Q("¿Dónde compra el pasaje?", ("En la estación", "En el hotel", "En el bus", "En una cafetería"), "En la estación", "Compra la Fahrkarte en el Bahnhof."),
            Q("¿A qué hora sale el tren?", ("A las diez", "A las nueve", "A las once", "A las doce"), "A las diez", "«Um zehn Uhr» significa «a las diez»."),
            Q("¿Desde qué andén sale?", ("Andén tres", "Andén uno", "Andén dos", "Andén cinco"), "Andén tres", "Sale desde «Gleis drei»."),
            Q("¿Qué equipaje lleva?", ("Una maleta y una mochila", "Dos maletas", "Solo una cartera", "Una bicicleta"), "Una maleta y una mochila", "Lleva un Koffer y un Rucksack."),
            Q("¿Qué está buscando?", ("El andén tres", "Un restaurante", "Su pasaporte", "El baño"), "El andén tres", "Ella busca «Gleis drei»."),
            Q("¿A quién pide ayuda?", ("A un trabajador", "A una profesora", "A Ana", "A un policía"), "A un trabajador", "Pregunta a «einen Mitarbeiter»."),
            Q("¿Qué expresión usa para pedir ayuda?", ("Entschuldigung", "Gute Nacht", "Bitte schön", "Auf Wiedersehen"), "Entschuldigung", "Usa «Entschuldigung» antes de la pregunta."),
            Q("¿Hacia dónde señala el trabajador?", ("A la izquierda", "A la derecha", "Hacia arriba", "Hacia atrás"), "A la izquierda", "«nach links» significa «hacia la izquierda»."),
            Q("¿Dónde se sienta Lula?", ("Junto a la ventana", "Junto a la puerta", "En el pasillo", "No encuentra asiento"), "Junto a la ventana", "«Sie sitzt am Fenster» significa que se sienta junto a la ventana."),
        ),
    ),
    Lesson(
        id="essen",
        category="Comida",
        title_de="Im Café",
        title_es="En una cafetería",
        level="A1",
        minutes=12,
        paragraphs=(
            "Lula trifft Ana in einem Café. Die Kellnerin bringt die Speisekarte. Lula bestellt einen Kaffee mit Milch und ein Stück Apfelkuchen.",
            "Ana möchte einen Tee und ein Käsebrot. Das Café ist ruhig, und die Musik ist leise.",
            "Nach einer Stunde möchten sie bezahlen. Lula sagt: „Die Rechnung, bitte.“ Zusammen kostet alles achtzehn Euro.",
        ),
        spanish_help=(
            "Lula se encuentra con Ana en una cafetería. Pide café con leche y un trozo de pastel de manzana.",
            "Ana pide té y pan con queso. El lugar es tranquilo y la música está baja.",
            "Una hora después piden la cuenta. Todo cuesta dieciocho euros.",
        ),
        grammar_note="Para pedir algo, puedes usar «Ich möchte…» (quisiera…) o «Ich nehme…» (voy a tomar…). «Bitte» hace la frase más amable.",
        vocabulary=(
            V("cafe", "das Café", "la cafetería", "das ka-fé", "Das Café ist ruhig.", "La cafetería es tranquila."),
            V("kellnerin", "die Kellnerin", "la mesera", "di kél-ne-rin", "Die Kellnerin bringt die Karte.", "La mesera trae el menú."),
            V("speisekarte", "die Speisekarte", "el menú", "di shpái-se-kar-te", "Kann ich die Speisekarte haben?", "¿Me puede traer el menú?"),
            V("bestellen", "bestellen", "pedir / ordenar", "be-shté-len", "Ich bestelle einen Kaffee.", "Pido un café."),
            V("milch", "die Milch", "la leche", "di milj", "Kaffee mit Milch, bitte.", "Café con leche, por favor."),
            V("apfelkuchen", "der Apfelkuchen", "el pastel de manzana", "der áp-fel-ku-jen", "Der Apfelkuchen ist lecker.", "El pastel de manzana es rico."),
            V("ruhig", "ruhig", "tranquilo", "rú-ij", "Hier ist es ruhig.", "Aquí está tranquilo."),
            V("leise", "leise", "bajo / silencioso", "lái-se", "Die Musik ist leise.", "La música está baja."),
            V("rechnung", "die Rechnung", "la cuenta", "di réj-nung", "Die Rechnung, bitte.", "La cuenta, por favor."),
            V("kosten", "kosten", "costar", "kós-ten", "Das kostet zehn Euro.", "Eso cuesta diez euros."),
        ),
        questions=(
            Q("¿Con quién se encuentra Lula?", ("Con Ana", "Con Jonas", "Con su jefe", "Con Frau Weber"), "Con Ana", "«Lula trifft Ana» significa que Lula se encuentra con Ana."),
            Q("¿Dónde se encuentran?", ("En una cafetería", "En una estación", "En la universidad", "En una oficina"), "En una cafetería", "Se encuentran «in einem Café»."),
            Q("¿Quién trae el menú?", ("La mesera", "Ana", "Lula", "El chef"), "La mesera", "«Die Kellnerin» trae la carta."),
            Q("¿Qué bebida pide Lula?", ("Café con leche", "Té", "Agua", "Jugo"), "Café con leche", "Pide «einen Kaffee mit Milch»."),
            Q("¿Qué comida pide Lula?", ("Pastel de manzana", "Pan con queso", "Sopa", "Ensalada"), "Pastel de manzana", "Pide «ein Stück Apfelkuchen»."),
            Q("¿Qué bebida pide Ana?", ("Té", "Café", "Leche", "Agua"), "Té", "Ana quiere «einen Tee»."),
            Q("¿Cómo es el café?", ("Tranquilo", "Muy ruidoso", "Vacío y oscuro", "Grande y caro"), "Tranquilo", "«Das Café ist ruhig» significa que el café es tranquilo."),
            Q("¿Cómo está la música?", ("Baja", "Muy fuerte", "Rápida", "No hay música"), "Baja", "«leise» significa baja o silenciosa."),
            Q("¿Qué piden después de una hora?", ("La cuenta", "Otro menú", "Una mesa", "Un taxi"), "La cuenta", "Lula dice «Die Rechnung, bitte»."),
            Q("¿Cuánto cuesta todo?", ("18 euros", "8 euros", "20 euros", "16 euros"), "18 euros", "La cuenta total es «achtzehn Euro»."),
        ),
    ),
    Lesson(
        id="gesundheit",
        category="Salud",
        title_de="Beim Arzt",
        title_es="En el médico",
        level="A1",
        minutes=13,
        paragraphs=(
            "Lula fühlt sich heute nicht gut. Sie hat Kopfschmerzen und ist sehr müde. Deshalb ruft sie in einer Arztpraxis an.",
            "Die Sprechstundenhilfe gibt ihr einen Termin um drei Uhr. Der Arzt fragt: „Haben Sie Fieber?“ Lula sagt: „Nein, aber mein Hals tut weh.“",
            "Der Arzt empfiehlt Ruhe, Wasser und warmen Tee. Lula soll heute zu Hause bleiben.",
        ),
        spanish_help=(
            "Lula se siente mal: le duele la cabeza y está cansada. Llama a una consulta médica.",
            "Le dan una hora a las tres. No tiene fiebre, pero le duele la garganta.",
            "El médico recomienda descanso, agua y té caliente. Debe quedarse en casa.",
        ),
        grammar_note="Para indicar dolor se usa «Mein … tut weh» en singular: «Mein Hals tut weh». También puedes decir «Ich habe Kopfschmerzen».",
        vocabulary=(
            V("sich_fuhlen", "sich fühlen", "sentirse", "zij fú-len", "Ich fühle mich nicht gut.", "No me siento bien."),
            V("kopfschmerzen", "die Kopfschmerzen", "el dolor de cabeza", "di kópf-shmér-tsen", "Ich habe Kopfschmerzen.", "Me duele la cabeza."),
            V("mude", "müde", "cansada/o", "mú-de", "Lula ist müde.", "Lula está cansada."),
            V("arztpraxis", "die Arztpraxis", "la consulta médica", "di árts-prák-sis", "Ich rufe in der Arztpraxis an.", "Llamo a la consulta médica."),
            V("termin", "der Termin", "la cita / hora", "der ter-mín", "Ich habe einen Termin um drei.", "Tengo una cita a las tres."),
            V("fieber", "das Fieber", "la fiebre", "das fí-ber", "Haben Sie Fieber?", "¿Tiene fiebre?"),
            V("hals", "der Hals", "la garganta / cuello", "der hals", "Mein Hals tut weh.", "Me duele la garganta."),
            V("ruhe", "die Ruhe", "el descanso", "di rú-e", "Der Arzt empfiehlt Ruhe.", "El médico recomienda descanso."),
            V("warm", "warm", "caliente / tibio", "varm", "Ich trinke warmen Tee.", "Tomo té caliente."),
            V("zu_hause_bleiben", "zu Hause bleiben", "quedarse en casa", "tsu jáu-se blái-ben", "Heute bleibe ich zu Hause.", "Hoy me quedo en casa."),
        ),
        questions=(
            Q("¿Cómo se siente Lula?", ("No se siente bien", "Se siente excelente", "Está enojada", "Tiene hambre"), "No se siente bien", "La primera frase dice «nicht gut»."),
            Q("¿Qué dolor tiene?", ("Dolor de cabeza", "Dolor de espalda", "Dolor de estómago", "Dolor de rodilla"), "Dolor de cabeza", "Tiene «Kopfschmerzen»."),
            Q("¿Qué otro síntoma tiene?", ("Está muy cansada", "Tiene tos", "No puede caminar", "Tiene frío"), "Está muy cansada", "«Sehr müde» significa «muy cansada»."),
            Q("¿A dónde llama?", ("A una consulta médica", "A una universidad", "A una estación", "A una oficina"), "A una consulta médica", "Llama a una Arztpraxis."),
            Q("¿A qué hora es la cita?", ("A las tres", "A las dos", "A las cuatro", "A las cinco"), "A las tres", "Le dan una hora «um drei Uhr»."),
            Q("¿Tiene fiebre?", ("No", "Sí", "No se sabe", "Solo por la noche"), "No", "Lula responde «Nein»."),
            Q("¿Qué parte le duele además?", ("La garganta", "El brazo", "La pierna", "El oído"), "La garganta", "Dice «mein Hals tut weh»."),
            Q("¿Qué recomienda el médico?", ("Descanso, agua y té", "Correr y trabajar", "Café y ejercicio", "Viajar"), "Descanso, agua y té", "Son las tres recomendaciones del texto."),
            Q("¿Cómo debe estar el té?", ("Caliente", "Frío", "Con hielo", "Muy dulce"), "Caliente", "El médico recomienda «warmen Tee»."),
            Q("¿Qué debe hacer Lula hoy?", ("Quedarse en casa", "Ir a trabajar", "Tomar un tren", "Ir a una fiesta"), "Quedarse en casa", "Debe «zu Hause bleiben»."),
        ),
    ),
    Lesson(
        id="freizeit",
        category="Tiempo libre",
        title_de="Ein Samstag im Park",
        title_es="Un sábado en el parque",
        level="A1",
        minutes=12,
        paragraphs=(
            "Am Samstag trifft Lula ihre Freunde im Park. Das Wetter ist sonnig, aber nicht zu warm. Lula bringt Wasser und Obst mit.",
            "Zuerst gehen alle eine Runde spazieren. Danach spielen zwei Freunde Fußball. Lula liest auf einer Bank ein Buch.",
            "Am Nachmittag kaufen sie Eis. Um sechs Uhr geht Lula nach Hause. Sie hatte einen schönen Tag.",
        ),
        spanish_help=(
            "El sábado Lula se junta con amigos en el parque. Está soleado y lleva agua y fruta.",
            "Primero caminan. Dos amigos juegan fútbol y Lula lee un libro en una banca.",
            "En la tarde compran helado. Lula vuelve a casa a las seis después de un buen día.",
        ),
        grammar_note="Con los días de la semana se usa «am»: am Samstag, am Montag. Para decir «primero» y «después», usa «zuerst» y «danach».",
        vocabulary=(
            V("samstag", "der Samstag", "el sábado", "der sáms-tag", "Am Samstag gehe ich in den Park.", "El sábado voy al parque."),
            V("park", "der Park", "el parque", "der park", "Wir treffen uns im Park.", "Nos juntamos en el parque."),
            V("wetter", "das Wetter", "el clima", "das vé-ter", "Das Wetter ist schön.", "El clima está agradable."),
            V("sonnig", "sonnig", "soleado", "só-nij", "Heute ist es sonnig.", "Hoy está soleado."),
            V("obst", "das Obst", "la fruta", "das opst", "Ich bringe Obst mit.", "Llevo fruta."),
            V("spazieren", "spazieren gehen", "salir a caminar", "shpa-tsí-ren gue-en", "Wir gehen spazieren.", "Salimos a caminar."),
            V("fussball", "der Fußball", "el fútbol", "der fús-bal", "Sie spielen Fußball.", "Ellos juegan fútbol."),
            V("bank", "die Bank", "la banca", "di bank", "Lula sitzt auf einer Bank.", "Lula está sentada en una banca."),
            V("buch", "das Buch", "el libro", "das buj", "Ich lese ein Buch.", "Leo un libro."),
            V("eis", "das Eis", "el helado", "das ais", "Wir kaufen Eis.", "Compramos helado."),
        ),
        questions=(
            Q("¿Qué día va Lula al parque?", ("Sábado", "Lunes", "Miércoles", "Viernes"), "Sábado", "La historia comienza «Am Samstag»."),
            Q("¿Con quién se encuentra?", ("Con sus amigos", "Con su jefe", "Con su profesora", "Con una médica"), "Con sus amigos", "Se encuentra con «ihre Freunde»."),
            Q("¿Cómo está el clima?", ("Soleado", "Lluvioso", "Nevado", "Muy frío"), "Soleado", "«sonnig» significa soleado."),
            Q("¿Qué lleva Lula?", ("Agua y fruta", "Café y pastel", "Una maleta", "Un computador"), "Agua y fruta", "Trae Wasser und Obst."),
            Q("¿Qué hacen primero?", ("Caminan", "Comen helado", "Juegan fútbol", "Van a casa"), "Caminan", "«Zuerst» indica que primero dan una vuelta caminando."),
            Q("¿Cuántos amigos juegan fútbol?", ("Dos", "Uno", "Tres", "Todos"), "Dos", "«Zwei Freunde» significa «dos amigos»."),
            Q("¿Qué hace Lula mientras ellos juegan?", ("Lee un libro", "Duerme", "Trabaja", "Habla por teléfono"), "Lee un libro", "Lula lee en una banca."),
            Q("¿Dónde se sienta?", ("En una banca", "En el suelo", "En un café", "En el bus"), "En una banca", "«auf einer Bank» significa en una banca."),
            Q("¿Qué compran en la tarde?", ("Helado", "Pan", "Té", "Entradas"), "Helado", "Compran «Eis»."),
            Q("¿A qué hora vuelve Lula?", ("A las seis", "A las cinco", "A las siete", "A las ocho"), "A las seis", "Vuelve «um sechs Uhr»."),
        ),
    ),
)


LESSON_BY_ID = {lesson.id: lesson for lesson in LESSONS}
ALL_VOCABULARY: tuple[VocabularyItem, ...] = tuple(
    item for lesson in LESSONS for item in lesson.vocabulary
)
VOCABULARY_BY_ID = {item.id: item for item in ALL_VOCABULARY}


def validate_content() -> None:
    lesson_ids: set[str] = set()
    vocab_ids: set[str] = set()
    for lesson in LESSONS:
        if lesson.id in lesson_ids:
            raise ValueError(f"ID de lección duplicado: {lesson.id}")
        lesson_ids.add(lesson.id)
        if lesson.level != "A1":
            raise ValueError(f"Nivel inesperado en {lesson.id}: {lesson.level}")
        if len(lesson.questions) != 10:
            raise ValueError(f"{lesson.id} debe tener 10 preguntas de lectura.")
        if len(lesson.vocabulary) != 10:
            raise ValueError(f"{lesson.id} debe tener 10 palabras de vocabulario.")
        for question in lesson.questions:
            if question.answer not in question.options:
                raise ValueError(f"Respuesta ausente en alternativas: {question.prompt}")
            if len(set(question.options)) != 4:
                raise ValueError(f"Alternativas repetidas: {question.prompt}")
        for item in lesson.vocabulary:
            if item.id in vocab_ids:
                raise ValueError(f"ID de vocabulario duplicado: {item.id}")
            vocab_ids.add(item.id)


validate_content()
