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
import { AuthService } from './services/auth.service';
import { ActivatedRoute, Router } from '@angular/router';

@Component({
  selector: 'cmdb-auth',
  templateUrl: './auth.component.html',
  styleUrls: ['./auth.component.scss']
})
export class AuthComponent implements OnInit {

  userName: string;
  userPassword: string;
  returnUrl: string;
  error = '';
  shake: any;

  constructor(private authService: AuthService, private router: Router, private route: ActivatedRoute) {
  }

  ngOnInit() {
    this.returnUrl = this.route.snapshot.queryParams['returnUrl'] || '/';
  }

  public onLogin() {
    this.authService.login(this.userName, this.userPassword).subscribe(loginResult => {
        this.router.navigate([this.returnUrl]);
      },
      error => {
        this.error = error;
      });
  }
}
