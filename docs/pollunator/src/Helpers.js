import { PUBLIC_KEY_URL } from './API.js'

async function urlBase64ToUint8Array(base64String) {
    const padding = '='.repeat((4 - base64String.length % 4) % 4);
    const base64 = (base64String + padding)
        .replace(/\-/g, '+')
        .replace(/_/g, '/')
    ;
    const rawData = window.atob(base64);
    return Uint8Array.from([...rawData].map((char) => char.charCodeAt(0)));
}

async function getPublicKeyArray() {
    const response = await fetch(PUBLIC_KEY_URL)
    const key = await response.text()

    return urlBase64ToUint8Array(key)
}

export { urlBase64ToUint8Array, getPublicKeyArray }