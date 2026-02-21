import { Type } from "@google/genai";

export interface PatientInfo {
  name: string;
  age: string;
  gender: string;
  labNumber: string;
  collectionDate: string;
  reportDate: string;
}

export type Severity = "Normal" | "Mild" | "Moderate" | "Critical";

export interface LabTest {
  name: string;
  value: string;
  unit: string;
  referenceRange: string;
  interpretation: "Low" | "High" | "Normal";
  severity: Severity;
}

export interface LabReport {
  patientInfo: PatientInfo;
  healthScore: number;
  summary: {
    totalTests: number;
    normalTests: number;
    abnormalTests: number;
  };
  findings: LabTest[];
}

export const LabReportSchema = {
  type: Type.OBJECT,
  properties: {
    patientInfo: {
      type: Type.OBJECT,
      properties: {
        name: { type: Type.STRING },
        age: { type: Type.STRING },
        gender: { type: Type.STRING },
        labNumber: { type: Type.STRING },
        collectionDate: { type: Type.STRING },
        reportDate: { type: Type.STRING },
      },
      required: ["name", "age", "gender", "labNumber", "collectionDate", "reportDate"],
    },
    healthScore: { type: Type.NUMBER, description: "A score from 0 to 100 representing overall health based on the report." },
    summary: {
      type: Type.OBJECT,
      properties: {
        totalTests: { type: Type.INTEGER },
        normalTests: { type: Type.INTEGER },
        abnormalTests: { type: Type.INTEGER },
      },
      required: ["totalTests", "normalTests", "abnormalTests"],
    },
    findings: {
      type: Type.ARRAY,
      items: {
        type: Type.OBJECT,
        properties: {
          name: { type: Type.STRING },
          value: { type: Type.STRING },
          unit: { type: Type.STRING },
          referenceRange: { type: Type.STRING },
          interpretation: { type: Type.STRING, enum: ["Low", "High", "Normal"] },
          severity: { type: Type.STRING, enum: ["Normal", "Mild", "Moderate", "Critical"] },
        },
        required: ["name", "value", "unit", "referenceRange", "interpretation", "severity"],
      },
    },
  },
  required: ["patientInfo", "healthScore", "summary", "findings"],
};
