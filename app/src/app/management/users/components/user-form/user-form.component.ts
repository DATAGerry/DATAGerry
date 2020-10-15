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
* along with this program. If not, see <https://www.gnu.org/licenses/>.
*/

import { Component, EventEmitter, Input, OnChanges, OnDestroy, OnInit, Output, SimpleChanges } from '@angular/core';
import { User } from '../../../models/user';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { Group } from '../../../models/group';
import { takeUntil } from 'rxjs/operators';
import { ReplaySubject } from 'rxjs';
import { Right } from '../../../models/right';

@Component({
  selector: 'cmdb-user-form',
  templateUrl: './user-form.component.html',
  styleUrls: ['./user-form.component.scss']
})
export class UserFormComponent implements OnInit, OnChanges, OnDestroy {

  /**
   * Component un-subscriber.
   */
  private subscriber: ReplaySubject<void> = new ReplaySubject<void>();

  /**
   * Input if user data exists.
   */
  @Input() public user: User;

  /**
   * List of possible groups.
   */
  @Input() public groups: Array<Group> = [];

  /**
   * List of possible auth providers.
   */
  @Input() public providers: Array<any> = [];

  /**
   * User NgForm.
   */
  public form: FormGroup;

  /**
   * Output if submit was triggered.
   */
  @Output() public submit: EventEmitter<User> = new EventEmitter<User>();

  /**
   * Output if validation status was changed.
   */
  @Output() public validation: EventEmitter<boolean> = new EventEmitter<boolean>();

  constructor() {
    this.form = new FormGroup({
      user_name: new FormControl('', [Validators.required]),
      email: new FormControl('', [Validators.email]),
      password: new FormControl('', [Validators.required]),
      first_name: new FormControl(null),
      last_name: new FormControl(null),
      authenticator: new FormControl('LocalAuthenticationProvider', Validators.required),
      group_id: new FormControl(2, Validators.required),
      image: new FormControl(null)
    });
  }

  public ngOnInit(): void {
    this.form.statusChanges.pipe(takeUntil(this.subscriber)).subscribe(status => {
      this.validation.emit(status);
    });
  }

  public get usernameControl(): FormControl {
    return this.form.get('user_name') as FormControl;
  }

  public get emailControl(): FormControl {
    return this.form.get('email') as FormControl;
  }

  public get passwordControl(): FormControl {
    return this.form.get('password') as FormControl;
  }

  public get firstNameControl() {
    return this.form.get('first_name') as FormControl;
  }

  public get lastNameControl() {
    return this.form.get('last_name') as FormControl;
  }

  public get authenticatorControl() {
    return this.form.get('authenticator') as FormControl;
  }

  public get groupControl() {
    return this.form.get('group_id') as FormControl;
  }

  public onSubmit(): void {
    this.form.markAllAsTouched();
    if (this.form.valid) {
      this.submit.emit(this.form.getRawValue() as User);
    }
  }

  /**
   * OnChange call for user form component.
   * Patches passed user data into the form.
   *
   * @param changes SimpleChanges of all input changes.
   */
  public ngOnChanges(changes: SimpleChanges): void {
    if (changes.user && changes.user.currentValue !== changes.user.previousValue) {
      this.form.patchValue(this.user);
      this.form.markAllAsTouched();
    }
  }

  /**
   * Auto un-subscribe by component destroy.
   */
  public ngOnDestroy(): void {
    this.subscriber.next();
    this.subscriber.complete();
  }

}
