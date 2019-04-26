/*
* Net|CMDB - OpenSource Enterprise CMDB
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

import { Directive, ElementRef, Input, OnDestroy, OnInit } from '@angular/core';
import { Subject } from 'rxjs';
import 'datatables.net';

@Directive({
  selector: '[cmdbDatatable]'
})
export class DatatableDirective implements OnInit, OnDestroy {

  @Input()
  dtOptions: DataTables.Settings = {};

  @Input()
  dtTrigger: Subject<any>;

  dtInstance: Promise<DataTables.Api>;

  private dt: DataTables.Api;

  constructor(private el: ElementRef) {
  }

  public ngOnDestroy(): void {
    if (this.dtTrigger) {
      this.dtTrigger.unsubscribe();
    }
  }

  public ngOnInit(): void {
    if (this.dtTrigger) {
      this.dtTrigger.subscribe(() => {
        this.displayTable();
      });
    } else {
      this.displayTable();
    }
  }

  private displayTable(): void {
    this.dtInstance = new Promise((resolve, reject) => {
      Promise.resolve(this.dtOptions).then(dtOptions => {
        setTimeout(() => {
          this.dt = $(this.el.nativeElement).DataTable(dtOptions);
          resolve(this.dt);
        });
      });
    });
  }

}
