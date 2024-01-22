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

import { Component, Input, OnDestroy, OnInit } from '@angular/core';
import { CmdbMode } from '../../../framework/modes.enum';
import { UntypedFormArray, UntypedFormBuilder, UntypedFormControl, UntypedFormGroup, Validators } from '@angular/forms';
import { ExternalSystemService } from '../../../settings/services/external-system.service';
import { DndDropEvent, DropEffect } from 'ngx-drag-drop';
import { ExportdJobBaseStepComponent } from '../exportd-job-base-step.component';
import { ReplaySubject } from 'rxjs';
import { takeUntil } from 'rxjs/operators';


@Component({
  selector: 'cmdb-task-destinations-step',
  templateUrl: './exportd-job-destinations-step.component.html',
  styleUrls: ['./exportd-job-destinations-step.component.scss']
})
export class ExportdJobDestinationsStepComponent extends ExportdJobBaseStepComponent implements OnInit, OnDestroy {

  private subscriber: ReplaySubject<void> = new ReplaySubject<void>();

  @Input()
  set preData(data: any) {
    if (data !== undefined) {
      if (data.destination) {
        // Create destination
        this.destinationForm = this.formBuilder.group({
          destination: new UntypedFormArray([])
        });
        this.destinationForm.removeControl('destination');
        const forArray: UntypedFormArray = this.formBuilder.array([]);
        for (const source of data.destination) {
          forArray.push(this.formBuilder.group({
            className: new UntypedFormControl('', Validators.required),
            parameter: this.formBuilder.array([])
          }));
        }
        this.destinationForm.addControl('destination', forArray);
        this.destinationForm.patchValue(data);
        // Create parameter
        let i = 0;
        while (i < forArray.controls.length) {
          for (let c = 0; c < data.destination[i].parameter.length; c++) {
            const control = forArray.controls[i].get('parameter') as UntypedFormArray;
            let required: boolean = false;
            let description: string = '';
            const classname = forArray.controls[i].get('className').value;
            if (classname !== '' && classname !== undefined) {
              this.externalService.getExternSystemParams(classname).subscribe(params => {
                required = params[c].required;
                description = params[c].description;
                control.push(this.createParameters('', '', description, required));
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
  public externalSystemList: any[] = [];
  public externalSystems: any[] = [];
  public destinationForm: UntypedFormGroup;
  readonly DESTINATION = 'destination';

  constructor(private formBuilder: UntypedFormBuilder, private externalService: ExternalSystemService) {
    super();
  }

  public ngOnInit(): void {
    this.destinationForm = this.formBuilder.group({
      destination: this.formBuilder.array([this.createDestination()])
    });

    this.externalService.getExternSystemList().pipe(takeUntil(this.subscriber)).subscribe(data => {
        this.externalSystemList = data;
      }, error => {
      },
      () => {
        for (const className of this.externalSystemList) {
          this.externalService.getExternSystemParams(className).pipe(takeUntil(this.subscriber)).subscribe(params => {
            this.externalSystems.push({ name: className, parameter: params });
          });
        }
      });
  }

  public ngOnDestroy(): void {
    this.subscriber.next();
    this.subscriber.complete();
  }

  private createDestination(): UntypedFormGroup {
    return this.formBuilder.group({
      className: new UntypedFormControl('', Validators.required),
      parameter: this.formBuilder.array([this.createParameters()])
    });
  }

  private createParameters(name = '', value = '', description = '', required = false): UntypedFormGroup {
    return this.formBuilder.group({
      name: new UntypedFormControl(name, Validators.required),
      value: new UntypedFormControl(value, Validators.required),
      required: new UntypedFormControl(required, Validators.required),
      description: new UntypedFormControl(description, Validators.required)
    });
  }

  private getDestinationAsFormArray(): any {
    return this.destinationForm.controls[this.DESTINATION] as UntypedFormArray;
  }

  public addDestination(): void {
    const control = this.getDestinationAsFormArray();
    control.push(this.createDestination());
  }

  public addParameters(event): void {
    const control = this.getDestinationAsFormArray().at(event).get('parameter') as UntypedFormArray;
    control.push(this.createParameters());
  }

  public delDestination(index): void {
    const control = this.getDestinationAsFormArray();
    control.removeAt(index);
  }

  public delParameter(index, event): void {
    const control = this.getDestinationAsFormArray().at(event).get('parameter') as UntypedFormArray;
    control.removeAt(index);
  }

  public onDraggedParameter(item: DndDropEvent, control: any, effect: DropEffect) {
    control.get('name').setValue(item.data.name);
    control.get('description').setValue(item.data.description);
    control.get('required').setValue(item.data.required);
    control.get('value').setValue(item.data.default);
  }

  public onDraggedSystem(item: DndDropEvent, control: any, index, effect: DropEffect) {
    control.get('className').setValue(item.data.name);
    let externalSystemParams = [];
    this.externalService.getExternSystemParams(item.data.name).pipe(takeUntil(this.subscriber)).subscribe(params => {
        externalSystemParams = params as [];
      }, error => console.log(error),
      () => {
        const controlArray = this.getDestinationAsFormArray().at(index).get('parameter') as UntypedFormArray;
        controlArray.clear();
        for (const param of externalSystemParams) {
          controlArray.push(this.createParameters(param.name, param.default, param.description, param.required));
        }
      });
  }
}
