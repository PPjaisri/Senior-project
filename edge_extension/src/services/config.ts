const url = 'https://361a-124-121-4-210.ngrok.io/extension'

const baseUrl: string = (process.env.NODE_ENV) === 'development' ? url : url;

const config = {
    baseUrl: baseUrl
}

export default config;