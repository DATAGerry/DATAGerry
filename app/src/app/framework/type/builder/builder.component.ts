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
import { ChangeDetectionStrategy, Component, EventEmitter, Input, OnChanges, OnDestroy, Output, SimpleChanges } from '@angular/core';

import { ReplaySubject } from 'rxjs';

import { DndDropEvent, DropEffect } from 'ngx-drag-drop';
import { NgbModal } from '@ng-bootstrap/ng-bootstrap';

import { ValidationService } from '../services/validation.service';

import { Controller } from './controls/controls.common';
import { SectionControl } from './controls/section.control';
import { Group } from '../../../management/models/group';
import { User } from '../../../management/models/user';
import { TextControl } from './controls/text/text.control';
import { PasswordControl } from './controls/text/password.control';
import { TextAreaControl } from './controls/text/textarea.control';
import { ReferenceControl } from './controls/specials/ref.control';
import { LocationControl } from './controls/specials/location.control';
import { RadioControl } from './controls/choice/radio.control';
import { SelectControl } from './controls/choice/select.control';
import { CheckboxControl } from './controls/choice/checkbox.control';
import { CmdbMode } from '../../modes.enum';
import { DateControl } from './controls/date-time/date.control';
import { RefSectionControl } from './controls/ref-section.common';
import { CmdbType, CmdbTypeSection } from '../../models/cmdb-type';
import { PreviewModalComponent } from './modals/preview-modal/preview-modal.component';
import { DiagnosticModalComponent } from './modals/diagnostic-modal/diagnostic-modal.component';
import { CmdbSectionTemplate } from '../../models/cmdb-section-template';
/* ------------------------------------------------------------------------------------------------------------------ */
declare var $: any;

