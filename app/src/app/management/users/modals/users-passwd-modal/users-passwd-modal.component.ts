import { Component, ElementRef, Input, ViewChild } from '@angular/core';
import { NgbActiveModal } from '@ng-bootstrap/ng-bootstrap';
import { User } from '../../../models/user';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { UserService } from '../../../services/user.service';
import { ToastService } from '../../../../layout/toast/toast.service';

@Component({
  templateUrl: './users-passwd-modal.component.html',
  styleUrls: ['./users-passwd-modal.component.scss']
})
export class UsersPasswdModalComponent {

  @ViewChild('passWordInput', { static: false }) public passWordToggle: ElementRef;

  // Data
  // tslint:disable-next-line:variable-name
  private _user: User;

  @Input('user')
  public set user(value: User) {
    this._user = value;
    this.passwdForm.get('public_id').setValue(this._user.public_id);
  }

  public get user(): User {
    return this._user;
  }

  // Form
  public passwdForm: FormGroup;

  constructor(private userService: UserService, private toast: ToastService, public activeModal: NgbActiveModal) {
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

  public changePasswd() {
    if (this.passwdForm.valid) {
      const changePasswd = this.userService.changeUserPassword(this.user.public_id, this.passwdForm.get('password').value).subscribe(
        () => {
          this.toast.success(`Password for user with ID: ${ this.user.public_id } was changed`);
        },
        (error => {
          console.error(error);
          this.activeModal.close();
        }),
        () => {
          this.activeModal.close();
          changePasswd.unsubscribe();
        }
      );
    }
  }

}
