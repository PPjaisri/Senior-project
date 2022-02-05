/// <reference types="react-scripts" />

import fs from 'fs';

SSL_CRT_FILE = fs.readFileSync('./certs/tls.cert')
SSL_KEY_FILE = fs.readFileSync('./certs/tls.key')
