import { Component, Input } from '@angular/core';
import { UntypedFormControl, UntypedFormGroup, Validators } from '@angular/forms';
import { NgbActiveModal } from '@ng-bootstrap/ng-bootstrap';
import { ReportCategoryService } from 'src/app/reporting/services/report-category.service';

@Component({
    selector: 'app-add-category-modal',
    templateUrl: './category-add-modal.component.html',
    styleUrls: ['./category-add-modal.component.scss']
})
export class AddCategoryModalComponent {
    @Input() predefined: boolean = false;

    public addCategoryForm: UntypedFormGroup = new UntypedFormGroup({
        name: new UntypedFormControl('', [Validators.required, Validators.minLength(3)])
    });

    constructor(public modal: NgbActiveModal, private categoryService: ReportCategoryService) { }

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
