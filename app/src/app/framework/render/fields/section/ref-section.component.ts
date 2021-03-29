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
import { CmdbObject } from '../../../models/cmdb-object';
import { ObjectService } from '../../../services/object.service';
import { CollectionParameters } from '../../../../services/models/api-parameter';
import { CmdbMode } from '../../../modes.enum';
import { takeUntil } from 'rxjs/operators';
import { ReplaySubject } from 'rxjs';
import { APIGetMultiResponse } from '../../../../services/models/api-response';

@Component({
  selector: 'cmdb-ref-section',
  templateUrl: './ref-section.component.html',
  styleUrls: ['./ref-section.component.scss']
})
export class RefSectionComponent extends RenderFieldComponent implements OnInit, OnDestroy {

  private subscriber: ReplaySubject<void> = new ReplaySubject<void>();
  public objects: Array<CmdbObject> = [];

  public loading: boolean = false;

  public totalObjects: number = 0;
  private currentPage: number = 1;
  private maxPage: number = 1;

  constructor(private objectService: ObjectService) {
    super();
  }

  private getApiParameters(page: number = 1): CollectionParameters {
    return {
      filter: { type_id: this.section.reference.type_id }, limit: 10, sort: 'public_id',
      order: 1, page, projection: { object_information: 1, summary_line: 1 }
    } as CollectionParameters;
  }

  private loadObjectsFromApi(): void {
    this.loading = true;
    this.objectService.getObjects(this.getApiParameters(this.currentPage)).pipe(takeUntil(this.subscriber))
      .subscribe((apiResponse: APIGetMultiResponse<CmdbObject>) => {
        this.objects = [... this.objects, ... apiResponse.results as Array<CmdbObject>];
        this.totalObjects = apiResponse.total;
        this.maxPage = apiResponse.pager.total_pages;
    }).add(() => this.loading = false);
  }

  private triggerAPICall(): void {
    if (this.maxPage && (this.currentPage <= this.maxPage)) {
      this.loadObjectsFromApi();
      this.currentPage += 1;
    }
  }

  public onScrollToEnd(): void {
    this.triggerAPICall();
  }


  public ngOnInit(): void {

    switch (this.mode) {
      case CmdbMode.Create:
      case CmdbMode.Edit:
      case CmdbMode.Bulk: {
        this.triggerAPICall();
        break;
      }

      case CmdbMode.View : {
        break;
      }
    }
  }

  public ngOnDestroy(): void {
    this.subscriber.next();
    this.subscriber.complete();
  }


}
