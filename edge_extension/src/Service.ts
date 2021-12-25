import { config } from "./config";
import { post_body } from "./types";

const baseUrl = config.baseUrl;

async function sendLink(body: post_body) {
    const res = await fetch(`${baseUrl}2`, {
        method: 'post',
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(body)
    });

    
    console.log('res', res);

    const result = res.json();
    if (result) {
        return result
    } else {
        return null;
    }
};

async function getLink() {
    const res = await fetch(`$(baseUrl)2`);
    const result = res.json();

    return result;
}

export {
    sendLink,
    getLink
};