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

import { Component, OnInit, ViewChild } from '@angular/core';
import { AuthService } from './auth/services/auth.service';
import { ActivationStart, Router, RouterOutlet } from '@angular/router';

@Component({
  selector: 'cmdb-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements OnInit {

  @ViewChild(RouterOutlet, { static: false }) outlet: RouterOutlet;

  public currentUserToken;

  constructor(private router: Router, private authService: AuthService) {
  }

  public ngOnInit(): void {

    this.currentUserToken = this.authService.currentUserTokenValue;
    this.router.events.subscribe(e => {

      if (e instanceof ActivationStart) {
        this.outlet.deactivate();
      }
    });
  }
}
