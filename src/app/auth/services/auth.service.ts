import { Injectable } from '@angular/core';
import { ApiCallService } from '../../services/api-call.service';
import { BehaviorSubject, Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import { UserToken } from '../models/user-token';


@Injectable({
  providedIn: 'root'
})
export class AuthService {

  private currentUserSubject: BehaviorSubject<UserToken>;
  public currentUser: Observable<UserToken>;

  constructor(private api: ApiCallService) {
    this.currentUserSubject = new BehaviorSubject<UserToken>(JSON.parse(localStorage.getItem('access-token')));
    this.currentUser = this.currentUserSubject.asObservable();
  }

  public get currentUserValue(): UserToken {
    return this.currentUserSubject.value;
  }


  public login(userName: string, userPassword: string) {
    const data = {
      user_name: userName,
      password: userPassword
    };
    const apiResponse = this.api.callPostRoute('auth/login', data);

    apiResponse.subscribe((loginResponse: any) => {
        localStorage.setItem('access-token', JSON.stringify(loginResponse));
        this.currentUserSubject.next(loginResponse);
      }
    );

    return apiResponse;

  }

  public logout() {
    localStorage.removeItem('access-token');
    this.currentUserSubject.next(null);
  }
}
