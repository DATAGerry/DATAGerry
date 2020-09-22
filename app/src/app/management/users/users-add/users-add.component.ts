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
import { AuthService } from '../../../auth/services/auth.service';
import { checkUserExistsValidator, UserService } from '../../services/user.service';
import { User } from '../../models/user';
import { Group } from '../../models/group';
import { GroupService } from '../../services/group.service';
import { ToastService } from '../../../layout/toast/toast.service';
import { Router } from '@angular/router';
import { Subscription } from 'rxjs';
import { map, delay } from 'rxjs/operators';


@Component({
  selector: 'cmdb-users-add',
  templateUrl: './users-add.component.html',
  styleUrls: ['./users-add.component.scss']
})
export class UsersAddComponent implements OnInit, OnDestroy {

  @ViewChild('passWordInput', { static: false }) public passWordToggle: ElementRef;

  public addForm: FormGroup;
  public authProviders: any[] = [];
  public groupList: Group[];
  private currentPasswordStrength: number = 0;
  public preview: any = undefined;

  private authProvidersSubscription: Subscription;
  private groupListSubscription: Subscription;

  constructor(private authService: AuthService, private userService: UserService, private groupService: GroupService,
              private toastService: ToastService, private router: Router) {
    this.addForm = new FormGroup({
      user_name: new FormControl('', [Validators.required], [checkUserExistsValidator(this.userService)]),
      email: new FormControl('', [Validators.required, Validators.email]),
      password: new FormControl('', [Validators.required]),
      first_name: new FormControl(null),
      last_name: new FormControl(null),
      authenticator: new FormControl('LocalAuthenticationProvider', Validators.required),
      group_id: new FormControl(2, Validators.required),
      image: new FormControl(null)
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

  public ngOnInit(): void {
    this.authProvidersSubscription = this.authService.getAuthProviders().subscribe((providerList: any[]) => {
      for (const provider of providerList) {
        this.authProviders.push(provider.class_name);
      }
    });
    this.groupListSubscription = this.groupService.getGroupList().subscribe((groupList: Group[]) => {
      this.groupList = groupList;
    });
  }

  public ngOnDestroy(): void {
    this.authProvidersSubscription.unsubscribe();
    this.groupListSubscription.unsubscribe();
  }

  public get user_name() {
    return this.addForm.get('user_name');
  }

  public get email() {
    return this.addForm.get('email');
  }

  public get password() {
    return this.addForm.get('password');
  }

  public get first_name() {
    return this.addForm.get('first_name');
  }

  public get last_name() {
    return this.addForm.get('last_name');
  }

  public get authenticator() {
    return this.addForm.get('authenticator');
  }

  public get group() {
    return this.addForm.get('group_id');
  }

  public get image() {
    return this.addForm.get('image');
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

  public saveUser() {
    this.addForm.markAllAsTouched();
    if (this.addForm.valid) {
      const addUser: User = this.addForm.getRawValue();
      this.userService.postUser(addUser).subscribe(addResp => {
        this.toastService.showToast(`User was added with ID: ${ addResp }`);
      }, (error) => {
        this.toastService.error(error.error.description);
      }, () => {
        this.router.navigate(['/management/users/']);
      });
    }
  }
}
