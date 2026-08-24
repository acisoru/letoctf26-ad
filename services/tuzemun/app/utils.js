function encodeInt(value) {
    return Buffer.from(`value/${value}/encoded`).toString('base64');
}

function decodeInt(encoded) {
    return parseInt(Buffer.from(encoded, 'base64').toString().split('/')[1]);
}

module.exports = {
    encodeInt,
    decodeInt,
}