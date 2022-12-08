import {isMobileOnly as isMobile} from "react-device-detect";

export const ACTIONS = {
    ADD: 'add',
    CHANGE: 'change',
    add_component: 'add_component',
    REMOVE_CHILD: 'delete_child',
    REDIRECT: 'redirect',
    DOWNLOAD: 'download'
}

export const METHODS = {
    GET: 'GET',
    POST: 'POST'
}

export const HTTP_RESPONSE = {
    OK: 200,
    BAD_REQUEST: 400,
    SERVER_ERROR: 500,
    CONNECTION_ERROR: 100,
    equal: (status, response)=> Math.abs(response-status) < 10
}

export const FONTS = {
    SECULAR_ONE: 'Secular One',
    RUBIK: 'Rubik',
    HEEBO: 'Heebo',
    GISHA: 'Gisha'
}

export const COLORS = {
    BLACK: 'black',
    WHITE: 'white',
    GRAY: 'gray',
    NONE: 'none',
    ALERT: 'indianred',
    TALPIOT_DARK_BLUE: '#023247',
    TALPIOT_BLUE: '#005074',
    TALPIOT_CYAN: '#009CCC',
    TRANSPARENT: 'transparent',
    findColor: (color) => COLORS[color.toUpperCase()] || color
}

export const FILE_TYPES = {
    FORM: {name: 'form', type: 'form', icon: 'https://iconape.com/wp-content/png_logo_vector/google-forms.png'},
    FILE: {name: 'file', type: 'file', icon: 'https://img.icons8.com/pastel-glyph/2x/document--v3.png'},
    DOCS: {name: 'docs', type: 'document', icon: 'https://3.bp.blogspot.com/-SUFiWdpwOPk/XJC7coki2zI/AAAAAAAAJNQ/uoW7uJxwKoY2RuhghoWfhFPAtK8rDJA3gCK4BGAYYCw/s1600/logo%2Bmicrosoft%2Bword%2Bicon.png'},
    SHEETS: {name: 'sheets', type: 'sheet', icon: 'https://www.pngrepo.com/png/303193/512/microsoft-excel-2013-logo.png'},
    SLIDES: {name: 'slides', type: 'presentation', icon: 'https://cdn.worldvectorlogo.com/logos/microsoft-powerpoint-2013.svg'},
    PDF: {name: 'pdf', type: 'pdf', icon: 'https://upload.wikimedia.org/wikipedia/commons/8/87/PDF_file_icon.svg'},
    IMAGE: {name: 'image', type: 'image', icon: 'https://upload.wikimedia.org/wikipedia/commons/thumb/6/6b/Picture_icon_BLACK.svg/1200px-Picture_icon_BLACK.svg.png'},
    VIDEO: {name: 'video', type: 'video', icon: 'https://www.iconpacks.net/icons/1/free-video-icon-818-thumb.png'},
    FOLDER: {name: 'folder', type: 'folder', icon: 'https://img.icons8.com/emoji/452/open-file-folder-emoji.png'},
    SHORTCUT: {name: 'shortcut', type: 'shortcut', icon: 'https://img.icons8.com/emoji/452/open-file-folder-emoji.png'}
}

export const TIME_FORMATS = {
    JSON: 'YYYY-MM-DDTHH:mm:ssZ',
    BOOTSTRAP: {
        date: 'YYYY-MM-DD',
        time: 'HH:mm'
    }
}

export const SIZES = {
    xs: isMobile ? '0.75vw': '5px',
    sm: isMobile ? '1vw': '9px',
    md: isMobile ? '2vw': '16px',
    lg: isMobile ? '5vw': '21px',
    xl: isMobile ? '7vw': '36px',
}
