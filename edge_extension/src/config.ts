const baseUrl: string = (process.env.NODE_ENV) === 'development' ? 'http://127.0.0.1:5000/extension' : 'other Url';

export const config = {
    baseUrl: baseUrl
}