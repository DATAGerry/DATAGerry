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
    @Input() predefined: boolean = false;

    public addCategoryForm: UntypedFormGroup;

    constructor(public modal: NgbActiveModal, private categoryService: ReportCategoryService) { }

    ngOnInit(): void {
        this.addCategoryForm = new UntypedFormGroup({
            name: new UntypedFormControl('', [Validators.required, Validators.minLength(3)])
        });
    }

    public get name() {
        return this.addCategoryForm.get('name');
    }

    public onSubmit(): void {
        if (this.addCategoryForm.valid) {
            const categoryData = { name: this.name.value, predefined: this.predefined };
            this.categoryService.createCategory(categoryData).subscribe(
                () => {
                    this.modal.close('success');
                },
                (error) => {
                    console.error('Error creating category:', error);
                    this.modal.dismiss('error');
                }
            );
        }

    }
}
