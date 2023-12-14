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
import { Component, Input, OnInit } from '@angular/core';
import { FormControl, FormGroup } from '@angular/forms';
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
import { SectionTemplateService } from '../../services/section-template.service';
import { ToastService } from 'src/app/layout/toast/toast.service';
import { APIInsertSingleResponse, APIUpdateSingleResponse } from 'src/app/services/models/api-response';
import { Router } from '@angular/router';
import { RenderResult } from 'src/app/framework/models/cmdb-render';
/* ------------------------------------------------------------------------------------------------------------------ */

@Component({
    selector: 'section-template-builder',
    templateUrl: './section-template-builder.component.html',
    styleUrls: ['./section-template-builder.component.scss']
})
export class SectionTemplateBuilderComponent implements OnInit {

    @Input()
    public sectionTemplateID: number;

    public initialSection: any = {
        'name': this.randomName(),
        'label': 'Section',
        'type': 'section',
        'fields': []
    };


    public MODES: typeof CmdbMode = CmdbMode;
    public types = [];

    public formGroup: FormGroup;
    isNameValid = true;
    isLabelValid = true;
    isValid$: Observable<boolean>;



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

    /* --------------------------------------------------- LIFE CYCLE --------------------------------------------------- */
    constructor(
        private validationService: ValidationService,
        private sectionTemplateService: SectionTemplateService,
        private toastService: ToastService,
        private router: Router) {

            this.formGroup = new FormGroup({
                'isGlobal': new FormControl(false)
            });
    }

    ngOnInit(): void {

        //EDIT MODE
        if(this.sectionTemplateID > 0){
            this.getSectionTemplate(this.sectionTemplateID);
        }

        this.isValid$ = this.validationService.getIsValid();
    }


/* ---------------------------------------------------- API Calls --------------------------------------------------- */
    /**
     * Decides if a section template should be crated or updated
     */
    public handleSectionTemplate(){


        if(this.sectionTemplateID > 0){
            this.updateSectionTemplate();
        } else {
            this.createSectionTemplate();
        }
    }

    /**
     * Send section template data to backend for creation
     */
    public createSectionTemplate(){
        let params = {
            "name": this.initialSection.name,
            "label": this.initialSection.label,
            "is_global": this.formGroup.value.isGlobal,
            "fields": JSON.stringify(this.initialSection.fields) 
        }

        this.sectionTemplateService.postSectionTemplate(params).subscribe((res: APIInsertSingleResponse) => {
            this.toastService.success("Section Template created!");
            this.router.navigate(['/framework/section_templates']);
        }, error => {
            console.log("error in create section template response");
            this.toastService.error(error);
        });
    }


    /**
     * Send section template data to backend to update the existing section template
     */
    public updateSectionTemplate(){
        let params = {
            'name': this.initialSection.name,
            'label': this.initialSection.label,
            'type': 'section',
            'is_global': this.formGroup.value.isGlobal,
            'fields': JSON.stringify(this.initialSection.fields),
            'public_id': this.initialSection.public_id
        }

        this.sectionTemplateService.updateSectionTemplate(params).subscribe((res: APIUpdateSingleResponse) => {
            this.toastService.success("Section Template updated!");
            this.router.navigate(['/framework/section_templates']);
        }, error => {
          this.toastService.error(error);
        });
    }


    /**
     * Retrieves a section template with the given publicID
     * 
     * @param publicID publicID of section template which should be edited
     */
    private getSectionTemplate(publicID: number){
        this.sectionTemplateService.getSectionTemplate(publicID).subscribe((response: RenderResult) => {
            this.initialSection = response;
            this.formGroup.controls.isGlobal.setValue(this.initialSection.is_global);
          });
    }
/* ------------------------------------------------- EVENT HANDLERS ------------------------------------------------- */

    /**
     * Handels dropping fields in Fieldzone
     * 
     * @param event triggered when a field is dropped in the Fieldszone
     */
    public onFieldDrop(event: DndDropEvent) {
        if (event.dropEffect === 'copy' || event.dropEffect === 'move') {
            this.initialSection.fields.splice(event.index, 0, event.data);
        }
    }


    /**
     * Checks if the field already exists in the section
     * 
     * @param field fieldData
     * @returns True if it a new field
     */
    public isNewField(field: any): boolean {
        return this.initialSection.fields.indexOf(field) > -1;
    }


    /**
     * Triggered when an existing field is moved inside the section
     * 
     * @param item field data
     */
    public onFieldDragged(item: any) {
        const fieldIndex = this.initialSection.fields.indexOf(item);
        let updatedDraggedFieldName = this.initialSection.fields[fieldIndex].name;

        this.initialSection.fields.splice(fieldIndex, 1);
        this.validationService.setIsValid(updatedDraggedFieldName, true)
    }


    /**
     * Triggered when a field is removed
     * 
     * @param item field which should be removed
     */
    public removeField(item: any) {
        const indexField: number = this.initialSection.fields.indexOf(item);
        let removedFieldName = this.initialSection.fields[indexField].name;

        if (indexField > -1) {
            this.initialSection.fields.splice(indexField, 1);
            this.initialSection.fields = [...this.initialSection.fields];
            this.validationService.updateFieldValidityOnDeletion(removedFieldName);
        }
    }

/* ------------------------------------------------- HELPER METHODS ------------------------------------------------- */

    /**
     * Sets the icon for the different controls
     * 
     * @param value string of field type
     * @returns Icon string
     */
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


    /**
     * Generates a random name for the section
     * 
     * @returns (string): random name for section
     */
    private randomName() {
        return `section_template-${Math.floor(Math.random() * (99999 - 10000 + 1)) + 10000}`;
    }
}