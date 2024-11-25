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

* You should have received a copy of the GNU Affero General Public License
* along with this program. If not, see <https://www.gnu.org/licenses/>.
*/
import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { ReportService } from 'src/app/reporting/services/report.service';
import { ToastService } from 'src/app/layout/toast/toast.service';
import { catchError, Observable, tap, throwError, forkJoin, switchMap, of } from 'rxjs';
import { TypeService } from 'src/app/framework/services/type.service';
import { FileSaverService } from 'ngx-filesaver';
import { FileService } from 'src/app/export/export.service';
import { CollectionParameters } from 'src/app/services/models/api-parameter';
import { Location } from '@angular/common';
import { unparse } from 'papaparse';
import { Sort, SortDirection } from 'src/app/layout/table/table.types';

@Component({
    selector: 'app-run-report',
    templateUrl: './run-report.component.html',
    styleUrls: ['./run-report.component.scss']
})
export class RunReportComponent implements OnInit {
    public reportId: number;
    public reportResults: any[] = [];
    public loading = false;
    public types: any;
    public columns: Array<any> = [];
    public items: Array<any> = [];
    public typeId: number;
    public selectedFields: string[] = [];
    public mdsMode: string;
    public collectionFilterParameter: any[] = [];
    public sort = { order: -1, name: 'public_id' };
    public selectedObjectsIDs: number[] = [];


    //properties for pagination and search
    public filter: string;
    public displayedItems: any[];
    public limit: number = 10;
    public page: number = 1;
    public total: number = 0;
    /* --------------------------------------------------- LIFECYCLE METHODS -------------------------------------------------- */

    constructor(
        private route: ActivatedRoute,
        private reportService: ReportService,
        private toast: ToastService,
        private typeService: TypeService,
        private fileService: FileService,
        private fileSaverService: FileSaverService,
        private location: Location,
    ) { }

    /**
     * OnInit lifecycle hook.
     * Subscribes to route parameters and query parameters to initialize the component.
     * Loads types and report data, then processes the report results.
     */
    ngOnInit(): void {
        this.route.paramMap.pipe(
            switchMap((params) => {
                this.reportId = +params.get('id');
                if (this.reportId) {
                    return this.route.queryParams.pipe(
                        switchMap((queryParams) => {
                            this.typeId = +queryParams['type_id'];
                            this.selectedFields = queryParams['selected_fields'];
                            this.mdsMode = queryParams['mds_mode'];

                            // Ensure selectedFields is an array
                            if (Array.isArray(this.selectedFields)) {
                                // If it's already an array, do nothing
                            } else if (typeof this.selectedFields === 'string') {
                                try {
                                    // Parse the JSON string into an array
                                    this.selectedFields = JSON.parse(this.selectedFields);
                                } catch (e) {
                                    // If parsing fails, perhaps it's a comma-separated list
                                    // this.selectedFields = this.selectedFields.split(',');
                                }
                            } else {
                                // If selectedFields is undefined or null, set it to an empty array
                                this.selectedFields = [];
                            }

                            this.loading = true;
                            // Load types and run report concurrently
                            return forkJoin([
                                this.loadType(),
                                this.runReport(this.reportId)
                            ]);
                        })
                    );
                } else {
                    // If no reportId, return an observable of null
                    return of(null);
                }
            })
        ).subscribe({
            next: () => {
                this.processReportResults();
                this.loading = false;
            },
            error: (error) => {
                this.toast.error(error?.error?.message);
                this.loading = false;
            }
        });
    }

    /* --------------------------------------------------- API CALLS -------------------------------------------------- */


    /**
     * Executes a report by its ID and updates the report results.
     * @param id - The ID of the report to run.
     * @returns An observable of the report execution response.
     */
    private runReport(id: number): Observable<any> {
        return this.reportService.runReport(id).pipe(
            tap((response) => {
                this.reportResults = response;
            }),
            catchError((error) => {
                this.toast.error('Error running report');
                return throwError(() => error);
            })
        );
    }


    /**
     * Loads the type data for the specified typeId and updates the types property.
     * @returns An observable of the type retrieval response.
     */
    private loadType(): Observable<any> {
        return this.typeService.getType(this.typeId).pipe(
            tap((response) => {
                this.types = response;
            }),
            catchError((error) => {
                this.toast.error(error?.error?.message);
                return throwError(() => error);
            })
        );
    }

