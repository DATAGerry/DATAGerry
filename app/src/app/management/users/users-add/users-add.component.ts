import { Component, ElementRef, OnInit, ViewChild } from '@angular/core';
import { AbstractControl, FormControl, FormGroup, Validators } from '@angular/forms';
import { AuthService } from '../../../auth/services/auth.service';
import { UserService } from '../../services/user.service';
import { User } from '../../models/user';
import { Group } from '../../models/group';
import { GroupService } from '../../services/group.service';
import { ToastService } from '../../../layout/services/toast.service';
import { Router } from '@angular/router';


@Component({
  selector: 'cmdb-users-add',
  templateUrl: './users-add.component.html',
  styleUrls: ['./users-add.component.scss']
})
export class UsersAddComponent implements OnInit {

  @ViewChild('passWordInput', {static: false}) public passWordToggle: ElementRef;

  public addForm: FormGroup;
  public authProviders: string[];
  public groupList: Group[];
  private currentPasswordStrength: number = 0;
  public preview: any = undefined;

  constructor(private authService: AuthService, private userService: UserService, private groupService: GroupService,
              private toastService: ToastService, private router: Router) {
    this.authService.getAuthProviders().subscribe((authList: string[]) => {
      this.authProviders = authList;
    });
    this.groupService.getGroupList().subscribe((groupList: Group[]) => {
      this.groupList = groupList;
    });
  }

  private passwordStringValidator(threshold: number = 2) {
    return (control: AbstractControl) => {
      if (this.currentPasswordStrength < threshold) {
        return {
          strength: {valid: false}
        };
      }
      return null;
    };
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

  public generatePassword(length: number = 12) {
    const chars = 'abcdefghijklmnopqrstuvwxyz!@#$%^&*()-+<>ABCDEFGHIJKLMNOP1234567890';
    let pass = '';
    for (let x = 0; x < length; x++) {
      const i = Math.floor(Math.random() * chars.length);
      pass += chars.charAt(i);
    }
    this.passWordToggle.nativeElement.value = pass;
    this.password.clearValidators();
    this.password.setValue(this.passWordToggle.nativeElement.value);
    this.password.markAsDirty();
    this.password.markAsTouched();
    this.password.disable();
  }

  public ngOnInit(): void {
    this.addForm = new FormGroup({
      user_name: new FormControl('', Validators.required),
      email: new FormControl('', [Validators.required, Validators.email]),
      password: new FormControl('', [Validators.required, this.passwordStringValidator()]),
      first_name: new FormControl(null),
      last_name: new FormControl(null),
      authenticator: new FormControl('LocalAuthenticationProvider', Validators.required),
      group_id: new FormControl(null, Validators.required),
      image: new FormControl(null)
    });
    this.authenticator.disable();
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
        this.toastService.show(`User was added with ID: ${addResp}`);
      }, (error) => {
        console.error(error);
      }, () => {
        this.router.navigate(['/management/users/']);
      });
    }
  }
}
