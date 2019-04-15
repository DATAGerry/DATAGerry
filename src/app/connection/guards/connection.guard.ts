import { Injectable } from '@angular/core';
import { CanActivate, ActivatedRouteSnapshot, RouterStateSnapshot, UrlTree, Router } from '@angular/router';
import { Observable } from 'rxjs';
import { ConnectionService } from '../services/connection.service';
import { connectableObservableDescriptor } from 'rxjs/internal/observable/ConnectableObservable';

@Injectable({
  providedIn: 'root'
})
export class ConnectionGuard implements CanActivate {

  private connectionIntervalTime: number = 10;
  private interval: any;

  constructor(private router: Router, private connectionService: ConnectionService) {
    // check if connection exists
    this.interval = setInterval(() => {
      if (!this.connectionService.isConnected) {
        this.router.navigate(['/connection']);
      }
    }, this.connectionIntervalTime * 1000);
  }

  canActivate(
    next: ActivatedRouteSnapshot,
    state: RouterStateSnapshot): Observable<boolean | UrlTree> | Promise<boolean | UrlTree> | boolean | UrlTree {
    const currentConnection = this.connectionService.currentConnection;
    if (currentConnection) {
      return true;
    }
    this.router.navigate(['/connection'], {queryParams: {returnUrl: state.url}});
    return false;
  }

}
