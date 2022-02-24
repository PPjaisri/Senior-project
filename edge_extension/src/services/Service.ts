import axios from "axios";
import config from "./config";
import {
    send_file,
    send_text
} from "./types";

const baseUrl = config.baseUrl;

async function sendLink(body: send_text) {
    const res = await fetch(`${baseUrl}`, {
        method: 'post',
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(body)
    });

    const result = res.json();
    return result;
};

async function getLink() {
    const res = await fetch(`$(baseUrl)`);
    const result = res.json();

    return result;
}

async function sendImage(body: send_file) {
    const config = {
        headers: {
            "Accept": "application/json",
            "Content-Type": "multipart/form-data"
        }
    };

    let result;

    await axios.post(`${baseUrl}`, body, config)
        .then((res: any) => {
            result = res;
        })
    
    return result;
}

export {
    sendLink,
    getLink,
    sendImage
};