import { Grid, CircularProgress, Box, Typography } from "@mui/material";

export default function DataLoading() {
    return (
        <Box sx={{ display: 'flex', justifyContent: "center" }}>
            <Grid>
                <Grid item>
                    <CircularProgress size={50} thickness={5} sx={{m:2}} />
                </Grid>
            </Grid>
            <Grid>
                <Grid item sx={{mt:4}}>
                    <Typography variant="h7">Fetching data............</Typography>
                </Grid>
            </Grid>
        </Box>
    );
}
