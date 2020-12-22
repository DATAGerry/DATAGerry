/*
* DATAGERRY - OpenSource Enterprise CMDB
* Copyright (C) 2019 - 2020 NETHINKS GmbH
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
* along with this program. If not, see <https://www.gnu.org/licenses/>.
*/

import { Component, ElementRef, Input, ViewChild } from '@angular/core';
import { NgbActiveModal } from '@ng-bootstrap/ng-bootstrap';
import { User } from '../../../models/user';
import { FormControl, FormGroup, Validators } from '@angular/forms';

@Component({
  templateUrl: './users-passwd-modal.component.html',
  styleUrls: ['./users-passwd-modal.component.scss']
})
export class UsersPasswdModalComponent {

  @ViewChild('passWordInput', { static: false }) public passWordToggle: ElementRef;
  @Input() public user: User;

  public passwdForm: FormGroup;

  constructor(public activeModal: NgbActiveModal) {
    this.passwdForm = new FormGroup({
      public_id: new FormControl(null),
      password: new FormControl('', Validators.required)
    });
  }

  public get password() {
    return this.passwdForm.get('password');
  }

  public toggleInput() {
    if (this.passWordToggle.nativeElement.type === 'password') {
      this.passWordToggle.nativeElement.type = 'text';
    } else {
      this.passWordToggle.nativeElement.type = 'password';
    }
  }

  public onPasswordChange(): void {
    if (this.passwdForm.valid) {
      this.activeModal.close({public_id: this.user.public_id, password: this.password.value});
    }
  }

}
