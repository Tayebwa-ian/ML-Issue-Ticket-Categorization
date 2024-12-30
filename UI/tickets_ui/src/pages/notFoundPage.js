import { Container, Typography } from "@mui/material";
import { Link } from "react-router-dom"

const NotFoundPage = () => {
  return (
    <Container
    sx={{
        mt: 2,
        mb: 5,
        textAlign: "center",
    }}
    >
      <Typography variant="h2">Ooooppsss! Sorry</Typography>
      <Typography variant="h6">That page cannot be found</Typography>
      <Link to="/">Back to the start...</Link>
    </Container>
  );
}
 
export default NotFoundPage;
