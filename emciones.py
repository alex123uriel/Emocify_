from textblob import TextBlob

emociones = {
    'amor': [
        'amor', 'enamorado', 'enamorada', 'romántico', 'romántica', 'te quiero', 'te amo', 'beso',
        'caricia', 'abrazo', 'cariño', 'querido', 'querida', 'adorado', 'adorada', 'afecto',
        'mi vida', 'mi cielo', 'mi amor', 'te extraño', 'contigo todo', 'me encantas', 'deseo verte',
        'me haces feliz', 'latido', 'tú y yo', 'complicidad', 'mi corazón', 'te necesito',
        'mariposas en el estómago', 'te pienso', 'mi alma gemela', 'eres lo mejor de mí',
        'te llevo en el alma', 'me haces falta', 'mi todo', 'lo eres todo para mí',
        'te adoro', 'quiero estar contigo', 'estoy para ti', 'solo tú', 'eres especial',
        'te pienso cada día', 'me iluminas', 'me haces sonreír'
    ],
    'celos': [
        'celos', 'celoso', 'celosa', 'posesivo', 'posesiva', 'inseguro', 'insegura',
        'desconfianza', 'por qué le hablas', 'te vi con alguien', 'no me gusta eso', 'quién es él',
        'quién es ella', 'lo estás viendo', 'me ocultas cosas', 'eso no me parece', 'te pasas',
        'te estoy viendo', 'no quiero compartirte', 'estás diferente', 'siento que lo ocultas',
        'me estás escondiendo algo', 'no lo soporto', 'me hierve la sangre'
    ],
    'envidia': [
        'envidia', 'envidioso', 'envidiosa', 'ojalá fuera yo', 'me gustaría tener', 'quién pudiera',
        'yo quiero eso', 'por qué no yo', 'qué suerte tienen otros', 'eso debería ser mío',
        'no es justo', 'todo le sale bien', 'le va mejor que a mí', 'quién como tú',
        'tiene todo lo que quiero', 'vida perfecta', 'qué envidia sana', 'me da coraje eso',
        'se lo merece más que yo', 'si yo tuviera eso'
    ],
    'euforia': [
        'emocionado', 'emocionada', 'increíble', 'eufórico', 'eufórica', 'euforia', 'wow',
        'alucinante', 'extraordinario', 'fantástico', 'brutal', 'épico', 'no lo creo',
        'demasiado bueno', 'exageradamente feliz', 'me voló la cabeza', 'al máximo',
        'me explotó el corazón', 'vibrando alto', 'no puedo con tanta emoción', 'explosión de felicidad',
        'esto es una locura', 'saltando de alegría'
    ],
    'entusiasmo': [
        'entusiasmado', 'entusiasmada', 'feliz', 'contento', 'contenta', 'motivado', 'motivada',
        'emocionante', 'genial', 'me encanta', 'qué bien', 'ánimo', 'ímpetu', 'estoy listo',
        'estoy lista', 'con ganas', 'super feliz', 'a darle', 'con toda la actitud', 'al 100',
        'con energía', 'me emociona esto', 'listo para todo', 'vamos con todo', 'hoy es el día',
        'con todas las pilas'
    ],
    'alegría': [
        'alegría', 'sonrisa', 'felicidad', 'risa', 'diversión', 'me alegra', 'gracias',
        'afortunado', 'afortunada', 'júbilo', 'regocijo', 'estoy feliz', 'día perfecto',
        'maravilloso', 'carcajada', 'todo va bien', 'es mi día', 'alegre', 'feliz de la vida',
        'feliz como una lombriz', 'no paro de reír', 'me alegraste el día', 'alegrón',
        'explosión de alegría'
    ],
    'serenidad': [
        'tranquilo', 'tranquila', 'sereno', 'serena', 'paz', 'calma', 'relajado', 'relajada',
        'zen', 'sosiego', 'quietud', 'equilibrio', 'momento de paz', 'todo en orden',
        'sin preocupaciones', 'armonía', 'fluye', 'estado de paz', 'bajo control', 'todo tranquilo',
        'respira profundo', 'en calma'
    ],
    'melancolía': [
        'melancolía', 'melancólico', 'melancólica', 'nostalgia', 'extraño', 'soledad', 'recuerdo',
        'pasado', 'vacío', 'añoranza', 'remordimiento', 'me hace falta', 'tiempos mejores',
        'cuando todo era mejor', 'mirando atrás', 'suspiros', 'duele recordar', 'me perdí en mis recuerdos',
        'los viejos tiempos', 'se me parte el alma', 'lágrimas en silencio'
    ],
    'tristeza': [
        'triste', 'llorando', 'dolor', 'deprimido', 'deprimida', 'desilusión', 'pena',
        'sufrimiento', 'desesperanza', 'desdicha', 'lágrimas', 'me siento mal', 'nada tiene sentido',
        'no puedo más', 'corazón roto', 'todo gris', 'día triste', 'sin ganas de nada',
        'estoy vacío', 'me duele el alma', 'no tengo fuerzas', 'llanto inconsolable', 'todo es oscuro'
    ],
    'enojo': [
        'enojo', 'molesto', 'molesta', 'furioso', 'furiosa', 'enojado', 'enojada', 'coraje',
        'odio', 'fastidio', 'irritación', 'exasperación', 'me harté', 'ya basta',
        'no lo soporto', 'maldito', 'me da rabia', 'me tienes harto', 'me tienes harta',
        'exploto', 'hasta aquí llegué', 'me sacas de quicio', 'no es justo esto', 'me alteras'
    ],
    'frustración': [
        'frustrado', 'frustrada', 'hartazgo', 'cansado', 'cansada', 'agotado', 'agotada',
        'rendido', 'rendida', 'harto', 'harta', 'desánimo', 'desesperación', 'no me sale nada',
        'no puedo más', 'nada funciona', 'todo mal', 'bloqueado', 'atascado', 'nada sirve',
        'me rindo', 'intento y nada', 'no avanza', 'todo está en mi contra'
    ],
    'miedo': [
        'miedo', 'temor', 'miedoso', 'miedosa', 'asustado', 'asustada', 'pánico', 'terror',
        'aprensión', 'me da cosa', 'tengo miedo', 'me asusta', 'inseguridad', 'angustia',
        'algo malo pasará', 'temblando', 'ansioso', 'ansiosa', 'no me atrevo', 'siento peligro',
        'esto me supera', 'me paraliza', 'tensión en el pecho'
    ],
    'sorpresa': [
        'sorpresa', 'inesperado', 'inesperada', 'inopinado', 'impactante', 'asombro',
        'no lo esperaba', 'qué locura', 'me sorprendió', 'de la nada', 'no lo puedo creer',
        'impresionante', 'de repente', 'sorprendente', 'me dejó sin palabras',
        'jamás lo pensé', 'me quedé en shock', 'increíble revelación'
    ],
    'gratitud': [
        'gracias', 'agradecido', 'agradecida', 'apreciado', 'apreciada', 'reconocido',
        'reconocida', 'mil gracias', 'te lo agradezco', 'muy agradecido', 'muy agradecida',
        'gracias de corazón', 'infinitas gracias', 'eternamente agradecido', 'bendecido',
        'no tengo palabras', 'gracias por tanto', 'qué detalle tan bonito', 'muy considerado'
    ],
    'orgullo': [
        'orgullo', 'orgulloso', 'orgullosa', 'satisfecho', 'satisfecha', 'triunfante',
        'me siento realizado', 'me siento realizada', 'lo logré', 'meta cumplida', 'valió la pena',
        'me superé', 'conseguido', 'esfuerzo recompensado', 'soy un crack', 'yo lo hice',
        'me lo gané', 'me reconozco'
    ],
    'vergüenza': [
        'vergüenza', 'avergonzado', 'avergonzada', 'culpable', 'remordimiento', 'metí la pata',
        'me da pena', 'no quería hacerlo', 'fue mi culpa', 'me siento mal por eso', 'me arrepiento',
        'ojalá no lo hubiera hecho', 'trágame tierra', 'qué oso', 'no sé dónde meterme'
    ],
    'esperanza': [
        'esperanza', 'esperanzado', 'esperanzada', 'optimista', 'fe', 'todo saldrá bien',
        'tengo fe', 'creo en el cambio', 'confío', 'vamos adelante', 'lo lograremos',
        'no pierdo la fe', 'hay luz al final', 'mantengo la esperanza', 'algo bueno vendrá',
        'nuevos comienzos', 'confianza en el futuro'
    ],
    'desesperanza': [
        'desesperanza', 'desesperado', 'desesperada', 'desmoralizado', 'desmoralizada', 'abatido',
        'abatida', 'todo está perdido', 'ya no importa', 'sin salida', 'no hay esperanza',
        'nada sirve ya', 'me rindo', 'fracaso total', 'no veo la salida', 'no hay solución',
        'oscuridad total', 'sin rumbo', 'vacío existencial'
    ]
}

