import { Component, OnDestroy, OnInit } from '@angular/core';
import { Observable, Subscription } from 'rxjs';
import { Group } from '../../models/group';
import { GroupService } from '../../services/group.service';
import { ActivatedRoute, Router } from '@angular/router';
import { ToastService } from '../../../layout/toast/toast.service';
import { FormControl, FormGroup, Validators } from '@angular/forms';

@Component({
  selector: 'cmdb-groups-delete',
  templateUrl: './groups-delete.component.html',
  styleUrls: ['./groups-delete.component.scss']
})
export class GroupsDeleteComponent implements OnInit, OnDestroy {

  private groupID: number;
  private routeParamObserver: Observable<any>;
  private routeParamSubscription: Subscription;
  private groupServiceObserver: Observable<Group>;
  private groupServiceSubscription: Subscription;

  public deleteAbleGroup: Group;
  public deleteForm: FormGroup;

  constructor(private groupService: GroupService, private route: ActivatedRoute,
              private toast: ToastService, private router: Router) {
    this.routeParamObserver = this.route.params;
    this.deleteForm = new FormGroup({
      deleteGroupAction: new FormControl('', Validators.required)
    });
  }

  public ngOnInit(): void {
    this.routeParamSubscription = this.routeParamObserver.subscribe(
      (params) => {
        this.groupID = params.publicID;
        this.groupServiceObserver = this.groupService.getGroup(this.groupID);
        this.groupServiceSubscription = this.groupService.getGroup(this.groupID).subscribe((group: Group) => {
          this.deleteAbleGroup = group;
        });
      }
    );
  }

  public onDeleteGroup(): void {
    if (this.deleteForm.valid) {
      const groupDeleteSub = this.groupService.deleteGroup(this.groupID, this.deleteForm.get('deleteGroupAction').value)
        .subscribe(ack => {
            console.log(ack);
          },
          error => {
          console.error(error);
          },
          () => {
            groupDeleteSub.unsubscribe();
          }
        );
    }
  }

  public ngOnDestroy(): void {
    this.routeParamSubscription.unsubscribe();
    this.groupServiceSubscription.unsubscribe();
  }

}
