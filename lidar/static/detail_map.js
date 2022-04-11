$('.loader').hide();


const copy = '© <a href="https://osm.org/copyright">OpenStreetMap</a> contributors'
const url = 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png'
const osm = L.tileLayer(url, { attribution: copy })
let options = { 
    layers: [osm],
    minZoom: 1, 
    contextmenu: true,
    contextmenuItems: this.mapContextMenuItems,
    // Here :
    position: 'topleft', // or 'topright' or 'bottomleft' or 'bottomright'
 }
const map = L.map('map', options)
//map.locate()
//.on('locationfound', e => map.setView(e.latlng, 8))
//.on('locationerror', () => map.setView([0, 0], 5))





function onEachFeature( feature, layer ) 
    {
        layer.bindPopup( "<h3>Original_id: " + String(feature.properties.h_max) + "</h3>" );
        style=style;
    }

function onEachFeature_base( feature, layer ) 
    {
        style={
            fillColor: '#800026',
            weight: 2,
            opacity: 1,
            color: 'white',
            dashArray: '3',
            fillOpacity: 0.7
        }
    };
function style(feature) {
    return {
        fillColor: get_color(feature.properties.h_max),
        weight: 2,
        opacity: 1,
        color: 'white',
        dashArray: '3',
        fillOpacity: 0.7
    };
}
function get_color(feature_value){
    return  feature_value > 200 ? '#800026':
            feature_value > 100 ? '#BD0026':
            feature_value > 50 ? '#E31A1C':
            feature_value > 20 ? '#FC4E2A':
            feature_value > 10 ? '#FD8D3C':
            feature_value > 5 ? '#FEB24C':
            feature_value > 0  ? '#FED976':
                                '#FFEDA0' ;
};

function show_original_layer(documentid, url) {
    var data = {
        'documentid': documentid,
    }
    console.log('LLL')
    console.log(documentid)
    console.log(url)
    $.ajax({
        type: "GET",
        url: url,// the view function to post
        data: data,
        contentType: 'application/json;charset=UTF-8',
        beforeSend: function(){
            $('.loader').show();
            $('.mapaBase').hide();
        },
        complete: function(){
            $('.mapaBase').show();
            $('.loader').hide();
        },
        success: function(response) {
            console.log(map)
            const jsonData = jQuery.parseJSON(response.rawData)
            console.log(jsonData)
            var col = [];
            for (var i = 0; i < jsonData.length; i++) {
                for (var key in jsonData[i]) {
                    if (col.indexOf(key) === -1) {
                        col.push(key);
                    }
                }
            }
            console.log(col)
            var geojson = L.geoJSON(null, {onEachFeature: onEachFeature_base}).addTo(map);
            geojson.addData( jsonData)
            map.fitBounds(geojson.getBounds(), { padding:[50,50] } );
            
        },
        error: function(response){
            console.log(response.responseJSON.errors)
        }
    });
}


function calcular_alturas(documentid, url) {
    var data = {
        'documentid': documentid,
    }
    console.log(documentid)
    $.ajax({
        type: "GET",
        url: url,// the view function to post
        data: data,
        contentType: 'application/json;charset=UTF-8',
        beforeSend: function(){
            $('.loader').show();
            $('.mapaBase').hide();
            $('.tabla_datos').hide();
        },
        complete: function(){
            $('.mapaBase').show();
            $('.tabla_datos').show();
            $('.loader').hide();
        },
        success: function(response) {
            const jsonData = jQuery.parseJSON(response.rawData)
            var geojson = L.geoJSON(null, {onEachFeature: onEachFeature,  style: style}).addTo(map);
            geojson.addData( jsonData)
            map.fitBounds(geojson.getBounds(), { padding:[50,50] } );
            
        },
        error: function(response){
            console.log(response.responseJSON.errors)
        }
    });
    }