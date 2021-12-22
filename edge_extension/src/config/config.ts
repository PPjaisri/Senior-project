const baseUrl: string = (process.env.NODE_ENV) === 'development' ? 'http://localhost:3000' : 'other Url';

export const config = {
    baseUrl: baseUrl
}