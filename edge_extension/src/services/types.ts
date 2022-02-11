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

interface fb_token {
    message_type: string,
    facebook_access_token: string
}

interface result {
    size: number,
    type: string,
    search: string,
    result: string
}

export type {
    send_text,
    send_file,
    send_image_file,
    fb_token,
    result
}