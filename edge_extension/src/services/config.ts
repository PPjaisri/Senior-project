const baseUrl: string = (process.env.NODE_ENV) === 'development' ? 'http://127.0.0.1:5000/extension' : 'http://127.0.0.1:5000/extension';

const CLIENT_ID_FB = '1009901223209735'
const CLIENT_SECRET_FB = 'a1a8a772e56c5c6d042a8f059c96caf8'

const config = {
    baseUrl: baseUrl,
    CLIENT_ID_FB: CLIENT_ID_FB,
    CLIENT_SECRET_FB: CLIENT_SECRET_FB
}

export default config;