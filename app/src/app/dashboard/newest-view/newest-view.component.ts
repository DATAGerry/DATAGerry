/*
* dataGerry - OpenSource Enterprise CMDB
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

import { Component, Input, OnDestroy, OnInit } from '@angular/core';
import { ApiCallService } from '../../services/api-call.service';
import { TableColumnAction } from '../../layout/components/table/models/table-columns-action';
import { RenderService } from '../../framework/render/service/render.service';
import { SpecialService } from '../../framework/services/special.service';
import { RenderResult } from '../../framework/models/cmdb-render';
import { Subject } from 'rxjs';

@Component({
  selector: 'cmdb-newest-view',
  templateUrl: './newest-view.component.html',
  styleUrls: ['./newest-view.component.scss']
})

export class NewestViewComponent implements OnInit, OnDestroy {

  public newest: RenderResult[] = [];
  public dtOptions: any = {};
  public dtTrigger: Subject<any> = new Subject();

  public constructor(private specialService: SpecialService<RenderResult>) {
  }

  public ngOnInit(): void {
    this.dtOptions = {
      ordering: true,
      order: [[4, 'desc']],
      language: {
        search: '',
        searchPlaceholder: 'Filter...'
      }
    };
    this.specialService.getNewestObjects().subscribe((newestList: RenderResult[]) => {
        this.newest = newestList;
      },
      err => {
        console.error(err);
      },
      () => {
        this.dtTrigger.next();
      });
  }

  public ngOnDestroy(): void {
    this.dtTrigger.unsubscribe();
  }

}
