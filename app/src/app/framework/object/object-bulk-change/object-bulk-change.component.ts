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

import { Component, OnDestroy, ViewChild } from '@angular/core';
import { UntypedFormGroup } from '@angular/forms';
import { ObjectService } from '../../services/object.service';
import { TypeService } from '../../services/type.service';
import { ActivatedRoute, Router } from '@angular/router';
import { RenderResult } from '../../models/cmdb-render';
import { ReplaySubject } from 'rxjs';
import { CmdbType } from '../../models/cmdb-type';
import { httpObserveOptions } from '../../../services/api-call.service';
import { CmdbObject } from '../../models/cmdb-object';
import { takeUntil } from 'rxjs/operators';
import { ToastService } from '../../../layout/toast/toast.service';
import { UserService } from '../../../management/services/user.service';
import { ProgressSpinnerService } from '../../../layout/progress/progress-spinner.service';
import { WizardComponent } from 'angular-archwizard';
import { APIUpdateMultiResponse } from '../../../services/models/api-response';

@Component({
  selector: 'cmdb-object-bulk-change',
  templateUrl: './object-bulk-change.component.html',
  styleUrls: ['./object-bulk-change.component.scss']
})
export class ObjectBulkChangeComponent implements OnDestroy {

  /**
   * The aw-wizard component defines the root component of a wizard.
   */
  @ViewChild('wizard', { static: false }) public wizard: WizardComponent;

  /**
   * Component un subscriber.
   * @private
   */
  private subscriber: ReplaySubject<void> = new ReplaySubject<void>();

  /**
   * Type of objects to bulk change.
   */
  public type: CmdbType;

  /**
   * Form for bulk change editor.
   */
  public changeForm: UntypedFormGroup = new UntypedFormGroup({});
  public renderForm: UntypedFormGroup = new UntypedFormGroup({});

  /**
   * Active status changed.
   */
  public activeState: boolean | undefined = undefined;

  /**
   * List of to change selected items.
   */
  public renderResults: Array<RenderResult> = [];

  /**
   * APIUpdateMultiResponse
   */
  public apiResponse: APIUpdateMultiResponse;

  /**
   * HTTP Options for PUT request
   * @private
   */
  private httpOptions;

  constructor(private objectService: ObjectService, private typeService: TypeService, private userServer: UserService,
              private activeRoute: ActivatedRoute, private router: Router, private toastService: ToastService,
              private spinner: ProgressSpinnerService, ) {
    if (this.router.getCurrentNavigation().extras.state) {
      this.type = this.router.getCurrentNavigation().extras.state.type;
      this.renderResults = this.router.getCurrentNavigation().extras.state.objects;
      this.httpOptions = Object.assign({}, httpObserveOptions);
      this.httpOptions.params = { objectIDs: this.renderResults.map(m => m.object_information.object_id) };
    }
  }

  /**
   * Was the form touched.
   */
  public get hasChanges(): boolean {
    return this.renderForm.dirty;
  }

  /**
   * Save a references object to the database.
   */
  public saveObject() {
    this.spinner.show();

    const changes = this.changeForm.getRawValue();
    const newObjectInstance = new CmdbObject();

    if (this.activeState !== undefined) {
      newObjectInstance.active = this.activeState;
    }

    newObjectInstance.author_id = this.userServer.getCurrentUser().public_id;
    newObjectInstance.type_id = this.type.public_id;
    newObjectInstance.fields = [];

    Object.keys(changes).forEach((key: string) => {
      newObjectInstance.fields.push({
        name: key,
        value: changes[key]
      });
    });

    this.objectService.putObject(0, newObjectInstance, this.httpOptions)
      .pipe(takeUntil(this.subscriber)).subscribe((response: APIUpdateMultiResponse) => {
        this.apiResponse = response;
        this.goToNextStepIndex(2);
      }, () => {
        this.spinner.hide();
      }, () => {
        this.spinner.hide();
      });
  }

  private goToNextStepIndex(index: number) {
    if (this.wizard ) {
      this.wizard.goToStep(index);
    }
  }

  public ngOnDestroy(): void {
    this.subscriber.next();
    this.subscriber.complete();
  }

}
