import { Component, Input, OnInit } from '@angular/core';
import { NgbActiveModal } from '@ng-bootstrap/ng-bootstrap';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { CmdbCategory } from '../../../../models/cmdb-category';
import { CategoryService, checkCategoryExistsValidator} from '../../../../services/category.service';
import { NgxSpinnerService } from 'ngx-spinner';

@Component({
  selector: 'cmdb-add-category-modal',
  templateUrl: './add-category-modal.component.html',
  styleUrls: ['./add-category-modal.component.scss']
})
export class AddCategoryModalComponent implements OnInit {

  public catAddForm: FormGroup;
  public categoryList: CmdbCategory[];

  constructor(public activeModal: NgbActiveModal, private spinner: NgxSpinnerService,
              private categoryService: CategoryService) {
    this.catAddForm = new FormGroup({
      name: new FormControl('', Validators.required),
      label: new FormControl('', Validators.required),
      parentID: new FormControl(null)
    });
  }

  ngOnInit(): void {
      this.catAddForm.get('name').setAsyncValidators(checkCategoryExistsValidator(this.categoryService));
      this.catAddForm.get('label').valueChanges.subscribe(value => {
        value = value == null ? '' : value;
        this.catAddForm.get('name').setValue(value.replace(/ /g, '-').toLowerCase());
        const newValue = this.catAddForm.get('name').value;
        this.catAddForm.get('name').setValue(newValue.replace(/[^a-z0-9 \-]/gi, '').toLowerCase());
        this.catAddForm.get('name').markAsDirty({onlySelf: true});
        this.catAddForm.get('name').markAsTouched({onlySelf: true});
      });
      this.categoryService.getCategoryList().subscribe((list: CmdbCategory[]) => {
          this.spinner.show();
          this.categoryList = list;
        }, error => {},
        () => this.spinner.hide());
  }

}
