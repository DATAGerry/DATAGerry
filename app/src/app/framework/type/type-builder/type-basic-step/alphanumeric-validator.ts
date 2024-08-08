import { AbstractControl, ValidationErrors, ValidatorFn } from '@angular/forms';

/**
 * Creates a validator function that checks if the control value contains only alphanumeric characters.
 * 
 * @returns A ValidatorFn that checks the control's value and returns validation errors if the value is not alphanumeric.
 */
export function alphanumericValidator(): ValidatorFn {
    return (control: AbstractControl): ValidationErrors | null => {
        const valid = /^[a-zA-Z0-9]*$/.test(control.value);
        return valid ? null : { invalidCharacters: true };
    };
}