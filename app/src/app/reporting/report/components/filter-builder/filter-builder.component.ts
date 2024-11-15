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
import { Component, Input, OnInit, OnChanges, SimpleChanges, EventEmitter, Output } from '@angular/core';
import { QueryBuilderConfig, QueryBuilderClassNames } from 'shout-angular-query-builder';

@Component({
    selector: 'app-filter-builder',
    templateUrl: './filter-builder.component.html',
    styleUrls: ['./filter-builder.component.scss']
})
export class FilterBuilderComponent implements OnInit, OnChanges {
    @Input() fields: Array<{ name: string; label: string; type?: string; options?: Array<{ name: string; value: any }> }> = [];
    @Output() conditionsChange = new EventEmitter<any>();
    @Output() filterBuilderValidation = new EventEmitter<any>();


    public query = { condition: 'and', rules: [] };
    public config: QueryBuilderConfig = { fields: {} };
    public classNames: QueryBuilderClassNames = {};
    public showQueryBuilder = true;

    /* --------------------------------------------------- LIFECYCLE METHODS -------------------------------------------------- */


    ngOnInit(): void {
        this.initializeConfig();
    }


    ngOnChanges(changes: SimpleChanges): void {
        if (changes.fields && !changes.fields.firstChange) {
            // Hide the query-builder component to force reinitialization
            this.showQueryBuilder = false;

            // Reset the entire query object
            this.query = {
                condition: 'and',
                rules: []
            };

            // Reinitialize the configuration
            this.initializeConfig();

            // Use setTimeout to re-show the component after it has been destroyed
            setTimeout(() => {
                this.showQueryBuilder = true;
            }, 0);
        }
    }

    /* --------------------------------------------------- QUERY CONFIGURATIONS -------------------------------------------------- */


    /**
     * Initializes the configuration for query fields based on available fields, setting default operators and types.
     */
    private initializeConfig(): void {
        if (this.fields && this.fields.length > 0) {
            const configFields: { [key: string]: any } = {};

            this.fields.forEach(field => {
                let fieldType = field.type;
                let operators = ['=', '!=', 'contains', 'is null', 'is not null', 'like']; // Default operators for non-numeric types

                // Check if the fieldType is specifically 'number' or 'date'
                if (fieldType === 'number' || fieldType === 'date') {
                    operators = ['=', '!=', '<', '>', '<=', '>='];
                }
                else if (fieldType === 'select') {
                    operators = ['=', '!=', 'in', 'not in'];
                    fieldType = 'category';
                }
                else {
                    // Treat any other type as 'string'
                    fieldType = 'string';
                }

                configFields[field.name] = {
                    name: field.label,
                    type: fieldType,
                    operators: operators,
                    defaultValue: '',
                    ...(fieldType === 'category' && field.options ? { options: field.options } : {}) // Only add options if category
                };
            });

            this.config.fields = configFields;
        } else {
            // Reset the query if no fields are available
            this.query = {
                condition: 'and',
                rules: []
            };
            this.config.fields = {};
        }
    }


    /**
     * Emits an updated query when conditions change.
     */
    onQueryChange(): void {
        this.conditionsChange.emit(this.query);
        this.isAnyFieldEmpty()
    }


    /* --------------------------------------------------- TEMPLATE HELPER -------------------------------------------------- */


    /**
     * Determines if the value field should be hidden based on the selected operator.
     */
    shouldHideValueField(operator: string): boolean {
        return operator === 'is null' || operator === 'is not null';
    }


    /**
     * Checks if any field in the query rules is empty (excluding null checks) and emits validation status.
     */
    isAnyFieldEmpty() {
        let isAnyFieldEmpty = this.query.rules.filter(rule => rule.value === '' && rule.operator !== 'is null' && rule.operator !== 'is not null').length > 0;
        this.filterBuilderValidation.emit(!isAnyFieldEmpty)
    }
}