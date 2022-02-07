import axios from "axios";
import config from "./config";
import { post_body, post_image_body } from "../types";

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

async function sendImage(body: any) {
    console.log(body);
    const res = await fetch(`${baseUrl}`, {
        method: 'post',
        headers: {
            "Accept": "application/json",
            "Content-Type": "multipart/form-data"
            // "Content-Type": "application/json"
        },
        body: body
    });

    // const res = await axios.post(`${baseUrl}`, JSON.stringify(body))

    // const result = res.json();
    console.log(res)
    return res;
}

function authenticate() {
    const { accessToken } = body();

    axios.get(`https://graph.facebook.com/v8.0/me?access_token=${accessToken}`)
        .then(response => {
            const { data } = response;
            if (data.error)
                // return unauthorized(data.error.message);
                console.log('error')

            let account = accounts.find(x => x.facebookId === data.id);
            if (!account) {
                // create new account if first time logging in
                account = {
                    id: newAccountId(),
                    facebookId: data.id,
                    name: data.name,
                    extraInfo: `This is some extra info about ${data.name} that is saved in the API`
                }
                accounts.push(account);
                localStorage.setItem(accountsKey, JSON.stringify(accounts));
            }

            return ok({
                ...account,
                token: generateJwtToken(account)
            });
        });
}

async function apiAuthenticate(accessToken: string) {
    // authenticate with the api using a facebook access token,
    // on success the api returns an account object with a JWT auth token
    const response = await axios.post(`${baseUrl}/authenticate`, { accessToken });
    const account = response.data;
    accountSubject.next(account);
    startAuthenticateTimer();
    return account;
}

export {
    sendLink,
    getLink,
    sendImage
};