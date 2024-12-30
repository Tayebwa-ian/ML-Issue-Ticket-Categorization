import { Container, Grid } from "@mui/material";
import HorizontalCard from "../components/HorizontalCard";
import useGet from "../CRUD/get";
import DataLoading from "../components/DataLoading";
import ErrorDisplay from "../components/ErrorDisplay";

export default function IssuesPage() {
    const {data: issues, isPending, error} = useGet("http://127.0.0.1:5000/api/core/predict");
    return (
        <Container
        sx={{
            mb: 5,
            mt: 5,
        }}
        >
            { issues &&
            <Grid container>
                <Grid item xs={12}>
                    { issues.map((issue, index) => (
                        <HorizontalCard key={index} data={issue} />
                    ))}
                </Grid>
            </Grid>
            }
            { isPending && <DataLoading />}
            { error && <ErrorDisplay error={error} severity="warning" />}
        </Container>
    );
}
