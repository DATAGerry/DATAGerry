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
import { ApiCallService } from '../services/api-call.service';

@Component({
  selector: 'cmdb-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.scss']
})
export class DashboardComponent implements OnInit {

  public objectCount: number;
  public typeCount: number;
  public userCount: number;

  constructor(private api: ApiCallService) {
  }

  public ngOnInit(): void {
    this.api.callGetRoute('object/count/').subscribe((count) => {
      this.objectCount = count;
    });

    this.api.callGetRoute('type/count/').subscribe((count) => {
      this.typeCount = count;
    });

    this.api.callGetRoute('user/count/').subscribe((count) => {
      this.userCount = count;
    });
  }

}
