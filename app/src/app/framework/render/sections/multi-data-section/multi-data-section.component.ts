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
import { Component, Input, OnInit, TemplateRef, ViewChild } from '@angular/core';

import { BaseSectionComponent } from '../base-section/base-section.component';
import { Column } from 'src/app/layout/table/table.types';
/* ------------------------------------------------------------------------------------------------------------------ */

@Component({
    selector: 'cmdb-multi-data-section',
    templateUrl: './multi-data-section.component.html',
    styleUrls: ['./multi-data-section.component.scss']
})
export class MultiDataSectionComponent extends BaseSectionComponent implements OnInit{
    @Input() objectID: number;
    public multiDataColumns: Column[] = [];
    public multiDataValues = [];
    public totalCount: number = 0;

    // Table Template: Type actions column
    @ViewChild('actionsTemplate', { static: true }) actionsTemplate: TemplateRef<any>;

/* ------------------------------------------------------------------------------------------------------------------ */
/*                                                     LIFE CYCLE                                                     */
/* ------------------------------------------------------------------------------------------------------------------ */
    constructor() {
        super();
    }


    ngOnInit(): void {
        this.setColumns();
    }

/* ------------------------------------------------- HELPER METHODS ------------------------------------------------- */

    setColumns(){
        let fieldValues = {};

        for(let aField of this.fields){
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

            if(aField?.value) {
                fieldValues[aField.name] = aField.value;
            }
        }

        if(Object.keys(fieldValues).length > 0){
            this.multiDataValues.push(fieldValues);
    
            this.totalCount = this.multiDataValues.length;
    
            this.addActionColumn();
        }
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

/* -------------------------------------------------- HANDLE EVENTS ------------------------------------------------- */

    public onAddRowClicked(){
        console.log("clicked on add row");
    }
}
