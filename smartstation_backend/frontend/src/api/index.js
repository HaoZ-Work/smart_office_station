import axios from 'axios'

const BASE_URL = `/api/skill-managerhttp://127.0.0.1:8000/`


export function getValues() {
    return axios.get(`${BASE_URL}/dht22_data/get_last/`, )
}