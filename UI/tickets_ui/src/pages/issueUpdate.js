import { useState } from 'react';
import {
  Box,
  Typography,
  Checkbox,
  FormControlLabel,
  Button,
  Paper,
  FormGroup,
  Container
} from '@mui/material';
import { useParams } from "react-router-dom";
import useGet from '../CRUD/get';
import ErrorDisplay from '../components/ErrorDisplay';
import DataLoading from '../components/DataLoading';
import postUpdateDelete from '../CRUD/postUpdateDelete';
import Divider from '@mui/material/Divider';
import { useNavigate } from 'react-router-dom';

function IssueUpdate () {
    const categories = ["Bug", "Enhancement", "Question"];
    const navigate = useNavigate();
    const {issue_id} = useParams();
    const {data: issue, error, isPending} = useGet(`http://127.0.0.1:5000/api/core/issues/${issue_id}`);
    const [formData, setFormData] = useState({
        body: null,
        title: null,
        author: null,
        actual_label: null,
        prediction: null
    });

    const handleCategoryChange = (category) => {
        setFormData({
            ...formData,
            actual_label: category,
            body: issue.body,
            title: issue.title,
            author: issue.author,
            prediction: issue.prediction
        });
    };
    
    const handleSubmit = () => {
        console.log(formData);
        if (formData.actual_label) {
            const { error } = postUpdateDelete(
                `http://127.0.0.1:5000/api/core/issues/${issue_id}`,
                formData,
                "PUT"
            );
            navigate("/issues");
            if (error) alert(error); else alert(`Issue categorized under: ${formData.actual_label}`);
        } else {
            alert("Please select the Issue category.");
        }
    };

    return (
        <Container maxWidth="sm" style={{ marginTop: "2rem" }}>
            { issue &&
                <Paper elevation={3} sx={{ padding: 3 }}>
                    <Typography variant="h5" gutterBottom>
                        {issue.title}
                    </Typography>
                    <Divider />
                    <Typography variant="body1" paragraph sx={{m:4}}>
                        {issue.body}
                    </Typography>
                    <Divider />
                    <Typography variant="subtitle1" color="text.secondary" gutterBottom>
                        Reported on: {issue.updated_at}
                    </Typography>
                    <Typography variant="subtitle1" color="text.secondary" gutterBottom>
                        Author: {issue.author}
                    </Typography>
                    <Typography variant="subtitle1" color="text.secondary" gutterBottom>
                        Predicted label: {issue.prediction}
                    </Typography>
                    <Typography variant="subtitle1" color="text.secondary" gutterBottom>
                        Actual Label: {issue.actual_label}
                    </Typography>

                    {/* Categories Selection */}
                    <Box>
                        <Typography variant="h5" gutterBottom>
                            Correct Issue label:
                        </Typography>
                        <FormGroup>
                        {categories.map((category) => (
                            <FormControlLabel
                            key={category}
                            control={
                                <Checkbox
                                checked={formData.actual_label === category}
                                onChange={() => handleCategoryChange(category)}
                                />
                            }
                            label={category}
                            />
                        ))}
                        </FormGroup>
                    </Box>

                    {/* Submit Button */}
                    <Button
                    variant="contained"
                    color="primary"
                    onClick={handleSubmit}
                    sx={{ marginTop: 2 }}
                    >
                        Submit
                    </Button>
                </Paper>
            }
            { isPending &&
                <DataLoading />
            }
            { error && <ErrorDisplay error={error} severity="warning"/>}
        </Container>
    );
}

export default IssueUpdate;
