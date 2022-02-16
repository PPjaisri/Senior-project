const baseUrl: string = (process.env.NODE_ENV) === 'development' ?
    'http://127.0.0.1:5000/extension' :
    'http://127.0.0.1:5000/extension';

const config = {
    baseUrl: baseUrl
}

export default config;