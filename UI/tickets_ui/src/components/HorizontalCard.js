import * as React from 'react';
import Box from '@mui/material/Box';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import Typography from '@mui/material/Typography';
import { Grid } from '@mui/material';
import { Link } from 'react-router-dom';
import Divider from '@mui/material/Divider';


export default function HorizontalCard({data, key}) {

  return (
    <Link
    style={{
        display: 'block',
        textDecoration: 'none',
        color: 'inherit',
        border: '1px solid #ccc',
        padding: 5,
        borderRadius: '8px',
        mb: 4,
    }}
    to={`/issues/${data.id}`}
    key={key}
    >
        <Card sx={{ display: 'flex' }}>
            <Grid container spacing={2}>
                <Grid item xs={12}>
                    <Box sx={{ display: 'flex', flexDirection: 'column' }}>
                        <CardContent sx={{ flex: '1 0 auto' }}>
                        <Typography component="div" variant="h5">
                            <b>{data.title}</b>
                        </Typography>
                        <Divider />
                        <Typography component="div" sx={{mt:4, mb:4}}>
                            {data.body}
                        </Typography>
                        <Typography variant="subtitle1" component="div">
                            Reported: {data.created_at}<br/>
                            Author: {data.author}<br/>
                            <em>Probability: {data.pred_confidence}</em>
                            <br />
                            <em>Predicted label: {data.prediction}</em>
                            <br />
                            <em>Actual label: {data.actual_label}</em>
                        </Typography>
                        <br/>
                        </CardContent>
                    </Box>
                </Grid>
            </Grid>
        </Card>
    </Link>
  );
}
