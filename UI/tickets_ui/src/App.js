import './App.css';
import { ThemeProvider } from '@emotion/react';
import Header from './components/Header';
import { Grid } from '@mui/material';
import MainTheme from './components/MainTheme';
import NotFoundPage from './pages/notFoundPage'
import { Route, BrowserRouter as Router, Routes } from 'react-router-dom';
import Predict from './pages/predict';
import IssuesPage from './pages/issues';
import IssueUpdate from './pages/issueUpdate';

function App() {
  return (
    <ThemeProvider theme={MainTheme}>
      <Router>
        <div className="App">
          <Grid container>
            <Grid item xs={12}>
              <Header />
            </Grid>
            <Grid item xs={12}>
              <Routes>
                <Route path='/' element={<Predict />} />
                <Route path='/predict' element={<Predict />} />
                <Route path='/issues' element={<IssuesPage />} />
                <Route path='/issues/:issue_id' element={<IssueUpdate />} />
                <Route path='*' element={<NotFoundPage />} />
              </Routes>
            </Grid>
          </Grid>
        </div>
      </Router>
    </ThemeProvider>
  );
}

export default App;
