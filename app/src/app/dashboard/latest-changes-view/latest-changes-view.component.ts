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

import { Component, OnDestroy, OnInit } from '@angular/core';
import { RenderResult } from '../../framework/models/cmdb-render';
import { Subject } from 'rxjs';
import { SpecialService } from '../../framework/services/special.service';

@Component({
  selector: 'cmdb-latest-changes-view',
  templateUrl: './latest-changes-view.component.html',
  styleUrls: ['./latest-changes-view.component.scss']
})
export class LatestChangesViewComponent implements OnInit {

  public latest: RenderResult[] = [];
  public thColumnsActions: any[] = [];

  public constructor(private specialService: SpecialService<RenderResult>) {
  }

  public ngOnInit(): void {
    this.specialService.getLatestObjects().subscribe((latestList: RenderResult[]) => {
        this.latest = latestList;
      });

    this.thColumnsActions = [
      { name: 'view', classValue: 'text-dark ml-1', linkRoute: 'framework/object/view/', fontIcon: 'eye', active: true},
      { name: 'copy', classValue: 'text-dark ml-1', linkRoute: 'framework/object/copy/', fontIcon: 'copy'},
      { name: 'edit', classValue: 'text-dark ml-1', linkRoute: 'framework/object/edit/', fontIcon: 'edit'},
      { name: 'delete', classValue: 'text-dark ml-1', linkRoute: 'object/', fontIcon: 'trash-alt'}];
  }
}

