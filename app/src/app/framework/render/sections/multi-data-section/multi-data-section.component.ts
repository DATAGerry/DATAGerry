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
import { Component, Input, OnDestroy, OnInit, TemplateRef, ViewChild } from '@angular/core';
import { UntypedFormControl } from '@angular/forms';

import { NgbModal, NgbModalRef } from '@ng-bootstrap/ng-bootstrap';

import { BaseSectionComponent } from '../base-section/base-section.component';
import { Column } from 'src/app/layout/table/table.types';
import { PreviewModalComponent } from 'src/app/framework/type/builder/modals/preview-modal/preview-modal.component';
import { CmdbType } from 'src/app/framework/models/cmdb-type';
import { MultiDataSectionEntry, MultiDataSectionFieldValue, MultiDataSectionSet } from 'src/app/framework/models/cmdb-object';
import { DeleteEntryModalComponent } from '../modals/delete-entry-modal.component';

/* ------------------------------------------------------------------------------------------------------------------ */

@Component({
    selector: 'cmdb-multi-data-section',
    templateUrl: './multi-data-section.component.html',
    styleUrls: ['./multi-data-section.component.scss']
})
export class MultiDataSectionComponent extends BaseSectionComponent implements OnInit, OnDestroy{
    @Input() public typeInstance: CmdbType;
    public updateRequired = false;

    public multiDataColumns: Column[] = [];
    public multiDataValues = [];
    public totalCount: number = 0;

    maxIndex: number = 0; 
    formatedDataSection: MultiDataSectionEntry = {
        "section_id": "",
        "values": [
            {
                "multi_data_id": this.maxIndex,
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
    constructor(private modalService: NgbModal) {
        super();
    }


    ngOnInit(): void {
        this.initMultiDataSection();
        this.addFieldControls();

        console.log("this.formatedDataSection", this.formatedDataSection);

        this.setColumns();
        this.configureSectionData();
    }


    ngOnDestroy(): void {
        if (this.modalRef) {
            this.modalRef.close();
        }
    }

/* ------------------------------------------------- HELPER METHODS ------------------------------------------------- */

    initMultiDataSection() {
        this.formatedDataSection = {
            "section_id": this.section.name,
            "values": []
        }
        this.formatedDataSection.section_id = this.section.name;
    }


    addFieldControls(){
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

    setColumns(){
        for(let aField of this.fields){

            if (this.section.fields.includes(aField.name)) {
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


            // if(aField?.value) {
            //     fieldValues[aField.name] = aField.value;
            // }
        }

        // if(Object.keys(fieldValues).length > 0){
        //     this.multiDataValues.push(fieldValues);
    
        //     this.totalCount = this.multiDataValues.length;
        // }

        this.addActionColumn();
    }


    public addActionColumn() {
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


    private configureSectionData() {
        this.modalSection['type'] = this.section.type;
        this.modalSection['name'] = this.section.name;
        this.modalSection['label'] = this.section.label;
        this.modalSection['fields'] = [];

        for (let sectionFieldIndex in this.section.fields){
            const aSectionFieldName = this.section.fields[sectionFieldIndex];

            for(let fieldIndex in this.typeInstance.fields) {
                const aField = this.typeInstance.fields[fieldIndex];

                if (aField.name == aSectionFieldName) {
                    this.modalSection['fields'].push(aField);
                    continue;
                }
            }
        }
    }


    private setFormattedData(newValues: any){
        let newDataSet: MultiDataSectionSet = {
            "multi_data_id": this.maxIndex,
            "data": []
        }

        for (let field_id in newValues) {
            let dataElement: MultiDataSectionFieldValue = {
                "name": field_id,
                "value": newValues[field_id]

            }

            newDataSet.data.push(dataElement);
        }

        this.formatedDataSection.values.push(newDataSet);

        this.mdsTable.patchValue(this.formatedDataSection);
    }


    private modifyFormattedData(newValues: any, multiDataID: number) {
        console.log("edited values:", newValues);
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


    removeFromFormValues(multiDataID: number){
        this.multiDataValues = this.multiDataValues.filter((rowData) => rowData['dg-multiDataRowIndex'] != multiDataID);
    }


    removeDataSet(multiDataID: number){
        this.formatedDataSection.values = this.formatedDataSection.values.filter(
                                            (dataSet) => dataSet.multi_data_id != multiDataID
                                          );

        this.mdsTable.patchValue(this.formatedDataSection);
    }

/* -------------------------------------------------- HANDLE EVENTS ------------------------------------------------- */

    public onAddRowClicked(){
        this.modalRef = this.modalService.open(PreviewModalComponent, { scrollable: true, size: 'lg' });
        this.modalRef.componentInstance.sections = [this.modalSection];
        this.modalRef.componentInstance.saveValues = true;

        this.modalRef.result.then((values: any) => {
            if (values){
                this.setFormattedData(values);

                values['dg-multiDataRowIndex']= this.maxIndex;

                this.maxIndex++;

                this.multiDataValues.push(values);
                this.totalCount = this.multiDataValues.length;
            }
        });
    }


    public onRowPreview(rowIndex: any) {
        this.modalRef = this.modalService.open(PreviewModalComponent, { scrollable: true, size: 'lg' });
        this.modalRef.componentInstance.activateViewMode = true;
        this.modalRef.componentInstance.sections = [this.getModalSectionData(rowIndex)];

    }


    public onRowEdit(rowIndex: any) {
        this.modalRef = this.modalService.open(PreviewModalComponent, { scrollable: true, size: 'lg' });
        this.modalRef.componentInstance.saveValues = true;
        this.modalRef.componentInstance.sections = [this.getModalSectionData(rowIndex)];

        this.modalRef.result.then((values: any) => {

            if (values){
                this.modifyFormattedData(values, rowIndex);
            }
        });
    }


    public onRowDelete(rowIndex: any) {
        this.modalRef = this.modalService.open(DeleteEntryModalComponent);

        this.modalRef.result.then((deleteConfirm: boolean) => {

            if(deleteConfirm){
                this.removeFromFormValues(rowIndex);
                this.removeDataSet(rowIndex);
            } 
        });
    }
}