@Component({
  selector: 'cmdb-builder',
  templateUrl: './builder.component.html',
  styleUrls: ['./builder.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class BuilderComponent implements OnChanges, OnDestroy {
    private subscriber: ReplaySubject<void> = new ReplaySubject<void>();
    public MODES: typeof CmdbMode = CmdbMode;

    public sections: Array<any> = [];
    public typeInstance: CmdbType;
  
    public newSections: Array<CmdbTypeSection> = [];
    public newFields: Array<CmdbTypeSection> = [];

    @Input()
    public sectionTemplates: Array<CmdbSectionTemplate> = [];

    @Input()
    public globalSectionTemplates: Array<CmdbSectionTemplate> = [];

    public selectedGlobalSectionTemplates: Array<CmdbSectionTemplate> = [];
    public globalSectionTemplateFields: Array<string> = [];

    @Input() public mode = CmdbMode.View;
    @Input() public groups: Array<Group> = [];
    @Input() public users: Array<User> = [];
    @Input() public types: Array<CmdbType> = [];
    @Input() public valid: boolean = true;

    @Input('typeInstance')
    public set TypeInstance(instance: CmdbType) {
        this.typeInstance = instance;
        if (instance !== undefined) {
        const preSectionList: any[] = [];
        for (const section of instance.render_meta.sections) {
            preSectionList.push(section);
            const fieldBufferList = [];
            for (const field of section.fields) {
            const found = instance.fields.find(f => f.name === field);
            if (found) {
                fieldBufferList.push(found);
            }
            }
            preSectionList.find(s => s.name === section.name).fields = fieldBufferList;
        }
        this.sections = preSectionList;
        }
    }

    @Output() public validChange: EventEmitter<boolean> = new EventEmitter<boolean>();


    public structureControls = [
        new Controller('section', new SectionControl()),
        new Controller('ref-section', new RefSectionControl())
    ];


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

    public constructor(private modalService: NgbModal, private validationService: ValidationService) {
        this.typeInstance = new CmdbType();
    }


    ngOnChanges(changes: SimpleChanges): void {
        if(this.globalSectionTemplates.length > 0 && this.globalSectionTemplateFields.length == 0){
            this.initGlobalFieldsList();
        }
    }


    ngOnDestroy(): void {
        this.subscriber.next();
        this.subscriber.complete();
    }


/* ------------------------------------------------ FIELD ITERACTIONS ----------------------------------------------- */

    private addRefSectionSelectionField(refSection: CmdbTypeSection): void {
        refSection.fields = [];
        refSection.fields.push(`${refSection.name}-field`);

        this.typeInstance.fields.push({
            type: 'ref-section-field',
            name: `${refSection.name}-field`,
            label: refSection.label
        });

        this.typeInstance.fields = [...this.typeInstance.fields];
    }


    private removeRefSectionSelectionField(refSection: CmdbTypeSection): void {
        const index = this.typeInstance.fields.map(x => x.name).indexOf(`${refSection.name}-field`);
        this.typeInstance.fields.splice(index, 1);
        this.typeInstance.fields = [...this.typeInstance.fields];
    }


    /**
     * Handels dropping any kind of section in the drop area
     * 
     * @param event DropEvent containing the section as data
     */
    public onSectionDrop(event: DndDropEvent): void {
        let sectionData = event.data;

        //check if it is a section template
        if('is_global' in sectionData){

            if(sectionData.is_global){
                this.selectedGlobalSectionTemplates.push(sectionData);

                let index = 0;
                for(let sectionIndex in this.globalSectionTemplates){
                    const aTemplate = this.globalSectionTemplates[sectionIndex];

                    if(aTemplate.name == sectionData.name){
                        index = parseInt(sectionIndex);
                        break;
                    }
                }

                this.globalSectionTemplates.splice(index, 1);
            }

            sectionData = this.extractSectionData(event.data);
        }


        if (this.sections && (event.dropEffect === 'copy' || event.dropEffect === 'move')) {

            let index = event.index;
            if (typeof index === 'undefined') {
                index = this.sections.length;
            }

            for (const el of this.sections) {
                const collapseCard = ($('#' + el.name) as any);
                collapseCard.collapse('hide');
            }

            if (event.dropEffect === 'copy') {
                this.newSections.push(sectionData);
            }

            this.sections.splice(index, 0, sectionData);
            this.typeInstance.render_meta.sections = [...this.sections];

            if (sectionData.type === 'ref-section' && event.dropEffect === 'copy') {
                this.addRefSectionSelectionField(sectionData as CmdbTypeSection);
            }

            //add fields of section template after the section was added
            if('is_global' in event.data){
                this.setSectionTemplateFields(event.data);
            }
        }
    }


  /**
   * This method checks if the field is used for an external link.
   * @param field
   */
    public externalField(field) {
        const include = { links: [], total: 0 };

        for (const external of this.typeInstance.render_meta.externals) {
            const fields = external.hasOwnProperty('fields') ? Array.isArray(external.fields) ? external.fields : [] : [];
            const found = fields.find(f => f === field.name);

            if (found) {
                if (include.total < 10) {
                    include.links.push(external);
                }

                include.total = include.total + 1;
            }
        }

        return include;
    }


    public onFieldDrop(event: DndDropEvent, section: CmdbTypeSection) {
        console.log("onFieldDrop() - is global:",this.isGlobalSection(section));
        if(this.isGlobalSection(section)){
            return;
        }


        const fieldData = event.data;

        if (section && (event.dropEffect === 'copy' || event.dropEffect === 'move')) {
            let index = event.index;

            if (typeof index === 'undefined') {
                index = section.fields.length;
            }

            if (event.dropEffect === 'copy') {
                this.newFields.push(fieldData);
            }

            section.fields.splice(index, 0, fieldData);
            this.typeInstance.render_meta.sections = [...this.sections];
            this.typeInstance.fields.push(fieldData);
            this.typeInstance.fields = [...this.typeInstance.fields];
        }
    }


    public onFieldDragged(item: any, section: CmdbTypeSection) {
        if(this.isGlobalSection(section)){
            return;
        }

        const sectionIndex = section.fields.indexOf(item);
        section.fields.splice(sectionIndex, 1);
        const fieldIndex = this.typeInstance.fields.indexOf(item);
        let updatedDraggedFieldName = this.typeInstance.fields[fieldIndex].name;

        this.typeInstance.fields.splice(fieldIndex, 1);
        this.typeInstance.fields = [...this.typeInstance.fields];
        this.validationService.setIsValid(updatedDraggedFieldName, true)
    }


    public onDragged(item: any, list: any[], effect: DropEffect) {
        if (effect === 'move') {
            const index = list.indexOf(item);
            list.splice(index, 1);
            this.sections = list;
            this.typeInstance.render_meta.sections = [...this.sections];
        }
    }


    public removeSection(item: CmdbTypeSection) {
        this.handleGlobalTemplates(item);

        const index: number = this.typeInstance.render_meta.sections.indexOf(item);

        if (index !== -1) {
            if (item.type === 'section') {
                const fields: Array<string> = this.typeInstance.render_meta.sections[index].fields;

                for (const field of fields) {
                    const fieldIdx = this.typeInstance.fields.map(x => x.name).indexOf(field);

                    if (index !== -1) {
                        this.typeInstance.fields.splice(fieldIdx, 1);
                    }
                }

                this.typeInstance.fields = [...this.typeInstance.fields];

            } else if (item.type === 'ref-section') {
                this.removeRefSectionSelectionField(item);
            }

            this.sections.splice(index, 1);
            this.typeInstance.render_meta.sections.splice(index, 1);
            this.typeInstance.render_meta.sections = [...this.typeInstance.render_meta.sections];
        }
    }


    public removeField(item: any, section: CmdbTypeSection) {
        const indexField: number = this.typeInstance.fields.indexOf(item);
        let removedFieldName = this.typeInstance.fields[indexField].name;

        if (indexField > -1) {
            this.typeInstance.fields.splice(indexField, 1);
            this.typeInstance.fields = [...this.typeInstance.fields];
            this.validationService.updateFieldValidityOnDeletion(removedFieldName);
        }

        const sectionFieldIndex = section.fields.indexOf(item);

        if (sectionFieldIndex > -1) {
            section.fields.splice(sectionFieldIndex, 1);
        }

        this.typeInstance.render_meta.sections = [...this.typeInstance.render_meta.sections];
    }


    public replaceAt(array, index, value) {
        const ret = array.slice(0);
        ret[index] = value;

        return ret;
    }

/* -------------------------------------------- SECTION TEMPLATE HANDLING ------------------------------------------- */

    public getDnDEffectAllowedForField(field: any){
        return this.isGlobalField(field.name) ? "none" : "move";
    }


    public getSectionMode(section: CmdbTypeSection, mode: CmdbMode){
        if(this.isGlobalSection(section)){
            return CmdbMode.Global
        }

        if(this.isNewSection(section)){
            return CmdbMode.Create
        }

        return mode;
    }


    public getSectionCollapseIcon(section: CmdbTypeSection){
        return this.isGlobalSection(section) ? ['far', 'eye'] : ['far', 'edit'];
    }


    public isGlobalSection(section: CmdbTypeSection){
        for(let sectionIndex in this.globalSectionTemplates){
            const aTemplate = this.globalSectionTemplates[sectionIndex];

            if(aTemplate.name == section.name){
                return true;
            }
        }

        for(let sectionIndex in this.selectedGlobalSectionTemplates){
            const aTemplate = this.selectedGlobalSectionTemplates[sectionIndex];

            if(aTemplate.name == section.name){
                return true;
            }
        }

        return false;
    }


    public isGlobalField(fieldName: string){
        return this.globalSectionTemplateFields.indexOf(fieldName) > -1;
    }


    private initGlobalFieldsList(){
        for(let templateIndex in this.globalSectionTemplates){
            let aTemplate = this.globalSectionTemplates[templateIndex];

            for(let fieldIndex in aTemplate.fields){
                let aField = aTemplate.fields[fieldIndex];
                this.globalSectionTemplateFields.push(aField.name);
            }

        }
    }


    private handleGlobalTemplates(sectionData: CmdbTypeSection){
        let isGlobalTemplate = false;
        let globalTemplateIndex: number = -1;

        for(let index in this.selectedGlobalSectionTemplates){
            const aSection = this.selectedGlobalSectionTemplates[index];
            if(aSection.name == sectionData.name){
                isGlobalTemplate = true;
                globalTemplateIndex = parseInt(index);
                this.globalSectionTemplates.push(aSection);
                this.globalSectionTemplates.sort((a, b) => a.public_id - b.public_id);
            }
        }

        if(isGlobalTemplate){
            this.selectedGlobalSectionTemplates.splice(globalTemplateIndex, 1);
        }
    }

    /**
     * 
     * @param data Extracts the section properties from the section template
     * @returns section properties
     */
    public extractSectionData(data: CmdbSectionTemplate){
        let sectionName: string = data.name;

        if(!this.isUniqueID(sectionName)){
            sectionName = this.createUniqueID('section_template');
        }

        return {
            'name': sectionName,
            'label': data.label,
            'type': data.type,
            'fields': data.fields
        }
    }


    /**
     * Sets the fields from the section template to the type instance
     * @param sectionTemplateFields 
     */
    public setSectionTemplateFields(sectionTemplate: CmdbSectionTemplate){
        let sectionTemplateFields = sectionTemplate.fields;

        for (let fieldIndex in sectionTemplateFields){
            let aField = sectionTemplateFields[fieldIndex];

            if(!this.isUniqueID(aField.name)){
                aField.name = this.createUniqueID(aField.type);
            }

            this.newFields.push(aField);
            this.typeInstance.fields.push(aField);
        }

        this.typeInstance.fields = [...this.typeInstance.fields];
    }


    /**
     * Creates a unique name for section templates and fields if a section template is added more than once
     * @param name (string): The typ of the field or 'section_template'
     */
    public getUniqueName(name: string){
            return this.createUniqueID(name);
    }


    /**
     * Creates a unique ID for a field or section
     * @param name (string): The name will be placed at the front of the ID
     */
    private createUniqueID(name: string){
        const uniqueID = `${name}-${Math.floor(Math.random() * (99999 - 10000 + 1)) + 10000}`;

        // if ID is already used then create a new one
        if(this.isUniqueID(uniqueID)){
            return uniqueID;
        } else {
            return this.createUniqueID(uniqueID);
        }
    }


    /**
     * Checks if the given ID already exists for a field or section
     * @param uniqueID THe given ID
     * @returns True if this ID is not used, else False
     */
    private isUniqueID(uniqueID: string){
        //first check all field names
        for (let fieldIndex in this.typeInstance.fields){
            let currentField = this.typeInstance.fields[fieldIndex];

            if(currentField.name == uniqueID){
                return false;
            }
        }

        //check all section names 
        for (let sectionIndex in this.typeInstance.render_meta.sections){
            let currentSection = this.typeInstance.render_meta.sections[sectionIndex];

            if(currentSection.name == uniqueID){
                return false;
            }
        }

        return true;
    }


/* ------------------------------------------------ HELPER FUNCTIONS ------------------------------------------------ */

    public isNewSection(section: CmdbTypeSection): boolean {
        return this.newSections.indexOf(section) > -1;
    }


    public isNewField(field: any): boolean {
        return this.newFields.indexOf(field) > -1;
    }


    public openPreview() {
        const previewModal = this.modalService.open(PreviewModalComponent, { scrollable: true });
        previewModal.componentInstance.sections = this.sections;
    }


    public openDiagnostic() {
        const diagnosticModal = this.modalService.open(DiagnosticModalComponent, { scrollable: true });
        diagnosticModal.componentInstance.data = this.sections;
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
}
