/*
* DATAGERRY - OpenSource Enterprise CMDB
* Copyright (C) 2019 NETHINKS GmbH
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
import { Component, EventEmitter, Input, OnChanges, OnDestroy, OnInit, Output, SimpleChanges } from '@angular/core';
import { FormArray, FormControl, FormGroup, Validators } from '@angular/forms';
import { Subscription } from 'rxjs';
import { CmdbMode } from '../../modes.enum';
import { CmdbCategory } from '../../models/cmdb-category';
import { CmdbType } from '../../models/cmdb-type';
import { CategoryService, checkCategoryExistsValidator } from '../../services/category.service';
import { DndDropEvent, DropEffect } from 'ngx-drag-drop';

@Component({
  selector: 'cmdb-category-form',
  templateUrl: './category-form.component.html',
  styleUrls: ['./category-form.component.scss']
})
export class CategoryFormComponent implements OnInit, OnChanges, OnDestroy {

  /**
   * Modification mode for the form and validation.
   * Default is always: CREATE
   */
  @Input() public mode: CmdbMode = CmdbMode.Create;
  /**
   * Preset data from existing category.
   * Will be ignored if mode is CREATE.
   */
  @Input() public category: CmdbCategory;

  /**
   * Inner category holder for assignments
   */
  private $category: CmdbCategory = new CmdbCategory();

  /**
   * Event call if form is valid and submit button was pressed.
   * Data will be a category instance.
   */
  @Output() public submitEmitter: EventEmitter<CmdbCategory> = new EventEmitter<CmdbCategory>();
  /**
   * Event which will show the current validation status of the form.
   */
  @Output() public validationEmitter: EventEmitter<boolean> = new EventEmitter<boolean>();

  /**
   * Subscription if any value of the form has changed.
   * Triggers the validationEmitter output.
   */
  private valueChangeSubscription: Subscription = new Subscription();
  /**
   *
   */
  private categoryServiceSubscription: Subscription = new Subscription();


  public categoryForm: FormGroup;
  public categories: CmdbCategory[] = [];

  @Input() public unAssignedTypes: CmdbType[] = [];
  @Input() public assignedTypes: CmdbType[] = [];

  public effect: DropEffect = 'move';
  public readonly fallBackIcon = 'far fa-folder-open';

  /**
   * Category form constructor - Inits the category form
   */
  public constructor(private categoryService: CategoryService) {
    this.categoryForm = new FormGroup({
      name: new FormControl('', Validators.required),
      label: new FormControl(''),
      meta: new FormGroup({
        icon: new FormControl(null),
        order: new FormControl(null)
      }),
      parent: new FormControl(null),
      types: new FormArray([])
    });
  }

  public ngOnInit(): void {
    if (this.mode === CmdbMode.Create) {
      this.name.setAsyncValidators(checkCategoryExistsValidator(this.categoryService));
    } else if (this.mode === CmdbMode.Edit) {
      this.name.disable({ onlySelf: true });
    }
    this.categoryServiceSubscription = this.categoryService.getCategoryList().subscribe((categories: CmdbCategory[]) => {
      this.categories = categories;
    });

    this.valueChangeSubscription = this.categoryForm.statusChanges.subscribe(() => {
      this.validationEmitter.emit(this.categoryForm.valid);
    });

  }

  public ngOnChanges(changes: SimpleChanges): void {
    if (changes.category !== undefined && changes.category.currentValue !== undefined && (
      changes.category.previousValue !== changes.category.currentValue
    )) {
      this.$category = this.category;
      this.categoryForm.patchValue(this.$category);
    }
  }

  public ngOnDestroy(): void {
    this.valueChangeSubscription.unsubscribe();
    this.categoryServiceSubscription.unsubscribe();
    this.submitEmitter.unsubscribe();
  }

  public get name(): FormControl {
    return this.categoryForm.get('name') as FormControl;
  }

  public get label(): FormControl {
    return this.categoryForm.get('label') as FormControl;
  }

  public get meta(): FormGroup {
    return this.categoryForm.get('meta') as FormGroup;
  }

  public get icon(): FormControl {
    return this.meta.get('icon') as FormControl;
  }

  public onIconSelect(value: string): void {
    this.icon.setValue(value);
  }

  public get parent(): FormControl {
    return this.categoryForm.get('parent') as FormControl;
  }

  public get types(): FormArray {
    return this.categoryForm.get('types') as FormArray;
  }

  public clickRemoveAssignedType(item: CmdbType): void {
    const index: number = this.assignedTypes.indexOf(item);
    this.assignedTypes.splice(index, 1);
    this.unAssignedTypes.push(item);
    this.types.removeAt(index);
  }

  public clickReset() {
    this.unAssignedTypes = this.unAssignedTypes.concat(this.assignedTypes);
    this.assignedTypes = [];
  }

  public onDragStart(event: DragEvent) {
    console.log('Drag started!');
    console.log(event);
  }

  public onDragged(item: any, list: any[], effect: DropEffect) {
    if (effect === 'move') {
      const index = list.indexOf(item);
      list.splice(index, 1);
    }
  }

  public onDrop(event: DndDropEvent, list?: any[]) {
    let index = event.index;
    if (typeof index === 'undefined') {
      index = list.length;
    }
    list.splice(index, 0, event.data);
    this.types.insert(index, new FormControl(event.data.public_id));
  }

  public onSubmit(): void {
    this.categoryForm.markAllAsTouched();
    if (this.categoryForm.valid) {
      this.$category = Object.assign(this.$category, this.categoryForm.getRawValue() as CmdbCategory);
      this.submitEmitter.emit(this.$category);
    }
  }


}