emojis = {
    'alegría': [
        '😂', '😊', '😄', '😁', '😃', '😆', '😹', '🤣', '🥳', '😸', '😺', '✨', '🌞', '🌟', '🎉', '🎊', '🙌', '😇',
        '💃', '🕺', '🎈', '🌈', '😻', '💫', '😋', '🤗', '🎶', '🫶'
    ],
    'tristeza': [
        '😢', '😭', '💔', '😞', '😿', '😔', '🥺', '😓', '😥', '😩', '😖', '☹️', '🙁', '🌧️', '😫',
        '🫥', '🖤', '😟', '😪', '😶‍🌫️', '🫤'
    ],
    'enojo': [
        '😠', '😡', '🤬', '👿', '💢', '😤', '😾', '🔥', '🗯️', '😤', '💣', '🤯'
    ],
    'amor': [
        '❤️', '😍', '😘', '💖', '💕', '💞', '💘', '💓', '💗', '💝', '😻', '💑', '👩‍❤️‍👨', '🌹', '🌺', '🥰',
        '🤍', '🫶', '👩‍❤️‍💋‍👨', '👨‍❤️‍👨', '👩‍❤️‍👩', '💋', '💍'
    ],
    'neutral': [
        '🙂', '😐', '😶', '🙃', '😑', '🤔', '🤨', '🫥', '🫤'
    ],
    'frustración': [
        '😣', '😤', '😖', '😩', '😫', '😒', '😞', '🤯', '😔', '🫠', '🙄', '😕', '😓', '🤦', '😖'
    ],
    'melancolía': [
        '🥺', '😔', '😢', '😿', '🫥', '😟', '💭', '🌙', '☁️', '🌧️', '💔', '🖤'
    ],
    'euforia': [
        '🤩', '😵‍💫', '😛', '🎆', '🎇', '🎶', '💫', '🙀', '🌈', '🔥', '😝', '🥳', '🚀', '🕺', '💥'
    ],
    'sorpresa': [
        '😲', '😳', '😮', '😯', '🙀', '😱', '👀', '😧', '🫢', '😵', '😨', '🤯', '😦'
    ],
    'miedo': [
        '😨', '😰', '😱', '👻', '🫣', '🧟', '💀', '😖', '😬', '😵', '😟', '👀', '😳', '🕷️'
    ],
    'orgullo': [
        '😌', '💪', '🫡', '😎', '🏆', '🎖️', '🥇', '🦁', '👑', '🙌', '✨', '🎓'
    ],
    'vergüenza': [
        '🙈', '🙊', '😳', '😖', '😅', '🫣', '😓', '😬', '🙃', '😶‍🌫️'
    ],
    'esperanza': [
        '🌈', '✨', '☀️', '🙏', '💫', '🕊️', '🌄', '🤞', '🍀', '💐', '🌱', '🌻'
    ],
    'desesperanza': [
        '💔', '🖤', '😞', '🫥', '🌧️', '☁️', '😩', '😖', '😓', '😟', '😢', '🥀'
    ],
    'gratitud': [
        '🙏', '💐', '🌸', '🤗', '😊', '❤️', '🥹', '✨', '💝', '🙌', '💖', '🫶', '😇'
    ],
    'serenidad': [
        '🧘', '🌿', '🌊', '☁️', '🌅', '🌄', '🕊️', '🪷', '😌', '🧘‍♂️', '🧘‍♀️', '🫶'
    ]
}

def detectar_emocion(texto):
    texto = texto.lower()

    for emocion, palabras in emociones.items():
        if any(p in texto for p in palabras):
            return emocion

    for emocion, simbolos in emojis.items():
        if any(e in texto for e in simbolos):
            return emocion

    blob = TextBlob(texto)
    polaridad = blob.sentiment.polarity

    if polaridad > 0.4:
        return 'alegría'
    elif polaridad > 0.1:
        return 'entusiasmo'
    elif -0.1 <= polaridad <= 0.1:
        return 'neutral'
    elif -0.4 < polaridad < -0.1:
        return 'melancolía'
    elif polaridad <= -0.4:
        return 'tristeza'

    return 'neutral'
