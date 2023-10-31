

import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';

export interface ValidationStatus {
    fieldName: string;
    isValid: boolean;
    initialValue: string
}

@Injectable({
    providedIn: 'root',
})
export class ValidationService {
    private labelFieldValues = new Map<string, string>();

    private nameValidationStatusMap = new Map<string, ValidationStatus>();
    nameValidationStatus$ = new BehaviorSubject<Map<string, ValidationStatus>>(
        this.nameValidationStatusMap
    );

    private labelValidationStatusMap = new Map<string, ValidationStatus>();
    labelValidationStatus$ = new BehaviorSubject<Map<string, ValidationStatus>>(
        this.labelValidationStatusMap
    );

    // Updates labelValidationStatusMap when a label is changed
    updatelabelValidationStatusMap(previousValue: string, newValue: string) {

        let existingMap = this.labelValidationStatus$.getValue();
        // console.log('existing mappppp', existingMap)
        if (existingMap.has(previousValue)) {
            const tempValue = existingMap.get(previousValue);

            // Remove the previous entry
            existingMap.delete(previousValue);

            // If newValue is not empty, update the key to newValue and use initialValue as the new value
            if (newValue.trim()) {
                existingMap.set(newValue, { fieldName: tempValue.fieldName, isValid: true, initialValue: tempValue.initialValue });
            } else {
                // If newValue is empty, use initialValue as the key only if initialValue is not empty
                if (tempValue.initialValue.trim()) {
                    existingMap.set(tempValue.initialValue, { fieldName: tempValue.fieldName, isValid: false, initialValue: tempValue.initialValue });
                }
            }
        }

        this.labelValidationStatus$.next(existingMap);
    }


    // Initializes data in labelValidationStatusMap
    initializeData(initialData: string) {
        let existingMap = this.labelValidationStatus$.getValue();
        existingMap.set(initialData, { fieldName: 'label', isValid: true, initialValue: initialData })
        this.labelValidationStatus$.next(existingMap)
    }

    // Updates labelValidationStatusMap when labels are deleted
    updatelabelValidationStatusMaponDeletion(updatedFields: any[]) {
        console.log('Updated Fields', updatedFields)
        const updatedFieldKeys = updatedFields.map(field => field.name);
        const existingMap = this.labelValidationStatus$.getValue();
        const entriesToDelete: string[] = [];
        existingMap.forEach((value, key) => {
            if (!updatedFieldKeys.includes(key)) {

                entriesToDelete.push(key);
            }
        });
        entriesToDelete.forEach(key => existingMap.delete(key));
        this.labelValidationStatus$.next(existingMap);
    }

    // Updates nameValidationStatusMap based on changes to name validation status
    updateNameValidationStatus(fieldName: string, isValid: boolean, fieldValue: string, initialValue: string) {
        // Check if the fieldValue already exists
        if (this.nameValidationStatusMap.has(fieldValue)) {
            const existingStatus = this.nameValidationStatusMap.get(fieldValue);

            // Check if isValid and fieldName are the same
            if (existingStatus.isValid === isValid && existingStatus.fieldName === fieldName) {
                return;  // No need to update if everything is the same
            }

            // Update the isValid status for the existing key
            existingStatus.isValid = isValid;

            // Swap the fieldValue if it's different
            if (existingStatus.fieldName !== fieldName) {
                this.nameValidationStatusMap.delete(fieldValue);  // Remove the old entry
                this.nameValidationStatusMap.set(fieldName, existingStatus);  // Add the new entry
            }
        } else {
            // Create a new entry if the fieldValue doesn't exist
            this.nameValidationStatusMap.set(fieldValue, { fieldName, isValid, initialValue });
        }

        this.nameValidationStatus$.next(this.nameValidationStatusMap);
    }

    // Gets the label field value for a given field name
    getLabelFieldValue(fieldName: string): string {
        return this.labelFieldValues.get(fieldName) || '';
    }


    // Updates labelValidationStatusMap based on changes to label validation status
    updateLabelValidationStatus(fieldName: string, isValid: boolean, fieldValue: string, initialValue: string) {
        if (fieldValue.length === 0 || fieldValue.length > 0) {
            if (this.labelValidationStatusMap.has(fieldValue)) {
                const existingStatus = this.labelValidationStatusMap.get(fieldValue);
                existingStatus.isValid = isValid;
                this.labelValidationStatusMap.set(fieldValue, existingStatus);
            } else {
                this.labelValidationStatusMap.set(fieldValue, { fieldName, isValid, initialValue });
            }

            this.labelValidationStatus$.next(this.labelValidationStatusMap);
        }
    }

    // Updates validation status based on the type (name or label)
    updateValidationStatus(type: string, isValid: boolean, fieldName: string, fieldValue: string, initialValue: string, previousValue: string) {
        if (type === 'name') {
            this.updatelabelValidationStatusMap(previousValue, fieldValue);
        } else if (type === 'label') {
            if (fieldName === 'dg_location') {
                this.updateLabelValidationStatus(fieldName, isValid, 'dg_location', 'dg_location');
            } else {
                const previousValue = this.getLabelFieldValue(fieldName);
                const valueToPass = previousValue !== fieldValue ? fieldValue : previousValue;
                this.updateLabelValidationStatus(fieldName, isValid, valueToPass, initialValue);
            }
        }
    }
}