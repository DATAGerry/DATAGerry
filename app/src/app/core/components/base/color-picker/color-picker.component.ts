/*
* DATAGERRY - OpenSource Enterprise CMDB
* Copyright (C) 2026 becon GmbH
*
* This program is free software: you can redistribute it and/or modify
* it under the terms of the GNU Affero General Public License as
* published by the Free Software Foundation, either version 3 of the
* License, or (at your option) any later version.
*
* This program is distributed in the hope that it will be useful,
* but WITHOUT ANY WARRANTY; without even the implied warranty of
* MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
* GNU Affero General Public License for more details.

* You should have received a copy of the GNU Affero General Public License
* along with this program.  If not, see <https://www.gnu.org/licenses/>.
*/
import { Component, Input, forwardRef } from '@angular/core';
import { ControlValueAccessor, NG_VALUE_ACCESSOR } from '@angular/forms';
import { NgbDropdown } from '@ng-bootstrap/ng-bootstrap';

/** A colour is only painted/committed when it is a plain CSS name or a hex literal. */
const SAFE_COLOR = /^(#(?:[0-9a-f]{3}|[0-9a-f]{6})|[a-z]{3,20})$/i;
const HEX_COLOR = /^#(?:[0-9a-f]{3}|[0-9a-f]{6})$/i;
const NATIVE_FALLBACK_HEX = '#808080';

/** A small, fixed palette - enough to pick a common cable/port colour without opening the OS dialog. */
const DEFAULT_PRESETS: readonly string[] = [
    '#e94d18', '#f4511e', '#fb8c00', '#fdd835', '#7cb342', '#43a047',
    '#00897b', '#1e88e5', '#3949ab', '#8e24aa', '#d81b60', '#6d4c41',
    '#546e7a', '#000000', '#ffffff'
];

let uniqueColorPickerId = 0;

/**
 * Reusable colour field: free-text name/hex entry plus a swatch that opens a preset palette
 * and an OS colour dialog. Picking a preset closes the popover at once; opening the OS dialog
 * closes it too, since that dialog is a separate floating window we do not control.
 */
@Component({
    selector: 'app-color-picker',
    templateUrl: './color-picker.component.html',
    styleUrls: ['./color-picker.component.scss'],
    providers: [
        {
            provide: NG_VALUE_ACCESSOR,
            useExisting: forwardRef(() => ColorPickerComponent),
            multi: true
        }
    ],
    standalone: false
})
export class ColorPickerComponent implements ControlValueAccessor {
    @Input() label = 'Color';
    @Input() placeholder = 'e.g. blue or #1e88e5';
    @Input() required = false;
    @Input() disabled = false;
    @Input() errorMessage = '';
    @Input() presets: readonly string[] = DEFAULT_PRESETS;

    public readonly controlId = `app-color-picker-${ ++uniqueColorPickerId }`;
    public value = '';

    private onChange: (value: string) => void = () => {};
    private onTouched: () => void = () => {};

/* -------------------------------------------------- GETTER / SETTER ------------------------------------------------ */

    /** Only painted once the typed text is something a browser can actually render. */
    public get swatchColor(): string | null {
        const trimmed = this.value.trim();

        return SAFE_COLOR.test(trimmed) ? trimmed : null;
    }

    /** The OS picker only understands #rrggbb, so a name or a short hex falls back to a neutral grey. */
    public get nativeValue(): string {
        const trimmed = this.value.trim();

        if (!HEX_COLOR.test(trimmed)) {
            return NATIVE_FALLBACK_HEX;
        }

        return trimmed.length === 4
            ? '#' + [...trimmed.slice(1)].map((digit) => digit + digit).join('')
            : trimmed;
    }

/* --------------------------------------------- CONTROL VALUE ACCESSOR ---------------------------------------------- */

    public writeValue(value: string | null): void {
        this.value = value ?? '';
    }

    public registerOnChange(fn: (value: string) => void): void {
        this.onChange = fn;
    }

    public registerOnTouched(fn: () => void): void {
        this.onTouched = fn;
    }

    public setDisabledState(isDisabled: boolean): void {
        this.disabled = isDisabled;
    }

/* ---------------------------------------------------- EVENTS ------------------------------------------------------- */

    public onTextInput(event: Event): void {
        this.setValue((event.target as HTMLInputElement).value);
    }

    public onBlur(): void {
        this.onTouched();
    }

    /** A preset is a direct commit: set it and close the popover immediately. */
    public onPickPreset(preset: string, dropdown: NgbDropdown): void {
        this.setValue(preset);
        this.onTouched();
        dropdown.close();
    }

    /**
     * The OS colour dialog (e.g. macOS's NSColorPanel) does not close itself once a colour is picked.
     * Blurring the input is the only lever we have on it, and it works: Chromium treats the input
     * losing focus as the dialog's owner going away and dismisses the panel.
     */
    public onNativePick(event: Event): void {
        const input = event.target as HTMLInputElement;

        this.setValue(input.value);
        this.onTouched();
        input.blur();
    }

/* ------------------------------------------------ PRIVATE FUNCTIONS ------------------------------------------------ */

    private setValue(value: string): void {
        this.value = value;
        this.onChange(value);
    }
}
