import { Component, OnChanges, OnDestroy, OnInit, SimpleChanges } from '@angular/core';
import { GroupService } from '../../services/group.service';
import { ActivatedRoute, Router } from '@angular/router';
import { Observable, Subscription } from 'rxjs';
import { Group } from '../../models/group';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { RightService } from '../../services/right.service';
import { Right } from '../../models/right';
import { ToastService } from '../../../layout/toast/toast.service';

@Component({
  selector: 'cmdb-groups-edit',
  templateUrl: './groups-edit.component.html',
  styleUrls: ['./groups-edit.component.scss']
})
export class GroupsEditComponent implements OnInit, OnDestroy {

  private groupID: number;
  private routeParamObserver: Observable<any>;
  private routeParamSubscription: Subscription;
  private groupServiceObserver: Observable<Group>;
  private groupServiceSubscription: Subscription;
  private rightServiceSubscription: Subscription;

  public rightList: Right[];
  public editGroup: Group;
  public editForm: FormGroup;

  public constructor(private groupService: GroupService, private rightService: RightService, private route: ActivatedRoute,
                     private toast: ToastService, private router: Router) {
    this.routeParamObserver = this.route.params;
    this.editForm = new FormGroup({
      public_id: new FormControl(0),
      name: new FormControl('', Validators.required),
      label: new FormControl(''),
      rights: new FormControl([], Validators.minLength(1))
    });
  }

  public ngOnInit(): void {
    this.routeParamSubscription = this.routeParamObserver.subscribe(
      (params) => {
        this.groupID = params.publicID;
        this.groupServiceObserver = this.groupService.getGroup(this.groupID);
        this.groupServiceSubscription = this.groupService.getGroup(this.groupID).subscribe((group: Group) => {
          this.editGroup = group;
          this.patchGroupToForm();
        });
      }
    );
    this.rightServiceSubscription = this.rightService.getRightList().subscribe((rightList: Right[]) => {
      this.rightList = rightList;
    });
  }

  private patchGroupToForm() {
    Object.keys(this.editGroup).forEach(name => {
      if (this.editForm.controls[name]) {
        this.editForm.controls[name].patchValue(this.editGroup[name], { onlySelf: true });
      }
    });
    this.editForm.markAllAsTouched();
  }

  public groupByFn(item) {
    const baseData = item.name.split('.');
    return `${ baseData[0] }.${ baseData[1] }.*`;
  }

  public get name() {
    return this.editForm.get('name');
  }

  public get label() {
    return this.editForm.get('label');
  }

  public get rights() {
    return this.editForm.get('rights');
  }

  public updateGroup() {
    const updateData = this.editForm.getRawValue();
    const updateSub: Subscription = this.groupService.putGroup(this.groupID, updateData).subscribe(ack => {
        if (ack) {
          this.toast.show('Group was updated');
          this.router.navigate(['/management/groups/']);
        }
      },
      (error) => {
        console.error(error);
      }, () => {
        updateSub.unsubscribe();
      });
  }

  public ngOnDestroy(): void {
    this.routeParamSubscription.unsubscribe();
    this.groupServiceSubscription.unsubscribe();
    this.rightServiceSubscription.unsubscribe();
  }

}
