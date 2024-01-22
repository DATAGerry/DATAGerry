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
import { UntypedFormArray, UntypedFormBuilder, UntypedFormControl, UntypedFormGroup, Validators } from '@angular/forms';
import { CmdbMode } from '../../../framework/modes.enum';
import { CmdbType } from '../../../framework/models/cmdb-type';
import { TypeService } from '../../../framework/services/type.service';
import { BehaviorSubject, Observable, ReplaySubject, Subscription } from 'rxjs';
import { ExportdJobBaseStepComponent } from '../exportd-job-base-step.component';
import { takeUntil } from 'rxjs/operators';


@Component({
  selector: 'cmdb-task-sources-step',
  templateUrl: './exportd-job-sources-step.component.html',
  styleUrls: ['./exportd-job-sources-step.component.scss']
})
export class ExportdJobSourcesStepComponent extends ExportdJobBaseStepComponent implements OnInit, OnDestroy {

  private subscriber: ReplaySubject<void> = new ReplaySubject<void>();

  @Input()
  set preData(data: any) {
    if (data !== undefined) {
      if (data.sources) {
        // Create sources
        this.sourcesForm = this.formBuilder.group({
          sources: new UntypedFormArray([])
        });
        this.sourcesForm.removeControl('sources');
        const forArray: UntypedFormArray = this.formBuilder.array([]);
        for (const source of data.sources) {
          forArray.push(this.formBuilder.group({
            type_id: new UntypedFormControl('', Validators.required),
            condition: this.formBuilder.array([])
          }));
        }

        // Create condition
        let i = 0;
        while (i < forArray.controls.length) {
          for (const item of data.sources[i].condition) {
            const control = forArray.controls[i].get('condition') as UntypedFormArray;
            control.push(this.createCondition());
          }
          i++;
        }

        this.sourcesForm.addControl('sources', forArray);
        this.sourcesForm.patchValue(data);
      }
    }
  }

  public operators: any[] = ['!=', '=='];
  public sourcesForm: UntypedFormGroup;
  readonly SOURCES = 'sources';

  constructor(private formBuilder: UntypedFormBuilder, private typeService: TypeService) {
    super();
  }

  public ngOnInit(): void {
    this.sourcesForm = this.formBuilder.group({
      sources: this.formBuilder.array([this.createSource()])
    });

    if (this.mode === CmdbMode.Create) {
      this.delCondition(0, 0);
    }
  }

  /**
   * Load types to display
   * @param publicID
   */
  public loadDisplayType(publicID: number) {
    return this.typeService.getType(publicID).pipe(takeUntil(this.subscriber));
  }

  public getFields(publicID: any) {
    try {
      return this.types.find(id => id.public_id === publicID).fields;
    } catch (e) {
      return [];
    }
  }

  private createSource(): UntypedFormGroup {
    return this.formBuilder.group({
      type_id: new UntypedFormControl(null, Validators.required),
      condition: this.formBuilder.array([this.createCondition()])
    });
  }

  private createCondition(): UntypedFormGroup {
    return this.formBuilder.group({
      name: new UntypedFormControl('', Validators.required),
      value: new UntypedFormControl('', Validators.required),
      operator: new UntypedFormControl('', Validators.required)
    });
  }

  private getSourceAsFormArray(): any {
    return this.sourcesForm.controls[this.SOURCES] as UntypedFormArray;
  }

  public addSource(): void {
    const control = this.getSourceAsFormArray();
    control.push(this.createSource());
  }

  public addCondition(event): void {
    const control = this.getSourceAsFormArray().at(event).get('condition') as UntypedFormArray;
    control.push(this.createCondition());
  }

  public delSource(index): void {
    const control = this.getSourceAsFormArray();
    control.removeAt(index);
  }

  public delCondition(index, event): void {
    const control = this.getSourceAsFormArray().at(event).get('condition') as UntypedFormArray;
    control.removeAt(index);
  }

  public ngOnDestroy(): void {
    this.subscriber.next();
    this.subscriber.complete();
  }

}
