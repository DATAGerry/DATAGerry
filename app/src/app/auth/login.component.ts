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

import { Component, OnDestroy, OnInit, Renderer2 } from '@angular/core';
import { AuthService } from './services/auth.service';
import { ActivatedRoute, Router } from '@angular/router';
import { FormBuilder, FormControl, FormGroup, Validators } from '@angular/forms';
import { first } from 'rxjs/operators';
import { forkJoin, Subscription } from 'rxjs';
import { User } from '../management/models/user';
import { PermissionService } from './services/permission.service';

@Component({
  selector: 'cmdb-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss']
})
export class LoginComponent implements OnInit, OnDestroy {

  public loginForm: FormGroup;
  public submitted = false;

  private loginSubscription: Subscription;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private authenticationService: AuthService,
    private permissionService: PermissionService,
    private render: Renderer2
  ) {
    this.loginSubscription = new Subscription();
  }

  public ngOnInit(): void {
    this.render.addClass(document.body, 'embedded');
    this.loginForm = new FormGroup({
      username: new FormControl('', [Validators.required]),
      password: new FormControl('', [Validators.required])
    });
  }

  public ngOnDestroy(): void {
    this.render.removeClass(document.body, 'embedded');
    this.loginSubscription.unsubscribe();
  }

  get controls() {
    return this.loginForm.controls;
  }

  public onSubmit() {
    this.submitted = true;
    this.render.addClass(document.getElementById('login-button'), 'button-progress');

    this.loginSubscription = this.authenticationService.login(
      this.loginForm.controls.username.value, this.loginForm.controls.password.value).pipe(first()).subscribe(
      (user: User) => {
        this.permissionService.storeUserRights(user.group_id).then(() => {
          this.router.navigate(['/']);
        });
      },
      async error => {
        this.render.removeClass(document.getElementById('login-button'), 'button-progress');
        this.render.addClass(document.getElementById('login-logo'), 'shake');
        this.loginForm.reset();
        await this.delay(1000);
        this.render.removeClass(document.getElementById('login-logo'), 'shake');
      }
    );

  }

  public delay(ms: number) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }


}
