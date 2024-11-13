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
import { Component, Input, OnInit } from '@angular/core';
import { UntypedFormControl, UntypedFormGroup, Validators } from '@angular/forms';
import { NgbActiveModal } from '@ng-bootstrap/ng-bootstrap';
import { ReportCategoryService } from 'src/app/reporting/services/report-category.service';

@Component({
    selector: 'app-add-category-modal',
    templateUrl: './category-add-modal.component.html',
    styleUrls: ['./category-add-modal.component.scss']
})
export class AddCategoryModalComponent implements OnInit {
    @Input() mode: 'add' | 'edit' | 'delete';
    @Input() categoryData: any = { name: '', predefined: false };

    public addCategoryForm: UntypedFormGroup;

    constructor(public modal: NgbActiveModal, private categoryService: ReportCategoryService) { }

    ngOnInit(): void {
        this.addCategoryForm = new UntypedFormGroup({
            name: new UntypedFormControl(this.categoryData.name, [Validators.required, Validators.minLength(3)])
        });
    }

    /**
     * Handles form submission based on the current mode.
     * Executes add, edit, or delete operations for categories.
     */
    public onSubmit(): void {
        if (this.mode === 'delete') {
            this.deleteCategory();
        } else if (this.addCategoryForm.valid) {
            const categoryData = {
                public_id: this.categoryData.public_id,
                name: this.addCategoryForm.value.name,
                predefined: this.categoryData.predefined
            };
            if (this.mode === 'add') {
                this.addCategory(categoryData);
            } else if (this.mode === 'edit') {
                this.updateCategory(categoryData);
            }
        }
    }

    /**
     * Adds a new category with the provided data.
     * Closes the modal on success or logs an error and dismisses the modal on failure.
     * @param categoryData - The data for the new category.
     */
    private addCategory(categoryData: { name: string; predefined: boolean }) {
        this.categoryService.createCategory(categoryData).subscribe(
            () => this.modal.close('success'),
            (error) => {
                console.error('Error creating category:', error);
                this.modal.dismiss('error');
            }
        );
    }

    /**
     * Updates an existing category with the provided data.
     * Closes the modal on success or logs an error and dismisses the modal on failure.
     * @param categoryData - The updated data for the category.
     */
    private updateCategory(categoryData: { public_id: number; name: string; predefined: boolean }) {
        this.categoryService.updateCategory(categoryData).subscribe(
            () => this.modal.close('updated'),
            (error) => {
                console.error('Error updating category:', error);
                this.modal.dismiss('error');
            }
        );
    }

    /**
     * Deletes the current category.
     * Closes the modal on success or logs an error and dismisses the modal on failure.
     */
    private deleteCategory() {
        this.categoryService.deleteCategory(this.categoryData.public_id).subscribe(
            () => this.modal.close('deleted'),
            (error) => {
                console.error('Error deleting category:', error);
                this.modal.dismiss('error');
            }
        );
    }
}
