export interface TaxDocument {
  id: string;
  type: 'W2' | '1099' | 'Other';
  year: number;
  uploadedAt: Date;
  status: 'Pending' | 'Processed' | 'Error';
  imageUrl: string;
}

export interface UserProfile {
  id: string;
  firstName: string;
  lastName: string;
  email: string;
  ssn: string;
  filingStatus: 'Single' | 'MarriedJointly' | 'MarriedSeparately' | 'HeadOfHousehold';
  dependents: Dependent[];
}

export interface Dependent {
  id: string;
  firstName: string;
  lastName: string;
  ssn: string;
  relationship: string;
  dateOfBirth: Date;
}

export interface TaxReturn {
  id: string;
  year: number;
  status: 'Draft' | 'InProgress' | 'Completed' | 'Filed';
  totalIncome: number;
  totalDeductions: number;
  totalTax: number;
  refundAmount: number;
  documents: TaxDocument[];
  createdAt: Date;
  updatedAt: Date;
} 