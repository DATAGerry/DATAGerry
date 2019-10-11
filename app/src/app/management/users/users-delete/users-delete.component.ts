import { Component, OnDestroy, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { Observable, Subscription } from 'rxjs';
import { User } from '../../models/user';
import { UserService } from '../../services/user.service';
import { ToastService } from '../../../layout/toast/toast.service';

@Component({
  selector: 'cmdb-users-delete',
  templateUrl: './users-delete.component.html',
  styleUrls: ['./users-delete.component.scss']
})
export class UsersDeleteComponent implements OnInit, OnDestroy {

  // ROUTE PARAMS
  private routeParamObserver: Observable<any>;
  private routeParamSubscription: Subscription;

  // USER DATA
  public userID: number;
  public deleteUser: User;
  private userServiceObserver: Observable<User>;
  private userServiceSubscription: Subscription;

  constructor(private userService: UserService, private router: Router, private route: ActivatedRoute,
              private toast: ToastService) {
    this.routeParamObserver = this.route.params;
  }

  public ngOnInit(): void {
    this.routeParamSubscription = this.routeParamObserver.subscribe(
      (params) => {
        this.userID = params.publicID;
        this.userServiceObserver = this.userService.getUser(this.userID);
        this.userServiceSubscription = this.userServiceObserver.subscribe((user: User) => {
          this.deleteUser = user;
        });
      }
    );
  }

  public ngOnDestroy(): void {
    this.routeParamSubscription.unsubscribe();
    this.userServiceSubscription.unsubscribe();
  }

  public onDelete(): void{
    this.userService.deleteUser(this.userID).subscribe((ack: boolean) => {
      this.toast.show('User was deleted');
      this.router.navigate(['/management/users']);
    });
  }

}
