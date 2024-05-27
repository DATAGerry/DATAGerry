/*
* DATAGERRY - OpenSource Enterprise CMDB
* Copyright (C) 2024 becon GmbH
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
import * as moment from 'moment';

import { Component, Input, OnDestroy, OnInit, TemplateRef, ViewChild } from '@angular/core';
import { UntypedFormControl } from '@angular/forms';

import { NgbModal, NgbModalRef } from '@ng-bootstrap/ng-bootstrap';

import { ObjectService } from 'src/app/framework/services/object.service';

import { BaseSectionComponent } from '../base-section/base-section.component';
import { Column } from 'src/app/layout/table/table.types';
import { PreviewModalComponent } from 'src/app/framework/type/builder/modals/preview-modal/preview-modal.component';
import { CmdbMultiDataSection, CmdbType } from 'src/app/framework/models/cmdb-type';
import { MultiDataSectionEntry, MultiDataSectionFieldValue, MultiDataSectionSet } from 'src/app/framework/models/cmdb-object';
import { DeleteEntryModalComponent } from '../modals/delete-entry-modal.component';
import { RenderResult } from 'src/app/framework/models/cmdb-render';
import { CmdbMode } from 'src/app/framework/modes.enum';
import { CollectionParameters } from 'src/app/services/models/api-parameter';
import { APIGetMultiResponse } from 'src/app/services/models/api-response';
/* ------------------------------------------------------------------------------------------------------------------ */

@Component({
    selector: 'cmdb-multi-data-section',
    templateUrl: './multi-data-section.component.html',
    styleUrls: ['./multi-data-section.component.scss']
})
export class MultiDataSectionComponent extends BaseSectionComponent implements OnInit, OnDestroy{
    @Input() public typeInstance: CmdbType;
    @Input() public renderResult: RenderResult;

    public referenceSummaries: any;
    public refTypesSummaries: any = {};

    public updateRequired = false;
    public multiDataColumns: Column[] = [];
    public multiDataValues = [];
    public totalCount: number = 0;

    formatedDataSection: MultiDataSectionEntry = {
        "section_id": "",
        "highest_id": 0,
        "values": [
            {
                "multi_data_id": 0,
                "data": []
            }
        ]
    };

    mdsTable = new UntypedFormControl('');

    // Table Template: Type actions column
    @ViewChild('actionsTemplate', { static: true }) actionsTemplate: TemplateRef<any>;

    private modalRef: NgbModalRef;
    public modalSection: any = {};

/* ------------------------------------------------------------------------------------------------------------------ */
/*                                                     LIFE CYCLE                                                     */
/* ------------------------------------------------------------------------------------------------------------------ */
    constructor(private modalService: NgbModal, private objectService: ObjectService) {
        super();
    }


    ngOnInit(): void {
        this.retrieveRefTypesSummaryLines(this.getRefTypes());

        this.initMultiDataSection();
        this.addFieldControls();

        this.setColumns();
        this.configureSectionData();

        if(this.mode == CmdbMode.View){
            this.getSummaryLines();
        } else {
            this.setMdsValues();
        }

    }


    ngOnDestroy(): void {
        if (this.modalRef) {
            this.modalRef.close();
        }
    }

/* ------------------------------------------------- HELPER METHODS ------------------------------------------------- */

    /**
     * Initialises the MultiDataSectionEntry which will be submited
     */
    initMultiDataSection(): void {
        if (this.mode == CmdbMode.View || this.mode == CmdbMode.Edit) {
            for (let aSection of this.renderResult.multi_data_sections) {
                if (aSection.section_id == this.section.name) {
                    this.formatedDataSection.section_id = aSection.section_id;
                    this.formatedDataSection.highest_id = aSection.highest_id;
                    this.formatedDataSection.values = aSection.values;
                }
            }
        } else {
            this.formatedDataSection = {
                "section_id": this.section.name,
                "highest_id": 0,
                "values": []
            }
        }
    }


    /**
     * Retrieves the next ID for a MultiDataSet
     * 
     * @returns (number): the next ID for a MultiDataSet
     */
    getNextMultiDataID(): number {
        return this.formatedDataSection.highest_id;
    }


    /**
     * Incrementy the highest ID for MultiDataSets
     */
    incrementNextMultiDataID(): void {
        this.formatedDataSection.highest_id += 1;
    }


