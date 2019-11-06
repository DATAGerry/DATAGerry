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
import { ExternalSystemService } from '../../../services/external_system.service';
import {DndDropEvent, DropEffect} from "ngx-drag-drop";

@Component({
  selector: 'cmdb-task-destinations-step',
  templateUrl: './task-destinations-step.component.html',
  styleUrls: ['./task-destinations-step.component.scss']
})
export class TaskDestinationsStepComponent implements OnInit {

  @Input()
  set preData(data: any) {
    if (data !== undefined) {
      if (data.destination) {
        // Create destination
        this.destinationForm = this.formBuilder.group({
          destination: new FormArray([])
        });
        this.destinationForm.removeControl('destination');
        const forArray: FormArray = this.formBuilder.array([]);
        for (const source of data.destination) {
          forArray.push(this.formBuilder.group({
            className: new FormControl('', Validators.required),
            parameter: this.formBuilder.array([])
          }));
        }
        this.destinationForm.addControl('destination', forArray);
        this.destinationForm.patchValue(data);
        // Create parameter
        let i = 0;
        while ( i < forArray.controls.length) {
          for (let c = 0; c < data.destination[i].parameter.length; c++) {
            const control = forArray.controls[i].get('parameter') as FormArray;
            let required: boolean = false;
            let description: string = '';
            const classname = forArray.controls[i].get('className').value;
            if (classname !== '' && classname !== undefined) {
              this.externalService.getExternSytemParams(classname).subscribe(params => {
                this.externalSystemParams = params as [];
                required = params[c].required;
                description = params[c].description;
                control.push(this.createParameters('', description, required));
                this.destinationForm.addControl('destination', forArray);
                this.destinationForm.patchValue(data);
              });
            }
          }
          i++;
        }
        this.destinationForm.addControl('destination', forArray);
        this.destinationForm.patchValue(data);
      }
    }
  }

  @Input() public mode: CmdbMode;
  public MODES = CmdbMode;
  public externalSystemList: any[] = [];
  public externalSystemParams: any[] = [];
  public destinationForm: FormGroup;
  readonly DESTINATION = 'destination';

  constructor(private formBuilder: FormBuilder, private externalService: ExternalSystemService) {}

  ngOnInit() {
    this.destinationForm = this.formBuilder.group({
      destination: this.formBuilder.array([this.createDestination()])
    });

    this.externalService.getExternSytemList().subscribe(data => {
      this.externalSystemList = data;
    });
  }

  public getSystemParameters(className: string) {
    this.externalService.getExternSytemParams(className).subscribe(params => {
      this.externalSystemParams = params as [];
    });
  }

  private createDestination(): FormGroup {
    return this.formBuilder.group({
      className: new FormControl('', Validators.required),
      parameter: this.formBuilder.array([this.createParameters()])
    });
  }

  private createParameters(name = '', description = '', required = false): FormGroup {
    return this.formBuilder.group({
      name: new FormControl(name, Validators.required),
      value: new FormControl('', Validators.required),
      required: new FormControl(required, Validators.required),
      description: new FormControl(description, Validators.required)
    });
  }

  private getDestinationAsFormArray(): any {
    return this.destinationForm.controls[this.DESTINATION] as FormArray;
  }

  public addDestination(): void {
    const control = this.getDestinationAsFormArray();
    control.push(this.createDestination());
  }

  public addParameters(event): void {
    const control = this.getDestinationAsFormArray().at(event).get('parameter') as FormArray;
    control.push(this.createParameters());
  }

  public delDestination(index): void {
    const control = this.getDestinationAsFormArray();
    control.removeAt(index);
  }

  public delParameter(index, event): void {
    const control = this.getDestinationAsFormArray().at(event).get('parameter') as FormArray;
    control.removeAt(index);
  }

  public onDraggedParameter(item: DndDropEvent, control: any, effect: DropEffect) {
    control.get('name').setValue(item.data.name);
    control.get('description').setValue(item.data.description);
    control.get('required').setValue(item.data.required);
    control.get('value').setValue(item.data.default);
  }

  public onDraggedSystem(item: DndDropEvent, control: any, effect: DropEffect) {
    control.get('className').setValue(item.data);
  }
}
