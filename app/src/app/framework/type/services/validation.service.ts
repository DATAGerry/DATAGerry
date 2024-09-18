

import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable } from 'rxjs';

export interface ValidationStatus {
    fieldName: string;
    isValid: boolean;
    initialValue: string
}

@Injectable({
    providedIn: 'root',
})
export class ValidationService {


    public fieldValidity = new Map<string, boolean>();
    private isValid$ = new BehaviorSubject<boolean>(true);

    public sectionValidity = new Map<string, boolean>();
    private sectionValidity$ = new BehaviorSubject<boolean>(true);

    /**
     * Sets the validity of a specific field.
     * Updates the overall form validity based on the validity of all fields.
     * @param key - The field identifier.
     * @param value - The validity of the field (true if valid, false otherwise).
     */
    setIsValid(key: string, value: boolean) {

        this.fieldValidity.set(key, value);
        const overallValidity = Array.from(this.fieldValidity.values()).every(
            (isValid) => isValid
        );
        this.isValid$?.next(overallValidity);
    }

    /**
     * Sets the validity of a specific section.
     * Updates the overall section validity based on the validity of all sections.
     * @param key - The section identifier.
     * @param value - The validity of the section (true if valid, false otherwise).
     */
    setSectionValid(key: string, value: boolean) {
        this.sectionValidity.set(key, value);
        const overallValidity = Array.from(this.sectionValidity.values()).every(
            (isValid) => isValid
        );
        this.sectionValidity$?.next(overallValidity);
    }

    /**
     * Returns an observable that emits the overall validity of all fields.
     * @returns Observable<boolean> - The overall field validity.
     */
    getIsValid(): Observable<boolean> {
        return this.isValid$?.asObservable();
    }

    /**
     * Returns an observable that emits the overall validity of all sections.
     * @returns Observable<boolean> - The overall section validity.
     */
    overallSectionValidity(): Observable<boolean> {
        return this.sectionValidity$?.asObservable();
    }

    /**
     * Removes the validity entry of a deleted field and updates the overall validity.
     * @param deletedKey - The identifier of the field to delete.
     */
    updateFieldValidityOnDeletion(deletedKey: string) {
        if (this.fieldValidity.has(deletedKey)) {
            this.fieldValidity.delete(deletedKey);
            let overallValidity = Array.from(this.fieldValidity.values()).every(
                (isValid) => isValid
            );
            this.isValid$?.next(overallValidity);
        }
    }


    /**
     * Updates a section's key in the sectionValidity map.
     * 
     * @param prevKey - The previous identifier of the section.
     * @param newKey - The new identifier of the section.
     * @returns Whether the update was successful.
     */
    updateSectionKey(prevKey: string, newKey: string) {
        if (this.sectionValidity.has(prevKey)) {
            const isValid = this.sectionValidity.get(prevKey);
            this.sectionValidity.delete(prevKey);
            this.sectionValidity.set(newKey, isValid!);
            const overallValidity = Array.from(this.sectionValidity.values()).every(
                (isValid) => isValid
            );
            this.sectionValidity$?.next(overallValidity);
        }
    }


    /**
    * Cleans up the field and section validity maps by resetting them.
    * This function should be called when the component is destroyed to avoid memory leaks.
    */
    cleanup() {
        this.fieldValidity.clear();
        this.isValid$?.next(true);

        this.sectionValidity.clear();
        this.sectionValidity$?.next(true);
    }

}