    /**
     * Sets the values of the MultiDataSets for the table
     */
    setMdsValues(): void {
        for (let aValue of this.formatedDataSection.values) {
            let initialData = {}

            initialData['dg-multiDataRowIndex'] = aValue.multi_data_id;

            if (this.mode == CmdbMode.View) {
                for (let aDataSet of aValue.data) {
                    if(this.isRefField(aDataSet.name)) {
                        initialData[aDataSet.name] = this.referenceSummaries[aDataSet.value];
                    } else {
                        initialData[aDataSet.name] = aDataSet.value;
                    }
                }
            } else {
                for (let aDataSet of aValue.data) {
                    initialData[aDataSet.name] = aDataSet.value;
                }
            }



            this.multiDataValues.push(initialData);
        }
    }


    getRefTypes() {
        let refTypes = []

        if (this.typeInstance) {
            for (let field of this.typeInstance.fields) {
                if (field.type == 'ref' && field.ref_types) {
                    refTypes = [...refTypes, ... field.ref_types];
                }
            }
        }
        else if(this.renderResult) {
            for (let field of this.renderResult.fields) {
                if (field.type == 'ref' && field.ref_types) {
                    refTypes = [...refTypes, ... field.ref_types];
                }
            }
        }

        return refTypes;
    }


    retrieveRefTypesSummaryLines(refTypes: any) {
        if (refTypes) {
            const params: CollectionParameters = {
                filter: [{ $match: { type_id: { $in: refTypes } } }],
                limit: 0,
                sort: 'public_id',
                order: 1,
                page: 1
            };

            this.objectService.getObjects(params)
            .subscribe((apiResponse: APIGetMultiResponse<RenderResult>) => {
                let objectList = apiResponse.results;

                for (let refObject of apiResponse.results) {
                    if(refObject.summary_line) {
                        let summaryLine = `${refObject.type_information.type_label} #${refObject.object_information.object_id} - `;
                        summaryLine += refObject.summary_line;
                        this.refTypesSummaries[refObject.object_information.object_id] = summaryLine;
                    } else {
                        this.refTypesSummaries[refObject.object_information.object_id] = `${refObject.type_information.type_label} #${refObject.object_information.object_id}`;
                    }
                    
                }
            });
        }
    }


    getSummaryLines() {
        //if this object has MDS
        if(this.mode == CmdbMode.View) {
            let refIDs = this.getFieldReferences(this.renderResult.multi_data_sections);

            if(refIDs.length > 0){
                this.objectService.getObjectMdsReferences(refIDs[0], refIDs).subscribe({
                    next: (result) => {
                        this.referenceSummaries = this.convertToSummaryLines(result);
                        this.setMdsValues();
                    },
                    error: (error) => {
                        console.error(error);
                    }
                });
            }
        }
    }


    getFieldReferences(multiDataSections: any) {
        let refIDs = []

        for(let section of multiDataSections) {
            for (let value of (section.values)) {
                for (let dataSet of value.data) {
                    if (this.isRefField(dataSet.name) && dataSet.value) {
                        refIDs.push(dataSet.value);
                    }
                }
            }
        }

        return refIDs;
    }


    isRefField(fieldName: string): boolean {
        if (this.mode == CmdbMode.View) {
            for (let aField of this.renderResult.fields) {
                if (aField.name == fieldName) {
                    return aField.type == 'ref';
                }
            }
        }

        return false;
    }


    convertToSummaryLines(refData: any){
        let summaryLines = {}
        for (let refID in refData) {
            let refDataSet = refData[refID];

            let summaryLine = `${refDataSet["type_label"]} #${refDataSet["object_id"]}`;

            if (refDataSet["summaries"].length > 0) {
                summaryLine += " -"
                
                for (let summary of refDataSet["summaries"]) {
                    if (summary["value"]) {
                        summaryLine += ` ${summary["value"]} |`;
                    } else {
                        summaryLine += ` None |`
                    }
                    
                }

                // Remove the last '|' from the string
                summaryLine = summaryLine.substring(0, summaryLine.length -1);
            }

            summaryLines[refID] = summaryLine;
        }

        return summaryLines;
    }


    /**
     * Adds all FieldControls for the Form-Popups
     */
    addFieldControls(): void {
        //add the controls for all fields of mds
        for(let aField of this.fields){
            if (this.section.fields.includes(aField.name)) {
                const fieldControl = new UntypedFormControl('');
                this.form.addControl(aField.name, fieldControl);
            }
        }

        //add the mds-Control
        this.form.addControl("dg-mds-"+this.section.name, this.mdsTable);
        this.mdsTable.patchValue(this.formatedDataSection);
    }


    /**
     * Checks if a Field is a hidden field
     * @param fieldName (string): identifier of the Field which should be checked
     * @returns (boolean): True if it is a hidden field, else False
     */
    isHiddenField(fieldName: string): boolean {
        return (this.section as CmdbMultiDataSection).hidden_fields?.includes(fieldName);
    }


