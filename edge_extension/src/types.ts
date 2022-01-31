interface post_body {
    message_type: string,
    message: string | FileReader
}

interface post_image_body {
    message_type: string,
    message: FileReader
}

export type {
    post_body,
    post_image_body
}