    /* --------------------------------------------------- DYNAMIC TABLE SETUP -------------------------------------------------- */


    private processReportResults(): void {
        const columnsMap = new Map<string, string>();
        this.columns = [];
        this.items = [];

        // Add 'Public ID' as the first column in the table
        this.columns.push({
            display: 'Public ID',
            name: 'public_id',
            data: 'public_id',
            sortable: true,
            style: { width: '120px', 'text-align': 'center' }
        });

        const type = this.types;
        if (!type) {
            this.toast.error(`Type with public_id ${this.typeId} not found`);
            return;
        }

        // Normalize selectedFields for consistent comparison
        const normalizedSelectedFields = this.selectedFields.map(f => f.trim().toLowerCase());

        // Build columns for selected fields
        for (const fieldName of this.selectedFields) {
            const typeField = type.fields.find(f => f.name === fieldName);
            if (!typeField) {
                continue;
            }
            const label = typeField.label;

            if (!columnsMap.has(fieldName)) {
                columnsMap.set(fieldName, label);
                this.columns.push({
                    display: label,
                    name: fieldName,
                    data: fieldName,
                    sortable: false
                });
            }
        }

        for (const reportResult of this.reportResults) {
            if (reportResult.type_id !== this.typeId) {
                continue;
            }


            const baseItem: any = {
                public_id: reportResult.public_id
            };

            const fieldValues = new Map<string, any>();

            // Process the fields
            for (const field of reportResult.fields) {
                const fieldName = field.name;
                const normalizedFieldName = fieldName.trim().toLowerCase();

                if (!normalizedSelectedFields.includes(normalizedFieldName)) {
                    continue;
                }

                let fieldValue = field.value;

                // Skip fields that are in MDS to avoid duplication
                const existsInMDS = reportResult.multi_data_sections && reportResult.multi_data_sections.some(mds =>
                    mds.values.some(mdsValue =>
                        mdsValue.data.some(d => d.name === fieldName)
                    )
                );

                if (existsInMDS) {
                    continue;
                }

                // Handle date formatting
                if (fieldValue && fieldValue.$date) {
                    fieldValue = new Date(fieldValue.$date).toLocaleDateString();
                }

                // Handle reference fields
                const typeField = type.fields.find(f => f.name === fieldName);
                if (typeField && typeField.type === 'ref' && fieldValue) {
                    fieldValue = `Ref ID: ${fieldValue}`;
                }

                fieldValues.set(fieldName, fieldValue);
            }

            // Now process the multi_data_sections
            if (this.mdsMode === 'ROWS') {

                const mdsValuesPerSection: any[][] = [];

                if (reportResult.multi_data_sections && reportResult.multi_data_sections.length > 0) {
                    // Collect MDS values per section
                    for (const mds of reportResult.multi_data_sections) {
                        const mdsValuesArray = [];
                        for (const mdsValue of mds.values) {
                            const mdsFields: { [key: string]: any } = {};
                            for (const mdsField of mdsValue.data) {
                                const fieldName = mdsField.name;
                                const normalizedFieldName = fieldName.trim().toLowerCase();

                                if (!normalizedSelectedFields.includes(normalizedFieldName)) {
                                    continue;
                                }

                                let fieldValue = mdsField.value;

                                // Handle date formatting
                                if (fieldValue && fieldValue.$date) {
                                    fieldValue = new Date(fieldValue.$date).toLocaleDateString();
                                }

                                // Handle reference fields
                                const typeField = type.fields.find(f => f.name === fieldName);
                                if (typeField && typeField.type === 'ref' && fieldValue) {
                                    fieldValue = `Ref ID: ${fieldValue}`;
                                }

                                mdsFields[fieldName] = fieldValue;
                            }
                            mdsValuesArray.push(mdsFields);
                        }
                        mdsValuesPerSection.push(mdsValuesArray);
                    }

                    // Compute the Cartesian product of MDS values
                    const cartesianProduct = this.computeCartesianProduct(mdsValuesPerSection);

                    // For each combination, create an item
                    for (const combination of cartesianProduct) {
                        const item = { ...baseItem };

                        // Copy over the field values
                        for (const [fieldName, fieldValue] of fieldValues.entries()) {
                            item[fieldName] = fieldValue;
                        }

                        // Merge the MDS fields from the combination
                        for (const mdsFields of combination) {
                            for (const [fieldName, fieldValue] of Object.entries(mdsFields)) {
                                item[fieldName] = fieldValue;
                            }
                        }

                        this.items.push(item);
                    }
                } else {
                    // If there are no MDS values, add the base item
                    const item = { ...baseItem };

                    // Copy over the field values
                    for (const [fieldName, fieldValue] of fieldValues.entries()) {
                        item[fieldName] = fieldValue;
                    }

                    this.items.push(item);
                }
            }

            else if (this.mdsMode === 'COLUMNS') {

                // Create a single item, combining MDS field values
                const item = { ...baseItem };

                // Copy over the field values
                for (const [fieldName, fieldValue] of fieldValues.entries()) {
                    item[fieldName] = fieldValue;
                }

                // For MDS fields, collect all values
                const mdsFieldValues = new Map<string, any[]>();

                if (reportResult.multi_data_sections && reportResult.multi_data_sections.length > 0) {
                    for (const mds of reportResult.multi_data_sections) {
                        for (const mdsValue of mds.values) {
                            for (const mdsField of mdsValue.data) {
                                const fieldName = mdsField.name;
                                const normalizedFieldName = fieldName.trim().toLowerCase();

                                // Only process if fieldName is in selectedFields
                                if (!normalizedSelectedFields.includes(normalizedFieldName)) {
                                    continue;
                                }

                                let fieldValue = mdsField.value;


                                // Handle date formatting
                                if (fieldValue && fieldValue.$date) {
                                    fieldValue = new Date(fieldValue.$date).toLocaleDateString();
                                }

                                // Handle reference fields
                                const typeField = type.fields.find(f => f.name === fieldName);
                                if (typeField && typeField.type === 'ref' && fieldValue) {
                                    fieldValue = `Ref ID: ${fieldValue}`;
                                }

                                if (!mdsFieldValues.has(fieldName)) {
                                    mdsFieldValues.set(fieldName, []);
                                }
                                mdsFieldValues.get(fieldName).push(fieldValue);
                            }
                        }
                    }
                }


                // Combine MDS field values using newline separator
                for (const [fieldName, values] of mdsFieldValues.entries()) {
                    item[fieldName] = values.join('\n');
                }

                // Only add the item if it has fields (other than public_id)
                if (Object.keys(item).length > 1) {
                    this.items.push(item);
                } else {
                    // console.warn(`Item for public_id ${reportResult.public_id} has no data to display.`);
                }
            }

            else {
                // Default behavior if mdsMode is not specified
                const item = { ...baseItem };

                // Copy over the field values
                for (const [fieldName, fieldValue] of fieldValues.entries()) {
                    item[fieldName] = fieldValue;
                }

                this.items.push(item);
            }
        }

        this.total = this.items.length;
        this.updateDisplayedItems();
    }


