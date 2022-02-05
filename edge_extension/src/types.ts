interface post_body {
    message_type: string,
    message: string | FileReader
}

interface post_image_body {
    message_type: string,
    message: FormData | FileReader
}

interface fb_response {
    status: string,
    authResponse: {
        accessToken: string,
        data_access_expiration_time: number,
        expiresIn: number,
        reauthorize_required_in: string,
        signedRequest: string,
        userID: string
    }
}

export type {
    post_body,
    post_image_body,
    fb_response
}