

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
    private isValid1$ = new BehaviorSubject<boolean>(true);


    setIsValid(key: string, value: boolean) {

        this.fieldValidity.set(key, value);

        const overallValidity = Array.from(this.fieldValidity.values()).every(
            (isValid) => isValid
        );

        this.isValid1$.next(overallValidity);


    }
    getIsValid() {
        return this.isValid1$.asObservable();
    }



    updateFieldValidityOnDeletion(deletedKey: string) {
        this.fieldValidity.delete(deletedKey);
        let overallValidity = Array.from(this.fieldValidity.values()).every(
            (isValid) => isValid
        );

        this.isValid1$.next(overallValidity);

    }
}