    /**
     * Computes the Cartesian product of an array of arrays.
     * @param arrays An array of arrays containing MDS values.
     * @returns An array of arrays representing all possible combinations.
     */
    private computeCartesianProduct(arrays: any[][]): any[][] {
        if (arrays.length === 0) {
            return [];
        }

        return arrays.reduce((accumulator, currentValue) => {
            const temp = [];
            for (const accItem of accumulator) {
                for (const currItem of currentValue) {
                    temp.push([...accItem, currItem]);
                }
            }
            return temp;
        }, [[]]);
    }

    /* --------------------------------------------------- SEARCH, SORTING, PAGINATION METHODS  -------------------------------------------------- */


    /**
     * Handles page change by updating the current page and refreshing the displayed items.
     * @param page - The new page number to navigate to.
     */
    public onPageChange(page: number): void {
        this.page = page;
        this.updateDisplayedItems();
    }


    /**
     * Handles changes in page size by updating the limit, resetting to the first page, and refreshing the displayed items.
     * @param limit - The new number of items per page.
     */
    public onPageSizeChange(limit: number): void {
        this.limit = limit;
        this.page = 1; // Reset to first page
        this.updateDisplayedItems();
    }


    /**
     * Handles sort changes by updating the sort criteria and refreshing the displayed items.
     * @param sort - The new sort configuration.
     */
    public onSortChange(sort: Sort): void {
        this.sort = sort;
        this.updateDisplayedItems();
    }


