import React, { useEffect, useState } from 'react';
import {
  Container,
  Stepper,
  Step,
  StepLabel,
  Button,
  Typography,
  Box,
  Paper,
} from '@mui/material';
import { DocumentUpload } from '../components/DocumentUpload';
import { useTax } from '../contexts/TaxContext';
import { createTaxReturn, processDocuments, submitTaxReturn } from '../services/api';

const steps = [
  'Upload Documents',
  'Review Information',
  'AI Processing',
  'Final Review',
  'Submit',
];

export const TaxFilingPage: React.FC = () => {
  const [activeStep, setActiveStep] = useState(0);
  const [processing, setProcessing] = useState(false);
  const { currentTaxReturn, setCurrentTaxReturn, documents } = useTax();

  useEffect(() => {
    const initTaxReturn = async () => {
      if (!currentTaxReturn) {
        const newTaxReturn = await createTaxReturn(new Date().getFullYear());
        setCurrentTaxReturn(newTaxReturn);
      }
    };
    initTaxReturn();
  }, [currentTaxReturn, setCurrentTaxReturn]);

  const handleNext = async () => {
    if (activeStep === 2) {
      setProcessing(true);
      try {
        if (currentTaxReturn) {
          const updatedReturn = await processDocuments(currentTaxReturn.id);
          setCurrentTaxReturn(updatedReturn);
        }
      } catch (error) {
        console.error('Processing error:', error);
      } finally {
        setProcessing(false);
      }
    }

    if (activeStep === 4 && currentTaxReturn) {
      try {
        const submittedReturn = await submitTaxReturn(currentTaxReturn.id);
        setCurrentTaxReturn(submittedReturn);
      } catch (error) {
        console.error('Submission error:', error);
        return;
      }
    }

    setActiveStep((prevStep) => prevStep + 1);
  };

  const handleBack = () => {
    setActiveStep((prevStep) => prevStep - 1);
  };

  const renderStepContent = (step: number) => {
    switch (step) {
      case 0:
        return <DocumentUpload />;
      case 1:
        return (
          <Box>
            <Typography variant="h6">Uploaded Documents</Typography>
            {documents.map((doc) => (
              <Paper key={doc.id} sx={{ p: 2, my: 1 }}>
                <Typography>Type: {doc.type}</Typography>
                <Typography>Status: {doc.status}</Typography>
              </Paper>
            ))}
          </Box>
        );
      case 2:
        return (
          <Box sx={{ textAlign: 'center', py: 4 }}>
            {processing ? (
              <Typography>AI is processing your documents...</Typography>
            ) : (
              <Typography>Ready to process your tax documents</Typography>
            )}
          </Box>
        );
      case 3:
        return (
          <Box>
            <Typography variant="h6">Tax Return Summary</Typography>
            {currentTaxReturn && (
              <>
                <Typography>Total Income: ${currentTaxReturn.totalIncome}</Typography>
                <Typography>Total Deductions: ${currentTaxReturn.totalDeductions}</Typography>
                <Typography>Total Tax: ${currentTaxReturn.totalTax}</Typography>
                <Typography>Refund Amount: ${currentTaxReturn.refundAmount}</Typography>
              </>
            )}
          </Box>
        );
      case 4:
        return (
          <Box sx={{ textAlign: 'center', py: 4 }}>
            <Typography variant="h6">Ready to Submit</Typography>
            <Typography>
              Please review all information before submitting your tax return.
            </Typography>
          </Box>
        );
      default:
        return null;
    }
  };

  return (
    <Container maxWidth="md" sx={{ py: 4 }}>
      <Stepper activeStep={activeStep} sx={{ mb: 4 }}>
        {steps.map((label) => (
          <Step key={label}>
            <StepLabel>{label}</StepLabel>
          </Step>
        ))}
      </Stepper>

      {activeStep === steps.length ? (
        <Box sx={{ textAlign: 'center', py: 4 }}>
          <Typography variant="h5" gutterBottom>
            Tax Return Successfully Submitted!
          </Typography>
          <Typography>
            Your tax return has been submitted. You will receive a confirmation email shortly.
          </Typography>
        </Box>
      ) : (
        <>
          {renderStepContent(activeStep)}
          <Box sx={{ display: 'flex', justifyContent: 'space-between', mt: 4 }}>
            <Button
              disabled={activeStep === 0}
              onClick={handleBack}
            >
              Back
            </Button>
            <Button
              variant="contained"
              onClick={handleNext}
              disabled={processing}
            >
              {activeStep === steps.length - 1 ? 'Submit' : 'Next'}
            </Button>
          </Box>
        </>
      )}
    </Container>
  );
}; 