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

import { Injectable } from '@angular/core';
import { HttpRequest, HttpHandler, HttpEvent, HttpInterceptor } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError } from 'rxjs/operators';
import { NavigationExtras, Router } from '@angular/router';
import { AuthService } from '../../auth/services/auth.service';

@Injectable()
export class HttpErrorInterceptor implements HttpInterceptor {

  public readonly CONNECTION_REFUSED: number = 0;
  public readonly UNAUTHORIZED: number = 401;

  constructor(private router: Router, private authService: AuthService) {
  }

  public intercept(request: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
    return next.handle(request).pipe(catchError(error => {
      const statusCode = error.status;
      switch (statusCode) {
        case this.CONNECTION_REFUSED:
          this.router.navigate(['/connect']);
          break;
        case this.UNAUTHORIZED:
          this.authService.logout();
          this.router.navigate(['/auth/login']);
      }

      return throwError(error);
    }));
  }
}
