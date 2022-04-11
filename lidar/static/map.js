const copy = '© <a href="https://osm.org/copyright">OpenStreetMap</a> contributors'
const url = 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png'
const osm = L.tileLayer(url, { attribution: copy })
const map = L.map('map', { layers: [osm], minZoom: 5 })
map.locate()
  .on('locationfound', e => map.setView(e.latlng, 8))
  .on('locationerror', () => map.setView([0, 0], 5))
/*const map = L.map('map', { layers: [osm] })
map.fitWorld();*/

async function load_lidar() {
    const lidar_url = `/api/lidar/?in_bbox=${map.getBounds().toBBoxString()}`
    const response = await fetch(lidar_url)
    const geojson = await response.json()
    return geojson
}
async function render_lidar() {
    map.removeLayer(L.geoJSON)
    const lidar = await load_lidar()
    return L.geoJSON(lidar).addTo(map)
}

map.on('moveend', render_lidar )

