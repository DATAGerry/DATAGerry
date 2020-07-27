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

import {Component, HostListener, OnInit} from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { ObjectService } from '../../services/object.service';
import { CmdbMode } from '../../modes.enum';
import { RenderResult } from '../../models/cmdb-render';
import { DataTableFilter, DataTablesResult } from '../../models/cmdb-datatable';
import {consoleTestResultHandler} from "tslint/lib/test";

@Component({
  selector: 'cmdb-object-view',
  templateUrl: './object-view.component.html',
  styleUrls: ['./object-view.component.scss']
})
export class ObjectViewComponent implements OnInit {

  public mode: CmdbMode = CmdbMode.View;
  private objectID: number;
  public renderResult: RenderResult;
  public recordsTotal: number = 0;

  constructor(public objectService: ObjectService, private activateRoute: ActivatedRoute) {
    this.activateRoute.params.subscribe((params) => {
      this.objectID = params.publicID;
      this.ngOnInit();
    });
  }

  public ngOnInit(): void {
    this.objectService.getObject(this.objectID).subscribe((result: RenderResult) => {
      this.renderResult = result;
      if (result) {
        this.objectService.getObjectsByFilter(result.type_information.type_id, new DataTableFilter())
          .subscribe((resp: DataTablesResult) => {
            this.recordsTotal = resp.recordsTotal;
          });
      }
    }, (error) => {
      console.error(error);
    });
  }

  public logChange(event) {
    // TODO: Update log list after object changed
  }

}