    /**
     * Sets the columns of the table
     */
    setColumns(): void{
        for(let aField of this.fields){
            if (this.section.fields.includes(aField.name) && !this.isHiddenField(aField.name)) {
                let fieldColumn: Column = {
                    display: aField.label,
                    name: aField.name,
                    data: aField.name,
                    searchable: false,
                    sortable: false,
                    fixed: true,
                    cssClasses: ['text-center'],
                };
    
                this.multiDataColumns.push(fieldColumn);
            }
        }

        this.addActionColumn();
    }


    /**
     * Adds the actions column to the table
     */
    public addActionColumn() {
        if (this.mode == CmdbMode.Create || this.mode == CmdbMode.Edit) {
            let actionsColumn: Column = {
                display: 'Actions',
                name: 'actions',
                data: 'actions',
                searchable: false,
                sortable: false,
                fixed: true,
                template: this.actionsTemplate,
                style: { width: '130px' },
                cssClasses: ['text-center']
            };
    
            this.multiDataColumns.push(actionsColumn);
        }
    }


    /**
     * Formats data for the modal sections
     */
    private configureSectionData() {
        this.modalSection['type'] = this.section.type;
        this.modalSection['name'] = this.section.name;
        this.modalSection['label'] = this.section.label;
        this.modalSection['fields'] = [];

        for (let sectionFieldIndex in this.section.fields){
            const aSectionFieldName = this.section.fields[sectionFieldIndex];

            for(let fieldIndex in this.fields) {
                const aField = this.fields[fieldIndex];

                if (aField.name == aSectionFieldName) {
                    this.modalSection['fields'].push(aField);
                    continue;
                }
            }
        }
    }


    private setFormattedData(newValues: any){
        let newDataSet: MultiDataSectionSet = {
            "multi_data_id": this.getNextMultiDataID(),
            "data": []
        }

        for (let fieldID in newValues) {
            let formattedValue = this.formatFieldValue(fieldID, newValues);

            let dataElement: MultiDataSectionFieldValue = {
                "name": fieldID,
                "value": formattedValue
            }
            newValues[fieldID] = formattedValue;
            newDataSet.data.push(dataElement);
        }

        this.formatedDataSection.values.push(newDataSet);
        this.mdsTable.patchValue(this.formatedDataSection);

        return newValues;
    }

/* ------------------------------------------------ FIELD FORMATTING ------------------------------------------------ */

    private formatFieldValue(fieldID: string, newValues:any){
        let fieldType = this.getFieldType(fieldID);

        switch (fieldType) {
            case "date": {
                if(newValues[fieldID]) {
                    const defaultDate = moment.utc(newValues[fieldID]);
                    return defaultDate.isValid() ? moment.tz(defaultDate, "UTC").format("YYYY-MM-DD") : newValues[fieldID];
                }
                
                break;
            }
            case "select": {
                if (newValues[fieldID]) {
                    return this.getOptionLabel(fieldID, newValues[fieldID]);
                }
                break;
            }
            case "radio": {
                if (newValues[fieldID]) {
                    return this.getOptionLabel(fieldID, newValues[fieldID]);
                }
                break;
            }
            case "ref": {
                if (newValues[fieldID] && this.refTypesSummaries) {
                    return this.refTypesSummaries[newValues[fieldID]];
                }
                break;
            }
        }

        return  newValues[fieldID];
    }


    private getOptionLabel(fieldID: string, value: string) {
        let fieldOptions = this.getField(fieldID)["options"];

        for (let option of fieldOptions) {
            if ( option["name"] == value) {
                return option["label"];
            }
        }

        return undefined;
    }


    private getTypeFields() {
        let typeFields = this.typeInstance.fields;

        if (this.mode == CmdbMode.Edit) {
            typeFields = this.renderResult.fields;
        }

        return typeFields;
    }


    private getField(fieldID: string) {
        let targetField = {};

        for (let aField of this.getTypeFields()) {
            if (aField["name"] == fieldID) {
                targetField = aField;
                break;
            }
        }

        return targetField;
    }


    private getFieldType(fieldID: string): string {
        let fieldType = "text";

        for (let aField of this.getTypeFields()) {
            if (aField["name"] == fieldID) {
                fieldType = aField["type"];
                break;
            }
        }

        return fieldType;
    }

/* ------------------------------------------------- TABLE HANDLING ------------------------------------------------- */

