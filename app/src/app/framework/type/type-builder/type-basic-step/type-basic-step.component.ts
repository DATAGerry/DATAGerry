/*
* DATAGERRY - OpenSource Enterprise CMDB
* Copyright (C) 2023 becon GmbH
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

import { Component, Input, OnDestroy, OnInit } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { checkTypeExistsValidator, TypeService } from '../../../services/type.service';
import { CmdbMode } from '../../../modes.enum';
import { ReplaySubject } from 'rxjs';
import { TypeBuilderStepComponent } from '../type-builder-step.component';
import { takeUntil } from 'rxjs/operators';
import { CmdbType } from '../../../models/cmdb-type';


/**
 * Type builder step for basic type information.
 */
@Component({
  selector: 'cmdb-type-basic-step',
  templateUrl: './type-basic-step.component.html',
  styleUrls: ['./type-basic-step.component.scss'],
})
export class TypeBasicStepComponent extends TypeBuilderStepComponent implements OnInit, OnDestroy {

  private subscriber: ReplaySubject<void> = new ReplaySubject<void>();
  public form: FormGroup;

  @Input('typeInstance')
  public set TypeInstance(instance: CmdbType) {
    if (instance) {
      this.typeInstance = instance;
      this.form.patchValue({
        name: this.typeInstance.name,
        label: this.typeInstance.label,
        description: this.typeInstance.description,
        active: this.typeInstance.active,
        icon: this.typeInstance.render_meta.icon
      });
    }
  }

  constructor(private typeService: TypeService) {
    super();
    this.form = new FormGroup({
      name: new FormControl('', Validators.required),
      label: new FormControl('', Validators.required),
      description: new FormControl(''),
      active: new FormControl(true),
      icon: new FormControl('fa fa-cube')
    });
  }

  public ngOnInit(): void {
    if (this.mode === CmdbMode.Create) {
      this.form.get('name').setAsyncValidators(checkTypeExistsValidator(this.typeService));
    } else if (this.mode === CmdbMode.Edit) {
      this.form.markAllAsTouched();
    }
    this.form.valueChanges.pipe(takeUntil(this.subscriber)).subscribe((changes: any) => {
      this.assign(changes);
    });
    this.form.statusChanges.pipe(takeUntil(this.subscriber)).subscribe(() => {
      this.validateChange.emit(this.form.valid);
      this.valid = this.form.valid;
    });
  }

  public assign(changes): void {
    this.typeInstance.name = changes.name;
    this.typeInstance.label = changes.label;
    this.typeInstance.description = changes.description;
    this.typeInstance.active = changes.active;
    this.typeInstance.render_meta.icon = changes.icon;
  }

  public get icon(): FormControl {
    return this.form.get('icon') as FormControl;
  }

  public get name(): FormControl {
    return this.form.get('name') as FormControl;
  }

  public get label(): FormControl {
    return this.form.get('label') as FormControl;
  }

  public get description(): FormControl {
    return this.form.get('description') as FormControl;
  }

  public ngOnDestroy(): void {
    this.subscriber.next();
    this.subscriber.complete();
  }

}
