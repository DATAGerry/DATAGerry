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
import { ActivatedRoute } from '@angular/router';
import { PreviousRouteService } from '../services/previous-route.service';

@Component({
  selector: 'cmdb-error',
  templateUrl: './error.component.html',
  styleUrls: ['./error.component.scss']
})
export class ErrorComponent implements OnInit {
  public readonly statusCode: number = 501;
  public statusText: string;
  public response: string;
  public message: string;
  public readonly now: number = Date.now();
  public previousUrl: string;


  constructor(private route: ActivatedRoute, private prevRouteService: PreviousRouteService) {
    if (this.route.snapshot.paramMap.get('statusCode') !== null) {
      this.statusCode = +this.route.snapshot.paramMap.get('statusCode');
    }
  }

  public ngOnInit(): void {
    this.route.queryParams.subscribe(params => {
      this.statusText = params.statusText;
      this.response = params.response;
      this.message = params.message;
    });

    this.previousUrl = this.prevRouteService.getPreviousUrl();
  }

}
