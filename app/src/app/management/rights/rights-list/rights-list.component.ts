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

import { Component, OnDestroy, OnInit, ViewChild } from '@angular/core';
import { RightService } from '../../services/right.service';
import { Right } from '../../models/right';
import { Subject, Subscription } from 'rxjs';
import { DataTableDirective } from 'angular-datatables';

@Component({
  selector: 'cmdb-rights-list',
  templateUrl: './rights-list.component.html',
  styleUrls: ['./rights-list.component.scss']
})
export class RightsListComponent implements OnInit, OnDestroy {

  // TABLE
  @ViewChild(DataTableDirective, { static: false })
  private dtElement: DataTableDirective;
  public dtOptions: any = {};
  public dtTrigger: Subject<any> = new Subject();

  // RIGHT DATA
  private rightListSubscription: Subscription;
  public rightList: Right[] = [];

  // LEVEL DATA
  private securityRightLevelsSubscription: Subscription;
  public securityRightLevels: any[] = [];

  constructor(private rightService: RightService) {
    this.dtOptions = {
      ordering: false,
      rowGroup: {
        startRender: (rows, group) => {
          return group + ' (' + rows.count() + ' rights)';
        },
        dataSrc: (data) => {
          const baseData = data[0].split('.');
          return `${baseData[0]}.${baseData[1]}`;
        }
      },
      pageLength: 50
    };
  }

  public ngOnInit(): void {
    this.rightListSubscription = this.rightService.getRightList().subscribe((rightList: Right[]) => {
        this.rightList = rightList;
        this.dtTrigger.next();
      });
    this.securityRightLevelsSubscription = this.rightService.getRightLevels().subscribe((levels: any[]) => {
      this.securityRightLevels = levels;
    });
  }

  public ngOnDestroy(): void {
    this.rightListSubscription.unsubscribe();
    this.securityRightLevelsSubscription.unsubscribe();
    this.dtTrigger.unsubscribe();
    this.dtElement.dtInstance.then((dtInstance: DataTables.Api) => {
      dtInstance.destroy();
    });

  }

}
