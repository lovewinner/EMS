/**
 * NB: If you update this file, please also update `docs/src/app/customization/Themes.js`
 */
import {
    pinkA200, cyan500,
    grey100, grey300, grey400, grey500,
    white, darkBlack, fullBlack,
} from 'material-ui/styles/colors';
import { fade } from 'material-ui/utils/colorManipulator'
import spacing from 'material-ui/styles/spacing'

/**
 *  Light Theme is the default theme used in material-ui. It is guaranteed to
 *  have all theme variables needed for every component. Variables not defined
 *  in a custom theme will default to these values.
 */
export default {
    appBar: {
        height: 48,
        color: "#2c5cd0",
    },
    FlatButton: {
        fontWeight: 'bold',
    },
    spacing: spacing,
    fontFamily: '"Noto Sans SC", Roboto, sans-serif',
    borderRadius: 4,
    palette: {
        primary1Color: '#4285f4',
        primary2Color: '#4285f4',
        primary3Color: '#4285f4',
        accent1Color: pinkA200,
        accent2Color: grey500,
        accent3Color: grey500,
        textColor: '#565656',
        secondaryTextColor: fade(darkBlack, 0.54),
        alternateTextColor: white,
        canvasColor: white,
        borderColor: grey300,
        disabledColor: fade(darkBlack, 0.3),
        pickerHeaderColor: cyan500,
        clockCircleColor: fade(darkBlack, 0.07),
        shadowColor: fullBlack,
    },
};