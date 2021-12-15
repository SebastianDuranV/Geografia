var config = {
    style: 'mapbox://styles/rukaguare/cki66xz6f2djh19o4wef05j9h',
    accessToken: 'pk.eyJ1IjoicnVrYWd1YXJlIiwiYSI6ImNraTY2dTUxeTB0MzMyeG53cjg2ZjdzOXgifQ.JRKz36Io_o_fVWYp2XCxeQ',
    showMarkers: false,
    alignment: 'left',
    theme: 'light',
    title: 'Valle los Exploradores',
    subtitle: 'Características generales',
    byline: '',
    footer: 'Varios autores',
    chapters: [
        {
            id: 'general',
            title: 'Ubicación general',
            image: 'figura1.png',
            description: 'El valle de los exploradores queda localizado en el sur de Chile, en la región de Aissén. Esta zona se localiza al noreste del campo de hielo sur. En el mapa se puede apreciar los hitos más importantes de la región.',
            location: {
                center: [ -73.20563, -46.57581],
                zoom: 9,
                pitch: 0,
                bearing: 11.20
            },
            onChapterEnter: [],
            onChapterExit: []
        },
        {
            id: 'puertotranquilo',
            title: '1. Punto de partida: Puerto Tranquilo',
            image: '',
            description: 'Puerto Tranquilo es sitio de llegada y servicios básicos para los visitantes y turistas. El Glaciar Exploradores recibe a miles de turistas al año siendo una de las principales fuentes económicas de Puerto Tranquilo.',
            location: {
                center: [-72.67136, -46.62618],
                zoom:  15.34,
                pitch: 27.00,
                bearing: -144.21
            },
            onChapterEnter: [],
            onChapterExit: []
        },
        {
            id: 'caminovalle',
            title: '2. Camino al Valle los Exploradores',
            image: 'figura2.png',
            description: 'Para ir hacia el glaciar Exploradores, se debe atravesar por un valle colgado, generado por los procesos de erosión desarrollado por los procesos hidrológicos y glaciológicos. Como consecuencias, se generaron diferentes lagos como el Lago Tranquilo y Bayo y cascadas como La Nutria.',
            location: {
                center: [-72.84144, -46.63567],
                zoom: 12.35,
                pitch: 60.00,
                bearing: -54.41
            },
            onChapterEnter: [],
            onChapterExit: []
        },
        {
            id: 'lagunaespontanea',
            title: '3. Laguna Espontanea',
            image: 'figura3.png',
            description: 'Se generó el vaciamiento de un lago glaciar ocurrido el 27 de octubre de 2018, probablemente producido por olas tras el impacto de un fenómeno gravitacional. Una avalancha de nieve/hielo podría ser el gatillante del evento. La crecida arrasó con bosque y arrastró rocas de más de 3 m de diámetro, depositando el material 1.45 km abajo obstruyendo el Río Norte formando una laguna de 0.26 km². La laguna limitó el paso de turistas en 5 meses, generando centenas de millones de pesos en pérdidas en turismo y gastos de rehabilitación, incluyendo el drenaje parcial de la laguna, la construcción de un terraplén y el funcionamiento de un sistema de postas para el traslado de personal.',
            location: {
                center: [-72.90467, -46.57727],
                zoom: 13.86,
                pitch:  41.00,
                bearing: -120.01
            },
            onChapterEnter: [],
            onChapterExit: []
        },
        {
            id: 'exploradores1',
            title: '4. Glaciar exploradores: Características',
            image: 'figura4.png',
            description: 'Localizado al  Noreste del Campo de Hielo Norte, es la masa de glaciar que desciende del cerro más grande del  campo de hielo (cerrro San Valentín). En el glaciar se forman diferentes túneles que  conenctan flujos superficiales de agua con drenajes basales.',
            location: {
                center: [-73.09532, -46.53833],
                zoom: 10.98,
                pitch: 0.00,
                bearing: 172.79
            },
            onChapterEnter: [],
            onChapterExit: []
        },
        {
            id: 'exploradores2',
            title: '5. Glaciar exploradores: Retroceso del graciar',
            image: 'figura5.png',
            description: 'En los últimos 45 años se ha perdido gran parte del Glaciar Exploradores. Entre 1987 a 2020 se ha disminuido un 10.5% del glaciar (de 87.6 km2 a 78.5 km2). En el lóbulo frontal del glaciar se ha retrocedido alrededor de 900 metros. Se asume al cambio climático y a la intervención antrópica las principales causante del retroceso glaciar.',
            location: {
                center: [-73.14192, -46.51371],
                zoom: 12.33,
                pitch: 0.00,
                bearing: -176.01
            },
            onChapterEnter: [
                  {
                   layer: 'retroceso-3senef',
                   opacity: 1
                   }
            ],
            onChapterExit: [
                  {
                   layer: 'retroceso-3senef',
                   opacity: 0
                   }
             ]
        },
        {
            id: 'exploradores3',
            title: '6. Glaciar exploradores: Sistemas de monitoreo',
            image: '',
            description: '',
            location: {
                center: [ -73.16288, -46.49693],
                zoom: 13.37,
                pitch: 40.00,
                bearing: 175.19
            },
            onChapterEnter: [
                  {
                   layer: 'Sitios_monitoreo',
                   opacity: 1
                   }
            ],
            onChapterExit: [
                  {
                   layer: 'Sitios_monitoreo',
                   opacity: 0
                   }
             ]
        },
        {
            id: 'chileno',
            title: '7. GLOF valle de los Chilenos',
            image: 'figura6.png',
            description: 'Un GLOF se presentó en diciembre de 2015 en el valle Los Chilenitos. La inundación duró 8 días, con un volumen descargado de 105,6 × 106m3. Como consecuencias el canal se ensanchó hasta 130m y la elevación de la superficie bajó a 38.8 ± 1.5 m, generando un abanico de ~340 m de ancho y un aumento relativo de la elevación de 4,6±1,5 m. El acontecimiento fue el siguiente: Un gran volumen de desechos se desplazó desde noreste del terminal del Glaciar Chileno, desplazando el agua del lago e incrementando la descarga. El flujo de agua erosión los sedimentos morrénicos, para ser depositados aguas abajo.',
            location: {
                center: [-73.09990, -46.52061],
                zoom: 12.39,
                pitch: 0.50,
                bearing: 172.79
            },
            onChapterEnter: [],
            onChapterExit: []
        },
        {
            id: 'triangulo',
            title: 'GLOF Laguna Triangulo 2018',
            image: 'figura7.png',
            description: 'La laguna Triángulo, es otro ejemplo de GLOF. Se vació en abril de 2018,reduciendo su superficie de 0.98 a 0.54 km2 liberando ~20x10^6 de agua subiendo el nivel del río Deshielo más de 5 metros en el puente homónimo, 11 km aguas abajo.',
            location: {
                center: [-73.11529, -46.58191],
                zoom: 12.34,
                pitch: 41.00,
                bearing: 164.89
            },
            onChapterEnter: [],
            onChapterExit: []
        },
        {
            id: 'general2',
            title: 'Referencias',
            image: 'figura8.png',
            description: 'R.Wilson a,⁎, S. Harrisonb, J. Reynolds c, A. Hubbardd, N.F. Glasser d, O.Wündrich e, P. Iribarren Anacona f, L.Mao g, S. Shannon h. 2019. The 2015 Chileno Valley glacial lake outburst flood, Patagonia. Geomorphology 332, p. 51-65.',
            location: {
                center: [ -73.20563, -46.57581],
                zoom: 9,
                pitch: 0,
                bearing: 11.20
            },
            onChapterEnter: [],
            onChapterExit: []
        },
        
         
        
    ]
};