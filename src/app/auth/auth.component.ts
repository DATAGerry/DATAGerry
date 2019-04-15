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
