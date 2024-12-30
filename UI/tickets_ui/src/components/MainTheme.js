import { createTheme } from "@mui/material";

const MainTheme = createTheme({
    palette: {
        mode: 'light',
        primary: {
          main: '#ff6d00',
        },
        secondary: {
          main: '#00c853',
        },
        divider: 'rgba(11,154,226,0.12)',
        info: {
          main: '#00e5ff',
        },
        success: {
          main: '#2979ff',
        },
        danger: {
          main: '#FF0000',
        },
        dark: {
          main: '#000000'
        },
      },
})

export default MainTheme;
