mapboxgl.accessToken =
    "pk.eyJ1Ijoic2ViYXN0aWFuZHVyYW52IiwiYSI6ImNrc3NjamoxNzBpcGcybmpzYnpzNmJkc2cifQ.RmdHKIqJm4SqauLFIBN2CQ";

const map = new mapboxgl.Map({
    container: "map",
    style: "mapbox://styles/mapbox/satellite-v9",
    center: [-73.012494, -39.798241],
    zoom: 10,
});

let element = document.createElement("h2");
var t = document.createTextNode("Valdivia"); // Create a text node
element.appendChild(t);
element.style["-webkit-text-stroke"] = "0.5px white";

const title = document.getElementById("title");

let marker = new mapboxgl.Marker(element)
    .setLngLat({
        lng: -73.234348,
        lat: -39.820650,
    })
    .addTo(map);

const geojson = {
    type: "FeatureCollection",
    features: [

    ],
};


async function actualizar(n) {
    const el = document.createElement("div");
    el.className = "cambio";
    nuevoNodo = {
        type: "Feature",
        geometry: {
            type: "Point",
            coordinates: [parseFloat(n[3]), parseFloat(n[2])],
        },
        properties: {
            title: parseInt(n[0]),
            description: n[1],
        },
    }
    geojson.features.push(nuevoNodo);
}

n = document.getElementById("nNodo").innerHTML;
n = n.slice(1, -1);
console.log(n)
var fNodo = n.split('), ');
for (i = 0; i < fNodo.length; i++) {
    fNodo[i] = fNodo[i].slice(1, -2);
    fNodo[i] = fNodo[i].split(',')
    actualizar(fNodo[i])
    console.log(fNodo[i])
}



// add markers to map
for (const {
        geometry,
        properties
    }
    of geojson.features) {
    // create a HTML element for each feature
    const el = document.createElement("div");
    el.className = "marker";

    // make a marker for each feature and add it to the map
    new mapboxgl.Marker(el)
        .setLngLat(geometry.coordinates)
        .setPopup(
            new mapboxgl.Popup({
                offset: 25
            }) // add popups
            .setHTML(`<h2 style="color:black;">${properties.title}</h2><h3 style="color:black;">${properties.description}</h3><a class="btn btn-secundary" href='/nodo/${properties.title}'> aquí </a>`)
        )
        .addTo(map);
}