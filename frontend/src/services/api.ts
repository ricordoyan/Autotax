import axios from 'axios';
import { TaxDocument, UserProfile, TaxReturn } from '../types/tax';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const uploadDocument = async (file: File): Promise<TaxDocument> => {
  const formData = new FormData();
  formData.append('file', file);
  const response = await api.post('/documents/upload', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  return response.data;
};

export const getUserProfile = async (): Promise<UserProfile> => {
  const response = await api.get('/profile');
  return response.data;
};

export const updateUserProfile = async (profile: Partial<UserProfile>): Promise<UserProfile> => {
  const response = await api.put('/profile', profile);
  return response.data;
};

export const createTaxReturn = async (year: number): Promise<TaxReturn> => {
  const response = await api.post('/tax-returns', { year });
  return response.data;
};

export const getTaxReturn = async (id: string): Promise<TaxReturn> => {
  const response = await api.get(`/tax-returns/${id}`);
  return response.data;
};

export const processDocuments = async (taxReturnId: string): Promise<TaxReturn> => {
  const response = await api.post(`/tax-returns/${taxReturnId}/process`);
  return response.data;
};

export const submitTaxReturn = async (taxReturnId: string): Promise<TaxReturn> => {
  const response = await api.post(`/tax-returns/${taxReturnId}/submit`);
  return response.data;
}; 