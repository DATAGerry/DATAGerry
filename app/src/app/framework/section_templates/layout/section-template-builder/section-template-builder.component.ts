/*
* DATAGERRY - OpenSource Enterprise CMDB
* Copyright (C) 2023 becon GmbH
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
*
* You should have received a copy of the GNU Affero General Public License
* along with this program. If not, see <https://www.gnu.org/licenses/>.
*/
import { Component, OnInit } from '@angular/core';
import { FormControl, FormGroup, UntypedFormControl, Validators } from '@angular/forms';
import { } from '@angular/material/checkbox';
import { DndDropEvent } from 'ngx-drag-drop';
import { Observable } from 'rxjs';

import { CmdbMode } from 'src/app/framework/modes.enum';
import { CheckboxControl } from 'src/app/framework/type/builder/controls/choice/checkbox.control';
import { RadioControl } from 'src/app/framework/type/builder/controls/choice/radio.control';
import { SelectControl } from 'src/app/framework/type/builder/controls/choice/select.control';
import { Controller } from 'src/app/framework/type/builder/controls/controls.common';
import { DateControl } from 'src/app/framework/type/builder/controls/date-time/date.control';
import { LocationControl } from 'src/app/framework/type/builder/controls/specials/location.control';
import { ReferenceControl } from 'src/app/framework/type/builder/controls/specials/ref.control';
import { PasswordControl } from 'src/app/framework/type/builder/controls/text/password.control';
import { TextControl } from 'src/app/framework/type/builder/controls/text/text.control';
import { TextAreaControl } from 'src/app/framework/type/builder/controls/text/textarea.control';
import { ValidationService } from 'src/app/framework/type/services/validation.service';
/* ------------------------------------------------------------------------------------------------------------------ */

@Component({
    selector: 'section-template-builder',
    templateUrl: './section-template-builder.component.html',
    styleUrls: ['./section-template-builder.component.scss']
})
export class SectionTemplateBuilderComponent implements OnInit {
    public MODES: typeof CmdbMode = CmdbMode;
    public types = [];

    public formGroup: FormGroup;
    public isGlobal: boolean = false;

    public initialSection: any = {
        'name': this.randomName(),
        'label': 'Section',
        'type': 'section',
        'fields': []
    };

    public basicControls = [
        new Controller('text', new TextControl()),
        new Controller('password', new PasswordControl()),
        new Controller('textarea', new TextAreaControl()),
        new Controller('checkbox', new CheckboxControl()),
        new Controller('radio', new RadioControl()),
        new Controller('select', new SelectControl()),
        new Controller('date', new DateControl())
    ];

    public specialControls = [
        new Controller('ref', new ReferenceControl()),
        new Controller('location', new LocationControl())
    ];

    isNameValid = true;
    isLabelValid = true;
    isValid$: Observable<boolean>;
    /* --------------------------------------------------- LIFE CYCLE --------------------------------------------------- */
    constructor(private validationService: ValidationService) {
        this.formGroup = new FormGroup({
            'isGlobalControl': new FormControl(this.isGlobal)
        });
    }

    ngOnInit(): void {
        this.isValid$ = this.validationService.getIsValid();
    }
    /* ----------------------------------------------------- METHODS ---------------------------------------------------- */


    public onFieldDrop(event: DndDropEvent) {
        const fieldData = event.data;
        if (event.dropEffect === 'copy' || event.dropEffect === 'move') {

            if (event.dropEffect === 'copy') {
                this.initialSection.fields.push(fieldData);
            }
            if (event.dropEffect === 'move') {
                this.initialSection.fields.splice(event.index, 0, fieldData);
            }
        }
    }


    public isNewField(field: any): boolean {
        return this.initialSection.fields.indexOf(field) > -1;
    }


    public onFieldDragged(item: any) {
        const fieldIndex = this.initialSection.fields.indexOf(item);
        let updatedDraggedFieldName = this.initialSection.fields[fieldIndex].name;

        this.initialSection.fields.splice(fieldIndex, 1);
        this.validationService.setIsValid(updatedDraggedFieldName, true)
    }


    public removeField(item: any) {
        const indexField: number = this.initialSection.fields.indexOf(item);
        let removedFieldName = this.initialSection.fields[indexField].name;

        if (indexField > -1) {
            this.initialSection.fields.splice(indexField, 1);
            this.initialSection.fields = [...this.initialSection.fields];
            this.validationService.updateFieldValidityOnDeletion(removedFieldName);
        }
    }


    public matchedType(value: string) {
        switch (value) {
            case 'textarea':
                return 'align-left';
            case 'password':
                return 'key';
            case 'checkbox':
                return 'check-square';
            case 'radio':
                return 'check-circle';
            case 'select':
                return 'list';
            case 'ref':
                return 'retweet';
            case 'location':
                return 'globe';
            case 'date':
                return 'calendar-alt';
            default:
                return 'font';
        }
    }


    private randomName() {
        return `section_template-${Math.floor(Math.random() * (99999 - 10000 + 1)) + 10000}`;
    }
}