    /**
     * Handles search input changes by updating the filter, resetting to the first page, and refreshing the displayed items.
     * @param search - The search query or criteria.
     */
    public onSearchChange(search: any): void {
        this.filter = search || '';
        this.page = 1; // Reset to first page
        this.updateDisplayedItems();
    }


    /**
     * Updates the list of displayed items based on current filters, sorting, and pagination settings.
     * Applies search filters, sorts the items, and slices them according to the current page and limit.
     */
    private updateDisplayedItems(): void {
        let filteredItems = this.items;

        // Apply search filter
        if (this.filter) {
            const searchLower = this.filter.toLowerCase();
            filteredItems = filteredItems.filter(item => {
                return this.columns.some(column => {
                    const value = item[column.name];
                    return value && value.toString().toLowerCase().includes(searchLower);
                });
            });
        }

        // Update total after filtering
        this.total = filteredItems.length;

        // Apply sorting
        if (this.sort) {
            const sortColumn = this.sort.name;
            const sortOrder = this.sort.order === SortDirection.DESCENDING ? -1 : 1;
            filteredItems.sort((a, b) => {
                if (a[sortColumn] < b[sortColumn]) return -1 * sortOrder;
                if (a[sortColumn] > b[sortColumn]) return 1 * sortOrder;
                return 0;
            });
        }

        // Apply pagination
        const startIndex = (this.page - 1) * this.limit;
        const endIndex = startIndex + this.limit;
        this.displayedItems = filteredItems.slice(startIndex, endIndex);
    }



    /* --------------------------------------------------- EXPORT FILE METHODS -------------------------------------------------- */

