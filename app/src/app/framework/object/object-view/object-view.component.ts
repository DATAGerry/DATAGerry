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

import { Component, OnInit } from '@angular/core';
import { ApiCallService } from '../../../services/api-call.service';
import { ActivatedRoute, Router } from '@angular/router';
import { CmdbObject } from '../../models/cmdb-object';
import { ObjectService } from '../../services/object.service';
import { CmdbType } from '../../models/cmdb-type';
import { TypeService } from '../../services/type.service';
import { CmdbMode } from '../../modes.enum';
import { RenderService } from '../../render/service/render.service';
import { RenderResult } from '../../models/cmdb-render';
import { LogService } from '../../services/log.service';
import { CmdbLog } from '../../models/cmdb-log';

@Component({
  selector: 'cmdb-object-view',
  templateUrl: './object-view.component.html',
  styleUrls: ['./object-view.component.scss']
})
export class ObjectViewComponent implements OnInit {

  public mode: CmdbMode = CmdbMode.View;
  private objectID: number;
  public renderResult: RenderResult;

  constructor(public renderService: RenderService, private activateRoute: ActivatedRoute) {
    this.activateRoute.params.subscribe((params) => {
      this.objectID = params.publicID;
      this.ngOnInit();
    });
  }

  public ngOnInit(): void {
    // RenderResult
    this.renderService.getRenderResult(this.objectID).subscribe((result: RenderResult) => {
      this.renderResult = result;
    }, (error) => {
      console.error(error);
    });
  }

}
