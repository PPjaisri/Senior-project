import axios from "axios";
import { config } from "./config";
import { post_body, post_image_body } from "./types";

const baseUrl = config.baseUrl;

async function sendLink(body: post_body) {
    const res = await fetch(`${baseUrl}`, {
        method: 'post',
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(body)
    });

    const result = res.json();
    return result
};

async function getLink() {
    const res = await fetch(`$(baseUrl)`);
    const result = res.json();

    return result;
}

async function sendImage(body: post_image_body) {
    const res = await fetch(`${baseUrl}`, {
        method: 'post',
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(body)
    });

    const result = res.json();
    console.log(result)
    return result;
}

export {
    sendLink,
    getLink,
    sendImage
};