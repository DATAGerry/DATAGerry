/*
* DATAGERRY - OpenSource Enterprise CMDB
* Copyright (C) 2019 - 2021 NETHINKS GmbH
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

import {
  ChangeDetectionStrategy,
  Component, DoCheck,
  Input, IterableDiffer, IterableDiffers,
  OnDestroy,
  OnInit,
} from '@angular/core';
import { AbstractControl, FormControl, FormGroup, Validators } from '@angular/forms';
import { TypeBuilderStepComponent } from '../type-builder-step.component';
import { ReplaySubject } from 'rxjs';
import { CmdbType } from '../../../models/cmdb-type';
import { takeUntil } from 'rxjs/operators';

function occurrences(s, subString): number {
  s += '';
  subString += '';
  if (subString.length <= 0) {
    return (s.length + 1);
  }

  let n = 0;
  let pos = 0;

  while (true) {
    pos = s.indexOf(subString, pos);
    if (pos >= 0) {
      ++n;
      pos += 1;
    } else {
      break;
    }
  }
  return n;
}

@Component({
  selector: 'cmdb-type-meta-step',
  templateUrl: './type-meta-step.component.html',
  styleUrls: ['./type-meta-step.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class TypeMetaStepComponent extends TypeBuilderStepComponent implements DoCheck, OnInit, OnDestroy {

  private subscriber: ReplaySubject<void> = new ReplaySubject<void>();

  public summaryForm: FormGroup;
  public externalsForm: FormGroup;

  public hasInter: boolean = false;

  public fields: Array<any> = [];
  private iterableDiffer: IterableDiffer<any>;

  @Input('typeInstance')
  public set TypeInstance(instance: CmdbType) {
    if (instance) {
      this.typeInstance = instance;
      // this.summaryForm.patchValue(instance.render_meta.summary); // TODO: Fields -> Name
      this.fields = this.typeInstance.fields;
      this.externalsForm.get('name').setValidators(this.listNameValidator());
    }
  }

  constructor(private iterableDiffers: IterableDiffers) {
    super();
    this.iterableDiffer = iterableDiffers.find([]).create(null);

    this.summaryForm = new FormGroup({
      fields: new FormControl('', Validators.required)
    });

    this.externalsForm = new FormGroup({
      name: new FormControl('', [Validators.required]),
      label: new FormControl('', Validators.required),
      icon: new FormControl(''),
      href: new FormControl('', [Validators.required]),
      fields: new FormControl('')
    });
  }

  public ngOnDestroy(): void {
    this.subscriber.next();
    this.subscriber.complete();
  }

  public get external_name() {
    return this.externalsForm.get('name');
  }

  public get external_label() {
    return this.externalsForm.get('label');
  }

  public listNameValidator() {
    return (control: AbstractControl): { [key: string]: any } | null => {
      const nameInList = this.typeInstance.render_meta.externals.find(el => el.name === control.value);
      return nameInList ? { nameAlreadyTaken: { value: control.value } } : null;
    };
  }

  public ngOnInit(): void {

    this.externalsForm.get('name').valueChanges.pipe(takeUntil(this.subscriber)).subscribe(val => {
      if (this.externalsForm.get('name').value !== null) {
        this.externalsForm.get('label').setValue(val.charAt(0).toUpperCase() + val.toString().slice(1));
        this.externalsForm.get('label').markAsDirty({ onlySelf: true });
        this.externalsForm.get('label').markAsTouched({ onlySelf: true });
      }
    });

    this.externalsForm.get('href').valueChanges.pipe(takeUntil(this.subscriber)).subscribe((href: string) => {
      this.hasInter = occurrences(href, '{}') > 0;
    });
  }

  public addExternal() {
    this.typeInstance.render_meta.externals.push(this.externalsForm.value);
    this.externalsForm.reset();
    this.externalsForm.get('icon').setValue('fas fa-external-link-alt');
  }

  public editExternal(data) {
    const rawExternalData = this.typeInstance.render_meta.externals[this.typeInstance.render_meta.externals.indexOf(data)];
    this.externalsForm.reset();
    this.deleteExternal(data);
    this.externalsForm.patchValue(rawExternalData);
  }

  public deleteExternal(data) {
    const index: number = this.typeInstance.render_meta.externals.indexOf(data);
    if (index !== -1) {
      this.typeInstance.render_meta.externals.splice(index, 1);
    }
  }

  public ngDoCheck(): void {
    const changes = this.iterableDiffer.diff(this.typeInstance.fields);
    if (changes) {
      this.fields = [...this.typeInstance.fields];
    }
  }


}
