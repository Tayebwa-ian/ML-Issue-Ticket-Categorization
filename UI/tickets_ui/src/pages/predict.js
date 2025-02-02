import { Container, Grid, TextField, Typography, Button, FormControl, MenuItem, Select, InputLabel } from "@mui/material";
import * as React from 'react';
import postUpdateDelete from "../CRUD/postUpdateDelete";
import { useNavigate } from "react-router-dom";

function Predict() {
    const [formData, setFormData] = React.useState({
        body: "",
        title: "",
        url: "",
        author: "",
    });
    const navigate = useNavigate()

    const handleSubmit = async (event) => {
        event.preventDefault();
        const { error } = await postUpdateDelete(`http://127.0.0.1:5000/api/core/predict`, formData);
        if (error) alert(`Invalid Inputs`);
        else navigate("/issues");
    };

    const handleChange = (event) => {
        const { name, value } = event.target;
        setFormData({
            ...formData,
            [name]: value
        });
    };

    return (
        <Container sx={{ width: 650, mt:5, mb: 5, textAlign: "center" }}>
            <Typography
            variant="h4"
            >
                Issue Submission
            </Typography>
            <Grid container spacing={-8}>
                <Grid item xs={12} sx={{ m:2}}>
                    <TextField 
                    required
                    label="Issue Title"
                    fullWidth
                    variant="outlined"
                    name="title"
                    value={formData.title}
                    onChange={handleChange}
                    />
                </Grid>
                <Grid item xs={12} sx={{ m:2}}>
                    <TextField
                    required
                    id="outlined-multiline-static"
                    fullWidth
                    label="Issue body"
                    multiline
                    rows={5}
                    name="body"
                    value={formData.body}
                    onChange={handleChange}
                    />
                </Grid>
                <Grid item xs={12} sx={{}}>
                    <FormControl sx={{width: 240 }}>
                        <InputLabel id="demo-simple-select-label">Author</InputLabel>
                        <Select
                        labelId="demo-simple-select-label"
                        id="demo-simple-select"
                        label="author"
                        name="author"
                        value={formData.author}
                        onChange={handleChange}
                        >
                            <MenuItem value="NONE">none</MenuItem>
                            <MenuItem value="MEMBER">member</MenuItem>
                            <MenuItem value="CONTRIBUTOR">contributor</MenuItem>
                            <MenuItem value="suspended">suspended</MenuItem>
                        </Select>
                    </FormControl>
                </Grid>
                <Grid item xs={12} sx={{ m:2}}>
                    <Button
                    variant="contained"
                    type="submit"
                    onClick={handleSubmit}
                    >
                        Submit
                    </Button>
                </Grid>
            </Grid>
        </Container>
    );
}

export default Predict;
