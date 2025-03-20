import React, { useCallback, useState } from 'react';
import { Box, Typography, CircularProgress, Alert } from '@mui/material';
import { useDropzone } from 'react-dropzone';
import { uploadDocument } from '../services/api';
import { useTax } from '../contexts/TaxContext';

export const DocumentUpload: React.FC = () => {
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const { addDocument } = useTax();

  const onDrop = useCallback(async (acceptedFiles: File[]) => {
    setUploading(true);
    setError(null);

    try {
      for (const file of acceptedFiles) {
        const document = await uploadDocument(file);
        addDocument(document);
      }
    } catch (err) {
      setError('Failed to upload document. Please try again.');
      console.error('Upload error:', err);
    } finally {
      setUploading(false);
    }
  }, [addDocument]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'image/*': ['.jpeg', '.jpg', '.png'],
      'application/pdf': ['.pdf']
    },
    multiple: true
  });

  return (
    <Box sx={{ width: '100%', maxWidth: 600, mx: 'auto', my: 4 }}>
      <Box
        {...getRootProps()}
        sx={{
          border: '2px dashed',
          borderColor: isDragActive ? 'primary.main' : 'grey.300',
          borderRadius: 2,
          p: 4,
          textAlign: 'center',
          cursor: 'pointer',
          bgcolor: isDragActive ? 'action.hover' : 'background.paper',
          transition: 'all 0.2s ease'
        }}
      >
        <input {...getInputProps()} />
        {uploading ? (
          <CircularProgress />
        ) : (
          <Typography>
            {isDragActive
              ? 'Drop your tax documents here...'
              : 'Drag and drop your tax documents here, or click to select files'}
          </Typography>
        )}
      </Box>
      {error && (
        <Alert severity="error" sx={{ mt: 2 }}>
          {error}
        </Alert>
      )}
    </Box>
  );
}; 