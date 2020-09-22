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

import { Component, ElementRef, OnDestroy, OnInit, ViewChild } from '@angular/core';
import { AbstractControl, FormControl, FormGroup, Validators } from '@angular/forms';
import { Group } from '../../models/group';
import { AuthService } from '../../../auth/services/auth.service';
import { UserService } from '../../services/user.service';
import { GroupService } from '../../services/group.service';
import { ToastService } from '../../../layout/toast/toast.service';
import { ActivatedRoute, Router } from '@angular/router';
import { User } from '../../models/user';
import { Observable, Subscription } from 'rxjs';


@Component({
  selector: 'cmdb-users-edit',
  templateUrl: './users-edit.component.html',
  styleUrls: ['./users-edit.component.scss']
})
export class UsersEditComponent implements OnInit, OnDestroy {

  @ViewChild('passWordInput', { static: false }) public passWordToggle: ElementRef;
  public editForm: FormGroup;
  public authProviders: any[] = [];
  public groupList: Group[];
  private currentPasswordStrength: number = 0;
  public preview: any = undefined;

  // ROUTE PARAMS
  private routeParamObserver: Observable<any>;
  private routeParamSubscription: Subscription;

  // USER DATA
  public userID: number;
  public editUser: User;
  private userServiceObserver: Observable<User>;
  private userServiceSubscription: Subscription;

  constructor(private authService: AuthService, private userService: UserService, private groupService: GroupService,
              private toastService: ToastService, private router: Router, private route: ActivatedRoute) {
    this.routeParamObserver = this.route.params;
    this.editForm = new FormGroup({
      public_id: new FormControl(0),
      user_name: new FormControl('', Validators.required),
      email: new FormControl('', [Validators.required, Validators.email]),
      first_name: new FormControl(null),
      last_name: new FormControl(null),
      authenticator: new FormControl('LocalAuthenticationProvider', Validators.required),
      group_id: new FormControl(2, Validators.required),
      image: new FormControl(null)
    });
    this.user_name.disable();
  }

  public ngOnInit(): void {
    this.routeParamSubscription = this.routeParamObserver.subscribe(
      (params) => {
        this.userID = params.publicID;
        this.userServiceObserver = this.userService.getUser(this.userID);
        this.userServiceSubscription = this.userServiceObserver.subscribe((user: User) => {
          this.editUser = user;
          this.patchGroupToForm();
        });
      }
    );

    this.authService.getAuthProviders().subscribe((providerList: any[]) => {
      for (const provider of providerList) {
        this.authProviders.push(provider.class_name);
      }
    });
    this.groupService.getGroupList().subscribe((groupList: Group[]) => {
      this.groupList = groupList;
    });

  }

  public onPasswordStrengthChanged(strength) {
    this.currentPasswordStrength = strength;
  }

  public toggleInput() {
    if (this.passWordToggle.nativeElement.type === 'password') {
      this.passWordToggle.nativeElement.type = 'text';
    } else {
      this.passWordToggle.nativeElement.type = 'password';
    }
  }

  public get user_name() {
    return this.editForm.get('user_name');
  }

  public get email() {
    return this.editForm.get('email');
  }

  public get password() {
    return this.editForm.get('password');
  }

  public get first_name() {
    return this.editForm.get('first_name');
  }

  public get last_name() {
    return this.editForm.get('last_name');
  }

  public get authenticator() {
    return this.editForm.get('authenticator');
  }

  public get group() {
    return this.editForm.get('group_id');
  }

  public get image() {
    return this.editForm.get('image');
  }

  public previewImage(event) {
    if (event.target.files && event.target.files[0]) {
      const reader = new FileReader();
      reader.onload = (eve: ProgressEvent) => {
        this.preview = (eve.target as FileReader).result;
        this.image.setValue(this.preview);
      };
      reader.readAsDataURL(event.target.files[0]);
    }
  }

  private patchGroupToForm() {
    Object.keys(this.editUser).forEach(name => {
      if (this.editForm.controls[name]) {
        this.editForm.controls[name].patchValue(this.editUser[name], { onlySelf: true });
      }
    });
    this.editForm.markAllAsTouched();
  }

  public updateUser() {
    this.editForm.markAllAsTouched();
    if (this.editForm.valid) {
      const data = this.editForm.getRawValue();
      this.userService.putUser(this.userID, data).subscribe(addResp => {
        this.toastService.success(`User with ID: ${ this.userID } was updated!`);
      }, (error) => {
        this.toastService.error(error.error.description);
      }, () => {
        this.router.navigate(['/management/users/']);
      });
    }
  }

  public ngOnDestroy(): void {
    this.routeParamSubscription.unsubscribe();
    this.userServiceSubscription.unsubscribe();
  }
}

