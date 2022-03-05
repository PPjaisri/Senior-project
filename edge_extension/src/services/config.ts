const url = 'http://192.168.1.43:5000/extension'

const baseUrl: string = (process.env.NODE_ENV) === 'development' ? url : url;

const config = {
    baseUrl: baseUrl
}

export default config;