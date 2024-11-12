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
import { Component, OnInit, OnDestroy, TemplateRef, ViewChild } from '@angular/core';

import { ReplaySubject } from 'rxjs';
import { takeUntil } from 'rxjs/operators';
import { ReportCategoryService } from 'src/app/reporting/services/report-category.service';
import { CollectionParameters } from 'src/app/services/models/api-parameter';
import { APIGetMultiResponse } from 'src/app/services/models/api-response';
import { AddCategoryModalComponent } from '../category-add-modal/category-add-modal.component';
import { NgbModal } from '@ng-bootstrap/ng-bootstrap';

@Component({
    selector: 'app-category-overview',
    templateUrl: './category-overview.component.html',
    styleUrls: ['./category-overview.component.scss']
})
export class CategoryOverviewComponent implements OnInit, OnDestroy {
    private unsubscribe$ = new ReplaySubject<void>(1);
    public categories: Array<any> = [];
    public totalCategories: number = 0;
    public loading = false;

    @ViewChild('actionsTemplate', { static: true }) actionsTemplate: TemplateRef<any>;

    public columns: Array<any>;

    /* --------------------------------------------------- LIFE CYCLE --------------------------------------------------- */

    constructor(
        private categoryService: ReportCategoryService,
        private modalService: NgbModal) { }


    ngOnInit(): void {
        this.columns = [
            { display: 'Public ID', name: 'public_id', data: 'public_id', sortable: true, style: { width: '120px', 'text-align': 'center' } },
            { display: 'Name', name: 'name', data: 'name', sortable: true, style: { width: 'auto', 'text-align': 'center' } },
            { display: 'Actions', name: 'actions', template: this.actionsTemplate, sortable: false, style: { width: '100px', 'text-align': 'center' } }
        ];

        this.loadCategories();
    }

    ngOnDestroy(): void {
        this.unsubscribe$.next();
        this.unsubscribe$.complete();
    }


    /* --------------------------------------------------- REPORT CATEGORY API -------------------------------------------------- */

    /**
     * Loads the list of categories with specified parameters.
     */
    private loadCategories(): void {
        this.loading = true;
        const params: CollectionParameters = {
            filter: {},
            limit: 10,
            sort: 'public_id',
            order: 1,
            page: 1
        };
        this.categoryService.getAllCategories(params).pipe(takeUntil(this.unsubscribe$)).subscribe(
            (response: APIGetMultiResponse<any>) => {
                this.categories = response.results;
                this.totalCategories = response.total;
                this.loading = false;
            }
        );
    }

    public editCategory(id: number): void {
        console.log('Edit category with ID:', id);
    }

    /**
     * Deletes a category by ID after user confirmation.
     * Reloads the category list on successful deletion, or logs an error if deletion fails.
     * @param id - The ID of the category to delete.
     */
    public deleteCategory(id: number): void {
        if (confirm('Are you sure you want to delete this category?')) {
            this.categoryService.deleteCategory(id).pipe(takeUntil(this.unsubscribe$)).subscribe(
                () => {
                    alert('Category deleted successfully');
                    this.loadCategories(); // Reload categories after deletion
                },
                error => {
                    console.error('Error deleting category:', error);
                }
            );
        }
    }


    /* ------------------------------------------------ REST OF THE FUNCTIONS ------------------------------------------------ */

    /**
     * Opens the Add Category modal and handles the result.
     * Reloads categories on success and shows an error toast on failure.
     */
    public openAddCategoryModal(): void {
        const modalRef = this.modalService.open(AddCategoryModalComponent, { size: 'lg' });
        modalRef.result.then(
            (result) => {
                if (result === 'success') {
                    this.loadCategories();
                }
            },
            (error) => { }
        );
    }

}
