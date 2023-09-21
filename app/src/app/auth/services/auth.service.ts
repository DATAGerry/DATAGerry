/*
* DATAGERRY - OpenSource Enterprise CMDB
* Copyright (C) 2023 becon GmbH
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
*
* You should have received a copy of the GNU Affero General Public License
* along with this program. If not, see <https://www.gnu.org/licenses/>.
*/

import { Injectable } from '@angular/core';
import { HttpBackend, HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { Router } from '@angular/router';

import { BehaviorSubject, Observable } from 'rxjs';
import { map } from 'rxjs/operators';

import { NgbModal, NgbModalOptions } from '@ng-bootstrap/ng-bootstrap';
import { NgxIndexedDBService } from 'ngx-indexed-db';


import { PermissionService } from './permission.service';
import { ConnectionService } from '../../connect/connection.service';
import { ApiCallService, ApiServicePrefix, httpObserveOptions } from '../../services/api-call.service';
import { SpecialService } from '../../framework/services/special.service';

import { User } from '../../management/models/user';
import { IntroComponent } from '../../layout/intro/intro.component';
import { StepByStepIntroComponent } from '../../layout/intro/step-by-step-intro/step-by-step-intro.component';
import { LoginResponse } from '../models/responses';
import { Token } from '../models/token';
/* ------------------------------------------------------------------------------------------------------------------ */


const httpOptions = {
  headers: new HttpHeaders({
    'Content-Type': 'application/json'
  })
};


@Injectable({
  providedIn: 'root'
})
export class AuthService<T = any> implements ApiServicePrefix {

  // Rest backend
  private restPrefix: string = 'rest';
  public readonly servicePrefix: string = 'auth';
  private http: HttpClient;

  // User storage
  private currentUserSubject: BehaviorSubject<User>;
  public currentUser: Observable<User>;
  private currentUserTokenSubject: BehaviorSubject<Token>;
  public currentUserToken: Observable<Token>;

  // First Step Intro
  private startIntroModal: any = undefined;
  private stepByStepModal: any = undefined;

  constructor(private backend: HttpBackend, 
              private connectionService: ConnectionService, 
              private api: ApiCallService,
              private permissionService: PermissionService, 
              private router: Router, 
              private introService: NgbModal,
              private specialService: SpecialService, 
              private indexDB: NgxIndexedDBService) {

    this.http = new HttpClient(backend);
    this.currentUserSubject = new BehaviorSubject<User>(
      JSON.parse(localStorage.getItem('current-user')));
    this.currentUser = this.currentUserSubject.asObservable();

    this.currentUserTokenSubject = new BehaviorSubject<Token>(
      JSON.parse(localStorage.getItem('access-token')));
    this.currentUserToken = this.currentUserTokenSubject.asObservable();
  }

  public get currentUserValue(): User {
    return this.currentUserSubject.value;
  }

  public get currentUserTokenValue(): Token {
    return this.currentUserTokenSubject.value;
  }


  public getProviders(): Observable<Array<T>> {
    const options = httpObserveOptions;
    options.params = new HttpParams();
    return this.api.callGet<Array<T>>(`${ this.servicePrefix }/providers`, options).pipe(
      map((apiResponse) => {
        return apiResponse.body as Array<T>;
      })
    );
  }


  public getSettings(): Observable<T> {
    const options = httpObserveOptions;
    options.params = new HttpParams();
    return this.api.callGet<T[]>(`${ this.servicePrefix }/settings`, options).pipe(
      map((apiResponse) => {
        return apiResponse.body;
      })
    );
  }


  public postSettings(data: T): Observable<T> {
    const options = httpObserveOptions;
    options.params = new HttpParams();
    return this.api.callPost<T>(`${ this.servicePrefix }/settings`, data, options).pipe(
      map((apiResponse) => {
        return apiResponse.body;
      })
    );
  }

/* ------------------------------------------------------------------------------------------------------------------ */
/*                                                   LOGIN / LOGOUT                                                   */
/* ------------------------------------------------------------------------------------------------------------------ */
  public login(username: string, password: string) {
    const data = {
      user_name: username,
      password
    };
    return this.http.post<LoginResponse>(
      `${ this.connectionService.currentConnection }/${ this.restPrefix }/${ this.servicePrefix }/login`, data, httpOptions)
      .pipe(map((response: LoginResponse) => {
        const token: Token = {
          token: response.token,
          issued: response.token_issued_at,
          expire: response.token_expire
        };
        localStorage.setItem('current-user', JSON.stringify(response.user));
        localStorage.setItem('access-token', JSON.stringify(token));
        this.currentUserSubject.next(response.user);
        this.currentUserTokenSubject.next(token);
        this.showIntro();
        return response;
      }));
  }

  public logout() {
    this.indexDB.clear('user-settings').subscribe();
    localStorage.removeItem('current-user');
    localStorage.removeItem('access-token');
    this.currentUserSubject.next(undefined);
    this.currentUserTokenSubject.next(undefined);
    this.permissionService.clearUserRightStorage();

    // Close Intro-Modal if open
    if (this.startIntroModal !== undefined) {
      this.startIntroModal.close();
    }
    if (this.stepByStepModal !== undefined) {
      this.stepByStepModal.close();
    }
    this.router.navigate(['/auth']);
  }

/* ------------------------------------------------------------------------------------------------------------------ */
/*                                                    INTRO SECTION                                                   */
/* ------------------------------------------------------------------------------------------------------------------ */
  public showIntro() {
    this.specialService.getIntroStarter().subscribe(value => {
      const options: NgbModalOptions = { centered: true, backdrop: 'static', keyboard: true, windowClass: 'intro-tour', size: 'lg' };
      const RUN = 'execute';
      // if (!value[RUN]) {
      if (!value[RUN]) {
        
        
        this.startIntroModal = this.introService.open(IntroComponent, options);
        this.startIntroModal.result.then((result) => {
          if (result) {
            this.router.navigate(['/framework/category/add']);
            this.showSteps();
          }
        }, 
        (reason) => {
          console.log(reason);
        });
      } else {
        //display assistant not usable
        this.startIntroModal = this.introService.open(IntroComponent, options);
        this.startIntroModal.componentInstance.isUsable = false;
      }
    });
  }

  private showSteps() {
    const options = { backdrop: false, keyboard: true, windowClass: 'step-by-step' };
    this.stepByStepModal = this.introService.open(StepByStepIntroComponent, options);
    this.stepByStepModal.result.then((resp) => {
      if (resp) {
        this.router.navigate(['/']);
      }
    }, (reason) => {
      console.log(reason);
    });
  }
}
