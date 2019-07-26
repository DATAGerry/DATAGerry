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

import { Component, OnDestroy, OnInit, ViewChild } from '@angular/core';
import { CmdbType } from '../../../models/cmdb-type';
import { TypeService } from '../../../services/type.service';
import { Subject } from 'rxjs';
import { DataTableDirective } from 'angular-datatables';
import { ActivatedRoute, Router } from '@angular/router';
import { ToastService } from '../../../../layout/services/toast.service';

@Component({
  selector: 'cmdb-type-list',
  templateUrl: './type-list.component.html',
  styleUrls: ['./type-list.component.scss']
})
export class TypeListComponent implements OnInit, OnDestroy {

  @ViewChild(DataTableDirective, {static: false})
  public dtElement: DataTableDirective;

  public typeList: CmdbType[] = [];
  public dtOptions: DataTables.Settings = {};
  public dtTrigger: Subject<any> = new Subject();
  public linkRoute: string = 'type/';
  public addNewType: {};

  constructor(private typeService: TypeService, private toastService: ToastService,
              private router: Router, private route: ActivatedRoute) {
    this.addNewType = {
      text: '<i class="fa fa-plus" aria-hidden="true"></i> Add',
      className: 'btn btn-success btn-sm mr-1',
      action: function() {
        this.router.navigate(['/framework/type/add']);
      }.bind(this)
    };
  }

  public ngOnInit(): void {
    this.dtOptions = {
      ordering: true,
      order: [[1, 'asc']],
      language: {
        search: '',
        searchPlaceholder: 'Filter...'
      },
    };

    this.route.params.subscribe((param) => {
      if (param.typeAddSuccess !== undefined) {
        this.toastService.show('A new type was added with ID: ' + param.typeAddSuccess);
      }
    });

    this.typeService.getTypeList().subscribe((list: CmdbType[]) => {
        this.typeList = this.typeList.concat(list);
      },
      (err) => {
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
