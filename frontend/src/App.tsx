import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { CssBaseline, ThemeProvider, createTheme } from '@mui/material';
import { TaxProvider } from './contexts/TaxContext';
import { TaxFilingPage } from './pages/TaxFilingPage';

const theme = createTheme({
  palette: {
    primary: {
      main: '#1976d2',
    },
    secondary: {
      main: '#dc004e',
    },
  },
});

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <TaxProvider>
        <Router>
          <Routes>
            <Route path="/" element={<TaxFilingPage />} />
          </Routes>
        </Router>
      </TaxProvider>
    </ThemeProvider>
  );
}

export default App;
