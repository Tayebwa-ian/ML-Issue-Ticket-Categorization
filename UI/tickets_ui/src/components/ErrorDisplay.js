import { WarningAmberOutlined } from '@mui/icons-material';
import { Alert } from '@mui/material';

export default function ErrorDisplay({error, severity}) {
    return (
        <Alert 
        icon={<WarningAmberOutlined fontSize="inherit" />}
        severity={severity}
        sx={{mb:2, mt:2}}
        >
            {error}
        </Alert>
    )
}
