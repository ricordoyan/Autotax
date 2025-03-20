import React, { createContext, useContext, useState, ReactNode } from 'react';
import { TaxReturn, UserProfile, TaxDocument } from '../types/tax';

interface TaxContextType {
  currentTaxReturn: TaxReturn | null;
  userProfile: UserProfile | null;
  documents: TaxDocument[];
  setCurrentTaxReturn: (taxReturn: TaxReturn | null) => void;
  setUserProfile: (profile: UserProfile | null) => void;
  addDocument: (document: TaxDocument) => void;
  removeDocument: (documentId: string) => void;
}

const TaxContext = createContext<TaxContextType | undefined>(undefined);

export const TaxProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [currentTaxReturn, setCurrentTaxReturn] = useState<TaxReturn | null>(null);
  const [userProfile, setUserProfile] = useState<UserProfile | null>(null);
  const [documents, setDocuments] = useState<TaxDocument[]>([]);

  const addDocument = (document: TaxDocument) => {
    setDocuments(prev => [...prev, document]);
  };

  const removeDocument = (documentId: string) => {
    setDocuments(prev => prev.filter(doc => doc.id !== documentId));
  };

  return (
    <TaxContext.Provider
      value={{
        currentTaxReturn,
        userProfile,
        documents,
        setCurrentTaxReturn,
        setUserProfile,
        addDocument,
        removeDocument,
      }}
    >
      {children}
    </TaxContext.Provider>
  );
};

export const useTax = () => {
  const context = useContext(TaxContext);
  if (context === undefined) {
    throw new Error('useTax must be used within a TaxProvider');
  }
  return context;
}; 