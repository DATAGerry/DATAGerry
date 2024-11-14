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
import { Component, OnInit, OnDestroy } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { ReportCategoryService } from 'src/app/reporting/services/report-category.service';
import { TypeService } from 'src/app/framework/services/type.service';
import { ReplaySubject } from 'rxjs';
import { takeUntil } from 'rxjs/operators';
import { ReportService } from 'src/app/reporting/services/report.service';
import { ToastService } from 'src/app/layout/toast/toast.service';

@Component({
    selector: 'app-create-report',
    templateUrl: './create-report.component.html',
    styleUrls: ['./create-report.component.scss']
})
export class CreateReportComponent implements OnInit, OnDestroy {
    public createReportForm: FormGroup;
    public categories = [];
    public types = [];
    public fields = [];
    public typeLoading = false;
    private unsubscribe$ = new ReplaySubject<void>(1);
    public conditions: any = {}; // Holds the conditions from FilterBuilderComponent


    /* --------------------------------------------------- LIFECYCLE METHODS -------------------------------------------------- */


    constructor(
        private fb: FormBuilder,
        private categoryService: ReportCategoryService,
        private typeService: TypeService,
        private reportService: ReportService,
        private toast: ToastService

    ) { }


    ngOnInit(): void {
        this.createReportForm = this.fb.group({
            name: ['', [Validators.required, Validators.minLength(3)]],
            category: [null, Validators.required],
            type: [null, Validators.required],
            fields: [[]]
        });

        this.loadCategories();
        this.loadTypes();

        // Subscribe to type change and load corresponding fields
        this.createReportForm.get('type').valueChanges
            .pipe(takeUntil(this.unsubscribe$))
            .subscribe((typeId) => {
                this.loadFieldsForType(typeId);
            });
    }


    ngOnDestroy(): void {
        this.unsubscribe$.next();
        this.unsubscribe$.complete();
    }

    /* --------------------------------------------------- LOADING FROM API -------------------------------------------------- */


    /**
     * Loads the list of categories with default parameters.
     * Updates the categories array or logs an error if loading fails.
     */
    private loadCategories(): void {
        const params = { limit: 0, page: 1, sort: 'public_id', order: 1 };
        this.categoryService.getAllCategories(params).pipe(takeUntil(this.unsubscribe$)).subscribe(
            (response) => {
                this.categories = response.results;
            },
            (error) => console.error('Error loading categories:', error)
        );
    }


    /**
     * Loads the list of types with default parameters.
     * Updates the types array and loading state or logs an error if loading fails.
     */
    private loadTypes(): void {
        this.typeLoading = true;
        const params = { limit: 0, page: 1, sort: 'public_id', order: 1 };
        this.typeService.getTypes(params).pipe(takeUntil(this.unsubscribe$)).subscribe(
            (response) => {
                this.types = response.results;
                this.typeLoading = false;
            },
            (error) => {
                console.error('Error loading types:', error);
                this.typeLoading = false;
            }
        );
    }


    /**
     * Loads fields for the specified type ID if fields are available.
     * Updates the fields array based on the selected type.
     * @param typeId - The ID of the type to load fields for.
     */
    private loadFieldsForType(typeId: number): void {
        const selectedType = this.types.find((type) => type.public_id === typeId);
        if (selectedType && selectedType.fields && selectedType.fields.length > 0) {
            this.fields = selectedType.fields;
        } else {
            this.fields = [];
        }
    }

    /* --------------------------------------------------- ACTION METHODS -------------------------------------------------- */


    /**
     * Updates the conditions based on changes from the FilterBuilderComponent.
     */
    onConditionsChange(conditions: any): void {
        // Receive conditions from FilterBuilderComponent
        this.conditions = conditions;
        console.log('conditions', this.conditions)
    }

    /**
     * Submits the report form if valid, sending data to the report service for creation.
     */
    onSubmit(): void {
        if (this.createReportForm.valid) {
            const formValues = this.createReportForm.value;

            const reportData = {
                report_category_id: formValues.category,
                name: formValues.name,
                type_id: formValues.type,
                selected_fields: formValues.fields,
                conditions: this.conditions,
                report_query: {}, // Empty as required by backend
                predefined: false
            };

            this.reportService.createReport(reportData).subscribe({
                next: (response) => {
                    console.log('Report created successfully:', response);
                },
                error: (error) => {
                    this.toast.error(error?.error?.message)
                    console.error('Error creating report:', error);
                },
                complete: () => {
                    console.log('Rprocess completed.');
                }
            });

        }
    }
}