    /**
     * Exports the report data using the specified format.
     */
    public exportingFiles() {
        const see = {
            extension: 'JsonExportFormat',
            label: 'csv',
            view: 'native'
        };

        const optional = {
            classname: see.extension,
            zip: false,
            metadata: undefined
        };

        const selectedObjectsIDs = this.reportResults.map(result => result.public_id);

        let exportFilter: any[];

        if (selectedObjectsIDs.length > 0) {
            exportFilter = [
                {
                    $match: {
                        public_id: {
                            $in: selectedObjectsIDs
                        }
                    }
                }
            ];
        } else {
            exportFilter = [
                {
                    $match: {
                        type_id: this.typeId
                    }
                }
            ];
        }

        const exportAPI: CollectionParameters = {
            filter: exportFilter,
            optional,
            order: this.sort.order,
            sort: this.sort.name
        };

        this.fileService.callExportRoute(exportAPI, see.view)
            .subscribe({
                next: (res) => {
                    if (res.body instanceof Blob) {
                        const reader = new FileReader();
                        reader.onload = () => {
                            const text = reader.result as string;
                            try {
                                const jsonData = JSON.parse(text);

                                let flattenedData = [];
                                jsonData.forEach(item => {
                                    const baseData = {
                                        public_id: String(item.object_id), // Convert ID to string
                                        active: String(item.active), // Convert boolean to string
                                        type_label: item.type_label
                                    };

                                    // Filter and add selected fields
                                    item.fields
                                        .filter(field => this.selectedFields.includes(field.name))
                                        .forEach(field => {
                                            let value = field.value;

                                            // Parse date fields
                                            if (value && typeof value === 'object' && '$date' in value) {
                                                value = new Date(value.$date).toLocaleDateString();
                                            }

                                            // Convert numeric values to strings with padding
                                            if (typeof value === 'number') {
                                                value = `'${String(value)}`; // Add single quote to treat as string in Excel
                                            }

                                            // Center-align password field values
                                            if (field.name.startsWith('password') && value) {
                                                const strValue = String(value);
                                                const padding = (20 - strValue.length) / 2; // Adjust 20 as needed
                                                value =
                                                    ' '.repeat(Math.floor(padding)) +
                                                    strValue +
                                                    ' '.repeat(Math.ceil(padding));
                                            }

                                            baseData[field.name] = value ?? '';
                                        });

                                    if (this.mdsMode === 'ROWS') {
                                        // Compute Cartesian product for MDS in ROWS mode
                                        const mdsValuesPerSection: any[][] = [];

                                        item.multi_data_sections.forEach(section => {
                                            const sectionValues = [];
                                            section.values.forEach(value => {
                                                const mdsFields: { [key: string]: any } = {};
                                                value.data
                                                    .filter(dataItem =>
                                                        this.selectedFields.includes(dataItem.name)
                                                    )
                                                    .forEach(dataItem => {
                                                        let fieldValue = dataItem.value;

                                                        // Parse date fields
                                                        if (
                                                            fieldValue &&
                                                            typeof fieldValue === 'object' &&
                                                            '$date' in fieldValue
                                                        ) {
                                                            fieldValue = new Date(
                                                                fieldValue.$date
                                                            ).toLocaleDateString();
                                                        }

                                                        // Convert numeric values to strings
                                                        if (typeof fieldValue === 'number') {
                                                            fieldValue = `'${String(fieldValue)}`;
                                                        }

                                                        // Center-align password field values
                                                        if (
                                                            dataItem.name.startsWith('password') &&
                                                            fieldValue
                                                        ) {
                                                            const strValue = String(fieldValue);
                                                            const padding =
                                                                (20 - strValue.length) / 2; // Adjust 20 as needed
                                                            fieldValue =
                                                                ' '.repeat(Math.floor(padding)) +
                                                                strValue +
                                                                ' '.repeat(Math.ceil(padding));
                                                        }

                                                        mdsFields[dataItem.name] = fieldValue ?? '';
                                                    });
                                                sectionValues.push(mdsFields);
                                            });
                                            mdsValuesPerSection.push(sectionValues);
                                        });

                                        // Compute Cartesian product
                                        const cartesianProduct = this.computeCartesianProduct(
                                            mdsValuesPerSection
                                        );

                                        // For each combination, create an item
                                        cartesianProduct.forEach(combination => {
                                            const row = { ...baseData };
                                            combination.forEach(mdsFields => {
                                                Object.entries(mdsFields).forEach(([key, value]) => {
                                                    row[key] = value;
                                                });
                                            });
                                            flattenedData.push(row);
                                        });
                                    } else {
                                        // Default COLUMNS mode
                                        const row = { ...baseData };

                                        // Add MDS fields in COLUMNS mode
                                        const mdsFieldValues = new Map<string, any[]>();
                                        item.multi_data_sections.forEach(section => {
                                            section.values.forEach(value => {
                                                value.data
                                                    .filter(dataItem =>
                                                        this.selectedFields.includes(dataItem.name)
                                                    )
                                                    .forEach(dataItem => {
                                                        let fieldValue = dataItem.value;

                                                        // Parse date fields
                                                        if (
                                                            fieldValue &&
                                                            typeof fieldValue === 'object' &&
                                                            '$date' in fieldValue
                                                        ) {
                                                            fieldValue = new Date(
                                                                fieldValue.$date
                                                            ).toLocaleDateString();
                                                        }

                                                        // Convert numeric values to strings
                                                        if (typeof fieldValue === 'number') {
                                                            fieldValue = `'${String(fieldValue)}`;
                                                        }

                                                        if (!mdsFieldValues.has(dataItem.name)) {
                                                            mdsFieldValues.set(dataItem.name, []);
                                                        }
                                                        mdsFieldValues
                                                            .get(dataItem.name)
                                                            .push(fieldValue ?? '');
                                                    });
                                            });
                                        });

                                        // Combine MDS field values with newline separator
                                        mdsFieldValues.forEach((values, key) => {
                                            row[key] = values.join('\n');
                                        });

                                        flattenedData.push(row);
                                    }
                                });

                                // Convert the flattened data to CSV
                                const csv = unparse(flattenedData, {
                                    quotes: false // Do not wrap fields in quotes
                                });

                                // Save the CSV file
                                const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
                                this.fileSaverService.save(blob, new Date().toISOString() + '.csv');
                            } catch (error) {
                                this.toast.error('Error parsing JSON or converting to CSV');
                            }
                        };
                        reader.onerror = () => {
                            this.toast.error('Error reading Blob data');
                        };
                        reader.readAsText(res.body);
                    } else {
                        this.toast.error('Unexpected response format');
                    }
                },
                error: () => {
                    this.toast.error('Error exporting report as CSV');
                }
            });
    }


    /* --------------------------------------------------- ACTION METHODS -------------------------------------------------- */


    /**
     * Navigates back to the previous page in the browser's history.
     */
    goBack(): void {
        this.location.back()
    }

    /**
     * Determines whether the export button should be disabled.
     * @returns `true` if there are items to export, otherwise `false`.
     */
    disableExportButton(): boolean {
        return this.items.length > 0;
    }
}