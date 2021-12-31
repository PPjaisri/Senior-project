import { config } from "./config";
import { post_body } from "./types";

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

export {
    sendLink,
    getLink
};