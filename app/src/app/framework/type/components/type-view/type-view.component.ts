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

import { Component, OnInit } from '@angular/core';
import { ApiCallService } from '../../../../services/api-call.service';
import { ActivatedRoute } from '@angular/router';
import { CmdbType } from '../../../models/cmdb-type';
import { CmdbObject } from '../../../models/cmdb-object';

@Component({
  selector: 'cmdb-type-view',
  templateUrl: './type-view.component.html',
  styleUrls: ['./type-view.component.scss']
})
export class TypeViewComponent implements OnInit {

  private typeID: number;
  private typeInstance: CmdbType;

  constructor(private api: ApiCallService, private route: ActivatedRoute) {
    this.route.params.subscribe((id) => this.typeID = id.publicID);
  }

  public ngOnInit(): void {
    this.api.callGetRoute<CmdbType>('type/' + `${this.typeID}`)
      .subscribe((typeInstance: CmdbType) => this.typeInstance = typeInstance);
  }

}
