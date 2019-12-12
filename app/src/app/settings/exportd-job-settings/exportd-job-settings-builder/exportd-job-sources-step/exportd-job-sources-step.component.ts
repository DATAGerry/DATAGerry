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
* along with this program.  If not, see <https://www.gnu.org/licenses/>.
*/

import {Component, Input, OnInit} from '@angular/core';
import {FormArray, FormBuilder, FormControl, FormGroup, Validators} from '@angular/forms';
import {CmdbMode} from '../../../../framework/modes.enum';
import {CmdbType} from '../../../../framework/models/cmdb-type';
import {TypeService} from '../../../../framework/services/type.service';


@Component({
  selector: 'cmdb-task-sources-step',
  templateUrl: './exportd-job-sources-step.component.html',
  styleUrls: ['./exportd-job-sources-step.component.scss']
})
export class ExportdJobSourcesStepComponent implements OnInit {

  @Input()
  set preData(data: any) {
    if (data !== undefined) {
      if (data.sources) {
        // Create sources
        this.sourcesForm = this.formBuilder.group({
          sources: new FormArray([])
        });
        this.sourcesForm.removeControl('sources');
        const forArray: FormArray = this.formBuilder.array([]);
        for (const source of data.sources) {
          forArray.push(this.formBuilder.group({
            type_id: new FormControl('', Validators.required),
            condition: this.formBuilder.array([])
          }));
        }

        // Create condition
        let i = 0;
        while ( i < forArray.controls.length) {
          for (const item of data.sources[i].condition) {
            const control = forArray.controls[i].get('condition') as FormArray;
            control.push(this.createCondition());
          }
          i++;
        }

        this.sourcesForm.addControl('sources', forArray);
        this.sourcesForm.patchValue(data);
      }
    }
  }

  @Input() public mode: CmdbMode;
  public typeList: CmdbType[] = [];
  public operators: any[] = ['!=', '=='];
  public sourcesForm: FormGroup;
  readonly SOURCES = 'sources';

  constructor(private formBuilder: FormBuilder, private typeService: TypeService) {}

  ngOnInit() {
    this.sourcesForm = this.formBuilder.group({
      sources: this.formBuilder.array([this.createSource()])
    });
    this.typeService.getTypeList().subscribe((value: CmdbType[]) => this.typeList = value);

    if (this.mode === CmdbMode.Create) {
      this.delCondition(0, 0);
    }
  }

  public getFields(item: any) {
    try {
      return this.typeService.findType(item).fields;
    } catch (e) {
      return [];
    }
  }

  private createSource(): FormGroup {
    return this.formBuilder.group({
      type_id: new FormControl(null, Validators.required),
      condition: this.formBuilder.array([this.createCondition()])
    });
  }

  private createCondition(): FormGroup {
    return this.formBuilder.group({
      name: new FormControl('', Validators.required),
      value: new FormControl('', Validators.required),
      operator: new FormControl('', Validators.required)
    });
  }

  private getSourceAsFormArray(): any {
    return this.sourcesForm.controls[this.SOURCES] as FormArray;
  }

  public addSource(): void {
    const control = this.getSourceAsFormArray();
    control.push(this.createSource());
  }

  public addCondition(event): void {
    const control = this.getSourceAsFormArray().at(event).get('condition') as FormArray;
    control.push(this.createCondition());
  }

  public delSource(index): void {
    const control = this.getSourceAsFormArray();
    control.removeAt(index);
  }

  public delCondition(index, event): void {
    const control = this.getSourceAsFormArray().at(event).get('condition') as FormArray;
    control.removeAt(index);
  }
}
