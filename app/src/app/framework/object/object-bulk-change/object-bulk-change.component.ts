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

import { Component, OnDestroy } from '@angular/core';
import { FormGroup } from '@angular/forms';
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

@Component({
  selector: 'cmdb-object-bulk-change',
  templateUrl: './object-bulk-change.component.html',
  styleUrls: ['./object-bulk-change.component.scss']
})
export class ObjectBulkChangeComponent implements OnDestroy {

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
  public changeForm: FormGroup = new FormGroup({});
  public renderForm: FormGroup = new FormGroup({});

  /**
   * Active status changed.
   */
  public activeState: boolean | undefined = undefined;

  /**
   * List of to change selected items.
   */
  public renderResults: Array<RenderResult> = [];

  constructor(private objectService: ObjectService, private typeService: TypeService, private userServer: UserService,
              private activeRoute: ActivatedRoute, private router: Router, private toastService: ToastService) {
    if (this.router.getCurrentNavigation().extras.state) {
      this.type = this.router.getCurrentNavigation().extras.state.type;
      this.renderResults = this.router.getCurrentNavigation().extras.state.objects;
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
    const changes = this.changeForm.getRawValue();
    const httpOptions = Object.assign({}, httpObserveOptions);
    httpOptions.params = { objectIDs: this.renderResults.map(m => m.object_information.object_id) };
    const patchValue = [];
    const newObjectInstance = new CmdbObject();
    newObjectInstance.author_id = this.userServer.getCurrentUser().public_id;
    if (this.activeState !== undefined) {
      newObjectInstance.active = this.activeState;
    }
    newObjectInstance.type_id = this.type.public_id;
    newObjectInstance.fields = [];
    Object.keys(changes).forEach((key: string) => {
      patchValue.push({
        name: key,
        value: changes[key]
      });
    });
    newObjectInstance.fields = patchValue;
    this.objectService.putObject(0, newObjectInstance, httpOptions).pipe(takeUntil(this.subscriber))
      .subscribe((res: boolean) => {
        this.toastService.success(`Bulk updated objects of type ${this.type.label}`);
        this.router.navigate(['framework', 'object', 'type', this.type.public_id]);
      });
  }

  public ngOnDestroy(): void {
    this.subscriber.next();
    this.subscriber.complete();
  }

}
