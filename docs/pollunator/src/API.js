const URL = 'http://localhost:5000'
const STATIONS_URI = '/api/stations'
const PUBLIC_KEY_URI = '/api/publickey'
const SUBSCRIBE_URI = '/api/subscribe'

const STATIONS_URL = `${URL}${STATIONS_URI}`
const PUBLIC_KEY_URL = `${URL}${PUBLIC_KEY_URI}`
const SUBSCRIBE_URL = `${URL}${SUBSCRIBE_URI}`

export default URL;
export { STATIONS_URL, PUBLIC_KEY_URL, SUBSCRIBE_URL }
