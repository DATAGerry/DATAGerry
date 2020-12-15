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

import { AfterViewInit, Component, OnDestroy, OnInit, ViewChild } from '@angular/core';
import { Right } from '../models/right';
import { ActivatedRoute } from '@angular/router';
import { DataTableDirective } from 'angular-datatables';
import { Subject } from 'rxjs';

@Component({
  selector: 'cmdb-rights',
  templateUrl: './rights.component.html',
  styleUrls: ['./rights.component.scss']
})
export class RightsComponent implements OnInit, AfterViewInit, OnDestroy {

  public rights: Array<Right> = [];

  @ViewChild(DataTableDirective)
  private dtElement: DataTableDirective;
  public dtOptions: any = {};
  public dtTrigger: Subject<any> = new Subject();

  constructor(private route: ActivatedRoute) {
    this.rights = this.route.snapshot.data.rights as Array<Right>;
  }

  public ngOnInit(): void {
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

  public ngOnDestroy(): void {
    this.dtTrigger.unsubscribe();
    this.dtElement.dtInstance.then((dtInstance: DataTables.Api) => {
      dtInstance.destroy();
    });

  }

  public ngAfterViewInit(): void {
    this.dtTrigger.next();
  }


}
