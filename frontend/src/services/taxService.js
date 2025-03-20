import api from '../api/axios';

export const createTaxReturn = async (data) => {
  try {
    const response = await api.post('/api/tax-processing/tax-returns/', data);
    return response.data;
  } catch (error) {
    console.error('Error in createTaxReturn:', error.message);
    if (!error.response) {
      throw new Error('Network error - Please check if the backend server is running');
    }
    throw error;
  }
};

export const initTaxReturn = async () => {
  try {
    const response = await api.get('/api/tax-processing/tax-returns/init/');
    return response.data;
  } catch (error) {
    console.error('Error in initTaxReturn:', error.message);
    if (!error.response) {
      throw new Error('Network error - Please check if the backend server is running');
    }
    throw error;
  }
}; 