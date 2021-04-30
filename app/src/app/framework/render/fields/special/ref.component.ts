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

import { Component, OnDestroy, OnInit } from '@angular/core';
import { RenderFieldComponent } from '../components.fields';
import { ObjectService } from '../../../services/object.service';
import { RenderResult } from '../../../models/cmdb-render';
import { HttpBackend, HttpResponse } from '@angular/common/http';
import { AuthService } from '../../../../auth/services/auth.service';
import { NgbModal, NgbModalRef } from '@ng-bootstrap/ng-bootstrap';
import { ObjectPreviewModalComponent } from '../../../object/modals/object-preview-modal/object-preview-modal.component';
import { CollectionParameters } from '../../../../services/models/api-parameter';
import { takeUntil } from 'rxjs/operators';
import { APIGetMultiResponse } from '../../../../services/models/api-response';
import { BehaviorSubject, ReplaySubject } from 'rxjs';
import { CmdbMode } from '../../../modes.enum';

@Component({
  templateUrl: './ref.component.html',
  styleUrls: ['./ref.component.scss']
})
export class RefComponent extends RenderFieldComponent implements OnInit, OnDestroy {

  private modalRef: NgbModalRef;
  private unsubscribe: ReplaySubject<void> = new ReplaySubject<void>();
  public objectList: Array<RenderResult> = [];
  public refObject: RenderResult;
  public changedReference: BehaviorSubject<any> = new BehaviorSubject<any>(undefined);
  public protect: boolean = false;

  public constructor(private objectService: ObjectService, private backend: HttpBackend,
                     private authService: AuthService, private modalService: NgbModal) {
    super();
  }

  public ngOnInit(): void {

    this.data.default = parseInt(this.data.default, 10);
    if (this.mode === CmdbMode.Edit || this.mode === CmdbMode.Create || this.mode === CmdbMode.Bulk) {
      if (this.data.ref_types) {
        if (this.data.ref_types) {
          if (!Array.isArray(this.data.ref_types)) {
            this.data.ref_types = [this.data.ref_types];
          }
        }
        const params: CollectionParameters = {
          filter: [{ $match: { type_id: { $in: this.data.ref_types } } }],
          limit: 0, sort: 'public_id', order: 1, page: 1
        };
        this.objectService.getObjects(params).pipe(takeUntil(this.unsubscribe))
          .subscribe((apiResponse: APIGetMultiResponse<RenderResult>) => {
            this.objectList = apiResponse.results;
          });
      }
    }

    if (this.data.reference && this.data.reference.object_id !== '' && this.data.reference.object_id !== 0) {
      if (typeof this.data.reference === 'string' || this.mode === CmdbMode.Create || this.mode === CmdbMode.Bulk) {
        this.protect = true;
      } else {
        this.objectService.getObject(this.data.reference?.object_id, false).pipe(takeUntil(this.unsubscribe))
          .subscribe((refObject: RenderResult) => {
              this.refObject = refObject;
            },
            (error) => {
              console.error(error);
            });
      }
    }
  }

  groupByFn = (item) => item.type_information.type_label;
  groupValueFn = (_: string, children: any[]) => ({
    name: children[0].type_information.type_label,
    total: children.length
  })

  public ngOnDestroy(): void {
    if (this.modalRef) {
      this.modalRef.close();
    }
    this.unsubscribe.next();
    this.unsubscribe.complete();
  }

  public searchRef(term: string, item: any) {
    term = term.toLocaleLowerCase();
    const value = item.object_information.object_id + item.type_information.type_label + item.summary_line;
    return value.toLocaleLowerCase().indexOf(term) > -1 || value.toLocaleLowerCase().includes(term);
  }

  public showReferencePreview() {
    this.modalRef = this.modalService.open(ObjectPreviewModalComponent, { size: 'lg' });
    this.modalRef.componentInstance.renderResult = this.refObject;
  }
}
