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


import { Component, OnDestroy, ViewChild } from '@angular/core';
import { DataTableDirective } from 'angular-datatables';
import { Subject } from 'rxjs';
import { ApiCallService } from '../../../../services/api-call.service';
import { ActivatedRoute } from '@angular/router';
import { NgxSpinnerService } from 'ngx-spinner';
import { map } from 'rxjs/operators';
import { DatePipe } from '@angular/common';
import { element } from 'protractor';

@Component({
  selector: 'cmdb-object-list',
  templateUrl: './object-list.component.html',
  styleUrls: ['./object-list.component.scss'],
  providers: [DatePipe]
})
export class ObjectListComponent implements OnDestroy {

  @ViewChild(DataTableDirective)
  public dtElement: DataTableDirective;
  public dtOptions: any = {}; // : DataTables.Settings = {};
  public dtTrigger: Subject<any> = new Subject();

  private summaries: [];
  private items: [];
  public objectLists: {};
  public isCategorized: boolean = false;
  readonly $date: string = '$date';

  constructor(private apiCallService: ApiCallService, private route: ActivatedRoute,
              private spinner: NgxSpinnerService, private dateFormatPipe: DatePipe) {

    this.route.params.subscribe((id) => {
      this.init(id);
    });
  }

  private init(id) {
    this.getRouteObjects(id.publicID);
  }

  private buildDtOptions() {
    this.dtOptions = {
      ordering: true,
      order: [[1, 'asc']],
      retrieve: true,
      language: {
        search: '',
        searchPlaceholder: 'Filter...'
      }
    };
  }

  private getRouteObjects(id) {
    let url = 'object/';
    if ( typeof id !== 'undefined') {
      url = url + 'type/' + id;
      this.isCategorized = true;
    }

    this.apiCallService.callGetRoute(url)
      .pipe(
        map( dataArray => {
          this.summaries = dataArray[0].summaries;
          this.items = dataArray;
          return[ {items: this.items, sums: this.summaries} ];
        })
      )
      .subscribe(
      data => {
        setTimeout( () => {
          this.objectLists = data;
          this.rerender();
          this.dtTrigger.next();
          this.spinner.hide();
        }, 100);
      });
    this.buildDtOptions();
  }

  ngOnDestroy(): void {
    // Do not forget to unsubscribe the event
    this.dtTrigger.unsubscribe();
  }

  public rerender(): void {
    if (typeof this.dtElement.dtInstance !== 'undefined') {
      this.dtElement.dtInstance.then((dtInstance: DataTables.Api) => {
        // Destroy the table first
        dtInstance.destroy();
      });
    }
  }

  public checkType(value) {
    if (value.hasOwnProperty('$date')) {
      return '<span>' + this.dateFormatPipe.transform(value[this.$date], 'dd/mm/yyyy - hh:mm:ss') + '</span>';
    }
    return '<span>' + value + '</span>';
  }

  public selectAll() {
    const overall: any = document.getElementsByClassName('select-all-checkbox')[0];
    const allCheckbox: any = document.getElementsByClassName('select-checkbox');
    const checking = overall.checked;
    for (const box of allCheckbox) {
      box.checked = checking;
    }
  }

  public updateDisplay() {
    const overall: any = document.getElementsByClassName('select-all-checkbox')[0];
    const allCheckbox: any = document.getElementsByClassName('select-checkbox');
    let checkedCount = 0;

    for (const box of allCheckbox) {
      if (box.checked) {
        checkedCount++;
        console.log(checkedCount);
      }
    }

    if (checkedCount === 0) {
      overall.checked = false;
      overall.indeterminate = false;
    } else if (checkedCount === allCheckbox.length) {
      overall.checked = true;
      overall.indeterminate = false;
    } else {
      overall.checked = false;
      overall.indeterminate = true;
    }
  }

  public delObject(id: number) {
    this.apiCallService.callDeleteRoute('object/' + id).subscribe(data => {
    });
  }
}
