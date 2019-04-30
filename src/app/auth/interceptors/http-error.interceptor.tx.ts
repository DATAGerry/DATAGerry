import { Injectable } from '@angular/core';
import { HttpRequest, HttpHandler, HttpEvent, HttpInterceptor } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError } from 'rxjs/operators';
import { NavigationExtras, Router } from '@angular/router';

@Injectable()
export class HttpErrorInterceptor implements HttpInterceptor {

  private readonly possibleStatusCodeList = [
    400,
    401,
    403,
    404,
    405,
    406,
    410,
    500,
    501
  ];

  constructor(private router: Router) {
  }

  intercept(request: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
    return next.handle(request).pipe(catchError(err => {
      const errorExtras: NavigationExtras = {
        queryParams: {
          statusText: err.statusText,
          message: err.message,
          response: JSON.stringify({
            err
          })
        }
      };

      if (this.possibleStatusCodeList.includes(err.status)) {
        this.router.navigate([`/error/${err.status}`], errorExtras);
      }

      const error = err.error.message || err.statusText;
      return throwError(error);
    }));
  }
}
