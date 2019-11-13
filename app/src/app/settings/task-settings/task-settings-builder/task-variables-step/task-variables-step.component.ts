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

import { Component, Input, OnInit} from '@angular/core';
import { CmdbMode } from '../../../../framework/modes.enum';
import { FormArray, FormBuilder, FormControl, FormGroup, Validators } from '@angular/forms';
import { CmdbType } from '../../../../framework/models/cmdb-type';
import { TypeService } from '../../../../framework/services/type.service';

@Component({
  selector: 'cmdb-task-variables-step',
  templateUrl: './task-variables-step.component.html',
  styleUrls: ['./task-variables-step.component.scss']
})
export class TaskVariablesStepComponent implements OnInit {

  @Input()
  set preData(data: any) {
    if (data !== undefined) {
      if (data.variables) {
        // Create variables
        this.variableForm = this.formBuilder.group({
          variables: new FormArray([])
        });
        this.variableForm.removeControl('variables');
        const forArray: FormArray = this.formBuilder.array([]);
        let i = 0;
        while (i < data.variables.length) {
          forArray.push(this.formBuilder.group({
            name: new FormControl('', Validators.required),
            default: new FormControl('', Validators.required),
            templates: this.formBuilder.array([])
          }));
          i++;
        }

        // Create templates
        i = 0;
        while ( i < forArray.controls.length) {
          for (const item of data.variables[i].templates) {
            const control = forArray.controls[i].get('templates') as FormArray;
            control.push(this.createTemplate());
          }
          i++;
        }

        this.variableForm.addControl('variables', forArray);
        this.variableForm.patchValue(data);
      }
    }
  }

  @Input() public mode: CmdbMode;
  public typeList: CmdbType[] = [];
  public variableForm: FormGroup;
  readonly VARIABLES = 'variables';

  constructor(private formBuilder: FormBuilder, private typeService: TypeService) {}

  ngOnInit() {
    this.variableForm = this.formBuilder.group({
      variables: this.formBuilder.array([this.createVariable()])
    });
    this.typeService.getTypeList().subscribe((value: CmdbType[]) => this.typeList = value);
  }

  private createVariable(): FormGroup {
    return this.formBuilder.group({
      name: new FormControl('', Validators.required),
      default: new FormControl('', Validators.required),
      templates: this.formBuilder.array([this.createTemplate()])
    });
  }

  private createTemplate(): FormGroup {
    return this.formBuilder.group({
      type: new FormControl('', Validators.required),
      template: new FormControl('', Validators.required)
    });
  }

  private getVariableAsFormArray(): any {
    return this.variableForm.controls[this.VARIABLES] as FormArray;
  }

  public addVariable(): void {
    const control = this.getVariableAsFormArray();
    control.push(this.createVariable());
  }

  public addTemplate(event): void {
    const control = this.getVariableAsFormArray().at(event).get('templates') as FormArray;
    control.push(this.createTemplate());
  }

  public delVariable(index): void {
    const control = this.getVariableAsFormArray();
    control.removeAt(index);
  }

  public delTemplate(index, event): void {
    const control = this.getVariableAsFormArray().at(event).get('templates') as FormArray;
    control.removeAt(index);
  }
}
