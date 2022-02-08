interface send_text {
    message_type: string,
    message: string
}

interface send_file {
    message_type: string,
    message: FormData
}

interface send_image_file {
    message_type: string,
    message: send_file
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
    send_text,
    send_file,
    send_image_file
}