    private modifyFormattedData(newValues: any, multiDataID: number) {
        // first update the formatedDataSection
        for (let aDataSet of this.formatedDataSection.values) {
            if (aDataSet.multi_data_id == multiDataID){

                for(let aField of aDataSet.data){
                    aField.value = newValues[aField.name];
                }
                break;
            } 
        }

        // update the multiDataValues
        for(let multiDataEntry of this.multiDataValues) {
            if (multiDataEntry['dg-multiDataRowIndex'] == multiDataID) {
                for (let key in newValues) {
                    multiDataEntry[key] = newValues[key];
                }
            }
        }

        this.updateRequired = true;
        setTimeout(() => {
            this.updateRequired = false
        }, 0);

        this.mdsTable.patchValue(this.formatedDataSection);
    }


    getDataSet(multiDataID: number) {
        return  this.formatedDataSection.values.filter((dataSet) => dataSet.multi_data_id == multiDataID)[0].data;
    }


    getModalSectionData(multiDataID: number){
        let previewSection = {...this.modalSection};

        let dataSet = this.getDataSet(multiDataID);

        for (let entry of dataSet){

            for(let aField of previewSection.fields){
                if (entry.name == aField.name) {
                    aField['value'] = entry.value;
                    break;
                }
            }
        }

        return previewSection;
    }


    /**
     * Removes a MultiDataSet with the given MultiDataID from the table values
     * 
     * @param multiDataID (number): MultiDataID of MultiDataSet
     */
    removeFromTableValues(multiDataID: number): void {
        this.multiDataValues = this.multiDataValues.filter((rowData) => rowData['dg-multiDataRowIndex'] != multiDataID);
    }


    /**
     * Removes a MultiDataSet with the given MultiDataID from the current values
     * 
     * @param multiDataID (number): MultiDataID of MultiDataSet
     */
    removeDataSet(multiDataID: number): void {
        this.formatedDataSection.values = this.formatedDataSection.values.filter(
                                            (dataSet) => dataSet.multi_data_id != multiDataID
                                          );

        this.mdsTable.patchValue(this.formatedDataSection);
    }


    /**
     * Resets all values for modals so the create popup is empty
     */
    resetModalValues(): void {
        for (let aField of this.modalSection.fields) {
            if("value" in aField){
                delete aField["value"];
            }
        }
    }


    /**
     * Decides if the add button should be showed above the table
     * @returns (boolean): True if the add button should be showed about the table, else False
     */
    showAddButton(): boolean {
        return this.mode == CmdbMode.Create || this.mode == CmdbMode.Edit;
    }

/* -------------------------------------------------- HANDLE EVENTS ------------------------------------------------- */

    /**
     * Opens empty popup form to create a now table row
     */
    public onAddRowClicked(): void{
        this.resetModalValues();
        this.modalRef = this.modalService.open(PreviewModalComponent, { scrollable: true, size: 'lg' });
        this.modalRef.componentInstance.sections = [this.modalSection];
        this.modalRef.componentInstance.saveValues = true;

        this.modalRef.result.then((values: any) => {
            if (values){
                values = this.setFormattedData(values);

                values['dg-multiDataRowIndex'] = this.getNextMultiDataID();

                this.incrementNextMultiDataID();

                this.multiDataValues.push(values);
                this.totalCount = this.multiDataValues.length;

                this.form.markAsDirty();
            }
        });
    }


    /**
     * Opens popup to show preview of all values of the MultiDataSet
     * 
     * @param rowIndex (number): MultiDataID of MultiDataSet
     */
    public onRowPreview(rowIndex: number): void {
        this.modalRef = this.modalService.open(PreviewModalComponent, { scrollable: true, size: 'lg' });
        this.modalRef.componentInstance.activateViewMode = true;
        this.modalRef.componentInstance.sections = [this.getModalSectionData(rowIndex)];
    }


    /**
     * Opens popup to edit edit current values of the MultiDataSet
     * 
     * @param rowIndex (number): MultiDataID of MultiDataSet
     */
    public onRowEdit(rowIndex: number): void {
        this.modalRef = this.modalService.open(PreviewModalComponent, { scrollable: true, size: 'lg' });
        this.modalRef.componentInstance.saveValues = true;
        this.modalRef.componentInstance.sections = [this.getModalSectionData(rowIndex)];

        this.modalRef.result.then((values: any) => {

            if (values){
                this.modifyFormattedData(values, rowIndex);
                this.form.markAsDirty();
            }
        });
    }


    /**
     * Opens popup to confim deletion of a MultiDataSet
     * 
     * @param rowIndex (number): MultiDataID of MultiDataSet
     */
    public onRowDelete(rowIndex: number): void {
        this.modalRef = this.modalService.open(DeleteEntryModalComponent);

        this.modalRef.result.then((deleteConfirm: boolean) => {
            if(deleteConfirm){
                this.removeFromTableValues(rowIndex);
                this.removeDataSet(rowIndex);
                this.form.markAsDirty();
            }
        });
    }
}
