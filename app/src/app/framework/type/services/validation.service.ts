

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

    setIsValid(key: string, value: boolean) {

        this.fieldValidity.set(key, value);
        const overallValidity = Array.from(this.fieldValidity.values()).every(
            (isValid) => isValid
        );
        this.isValid$.next(overallValidity);
    }


    setSectionValid(key: string, value: boolean) {
        this.sectionValidity.set(key, value);
        const overallValidity = Array.from(this.sectionValidity.values()).every(
            (isValid) => isValid
        );
        this.sectionValidity$.next(overallValidity);
    }


    getIsValid() {
        return this.isValid$.asObservable();
    }


    overallSectionValidity(): Observable<boolean> {
        return this.sectionValidity$.asObservable();
    }


    updateFieldValidityOnDeletion(deletedKey: string) {
        this.fieldValidity.delete(deletedKey);
        let overallValidity = Array.from(this.fieldValidity.values()).every(
            (isValid) => isValid
        );
        this.isValid$.next(overallValidity);
    }
}














